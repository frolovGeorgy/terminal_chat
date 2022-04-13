import asyncio

import aioconsole
import websockets

HOST = '0.0.0.0'
PORT = 3228

PING_INTERVAL = 5

PING_TIMEOUT = 100


async def connection_handler():
    try:
        async with websockets.connect(
                f"ws://{HOST}:{PORT}",
                ping_interval=PING_INTERVAL,
                ping_timeout=PING_TIMEOUT
        ) as websock:
            name = input('Hello, please input your name: ')
            await websock.send(name)
            message = await websock.recv()
            while message == 'This nickname already exists, please try again: ':
                print(message)
                name = await aioconsole.ainput()
                await websock.send(name)
                message = await websock.recv()
            print(message)
            await asyncio.gather(
                send_message(websock),
                get_message(websock),
            )
    except websockets.ConnectionClosed:
        print('Connection closed')


async def get_message(websock):
    async for message in websock:
        print(message)


async def send_message(websock):
    while True:
        line = await aioconsole.ainput()
        await websock.send(line)


if __name__ == '__main__':
    asyncio.run(connection_handler())
