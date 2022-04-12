import asyncio
import websockets


async def handler():
    try:
        async with websockets.connect("ws://localhost:8765") as websock:
            name = input('Hello, please input your name: ')
            await websock.send(name)
            while True:
                await asyncio.gather(
                    get_message(websock),
                    send_message(websock, name)
                )
    except websockets.ConnectionClosed:
        print('Something go wrong')


async def get_message(websock):
    message = await websock.recv()
    print(message)


async def send_message(websock, name):
    await websock.send(input(f'{name}: '))


asyncio.run(handler())
