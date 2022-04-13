import asyncio
import re

import bidict
import websockets

from logging_config import log

HOST = '0.0.0.0'
PORT = 3228

PING_INTERVAL = 5

PING_TIMEOUT = 100

clients = bidict.bidict()


async def handler(websock):
    try:
        await get_new_user(websock)
        async for message in websock:
            username = clients[websock]
            if message.startswith('/'):
                await command_handler(websock, message)
            else:
                websockets.broadcast(clients.keys(), f'{username}: {message}')
            log.info(f'{username}: {message}')
    finally:
        username = clients.pop(websock)
        websockets.broadcast(clients.keys(), f'{username} disconnected from server')
        log.debug(f'{username} disconnected from server')


async def get_new_user(websock):
    name = await websock.recv()
    while name in clients.values():
        await websock.send('This nickname already exists, please try again: ')
        name = await websock.recv()
    clients[websock] = name
    await websock.send(f'Welcome to server, {name}!')
    websockets.broadcast(clients.keys(), f'{name} connected')


async def command_handler(websock, message):
    receiver_client = None
    if message.startswith('/members'):
        response = f'Current members: {[member for member in clients.values()]}'
    elif message.startswith('/to'):
        response, receiver_client = get_receiver_and_message(message)
    elif message.startswith('/commands'):
        response = 'Commands:\n- "/members" list of current members\n' \
                   '- "/to <nickname>" send private message to member with nickname <nickname>'
    else:
        response = 'Command not found'

    if receiver_client:
        await send_private_message(response, receiver_client, websock)
    else:
        await websock.send(response)
        log.debug(f'{clients[websock]} got response ({response}) to command "{message}"')


async def send_private_message(message, receiver, websock):
    try:
        await asyncio.sleep(10)
        await receiver.send(f'{clients[websock]} (private): {message}')
    except (websockets.ConnectionClosedOK, websockets.ConnectionClosedError, KeyError):
        await websock.send(f'Message not delivered')
        log.debug(f'Message from {clients[websock]} not delivered')
    else:
        await websock.send('Message delivered')
        log.debug(f'Message from {clients[websock]} successfully delivered to {clients[receiver]}')
        log.info(f'{clients[websock]} (private to {clients[receiver]}): {message}')


def get_receiver_and_message(message):
    receiver = re.findall(r'^(?:\S+\s){1}(\S+)', message)[0]
    receiver_client = clients.inverse.get(receiver)
    if receiver_client:
        response = message.partition(f'/to {receiver} ')[2]
        response = '<empty message>' if not response else response
    else:
        response = f'Member with nickname {receiver} not found'
    return response, receiver_client


async def main():
    log.debug('server starting...')
    async with websockets.serve(
            handler,
            HOST,
            PORT,
            ping_interval=PING_INTERVAL,
            ping_timeout=PING_TIMEOUT
    ):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
