import asyncio

import bidict
import websockets

clients = bidict.bidict()


async def get_new_user(websock):
    name = await websock.recv()
    clients[websock] = name
    websockets.broadcast(clients.keys(), f'{name} connected')


async def handler(websock):
    try:
        await get_new_user(websock)
        async for message in websock:
            username = clients[websock]
            if message.startswith('/'):
                await websock.send(clients.values())
            else:
                websockets.broadcast(clients.keys(), f'{username}: {message}')
            print(f'{username}: {message}')
    finally:
        username = clients.pop(websock)
        websockets.broadcast(clients.keys(), f'{username} disconnected from server')


async def main():
    print('server starting...')
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()


asyncio.run(main())
