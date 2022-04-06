import socket
import threading
import re
from typing import Optional


def receive_connection() -> None:
    while True:
        client, address = server.accept()
        print(f'Connected from {str(address)}')
        message_thread = threading.Thread(target=get_a_message_from_client, args=(client,))
        message_thread.start()


def get_client_nickname(client: socket.socket) -> None:
    client.send('Input your nickname: '.encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')
    while nickname in clients.values():
        client.send('This nickname already exists, please try again: '.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
    message_for_all_clients(f'{nickname} connected to the chat')
    clients[client] = nickname
    client.send(f'You are connect to the chat as {nickname}'.encode('utf-8'))


def handle_command(message: str) -> tuple[str, Optional[str]]:
    if message.startswith('/members'):
        response = f'Current members: {[member for member in clients.values()]}'
        return (response, None)
    elif message.startswith('/to'):
        receiver = re.search(r'(?<=/to ).+?(?=\s)', message)[0]
        regular_expression = f'(?<=^/to {receiver} ).+'
        response = re.search(regular_expression, message)[0]
        return (response, receiver)


def get_a_message_from_client(client: socket.socket) -> None:
    get_client_nickname(client)
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('/'):
                #TODO add handler command
                handle_command(message)
            message_for_all_clients(f'{clients[client]}: {message}')
        except:
            nickname = clients.pop(client)
            print(f'{nickname} left the chat')
            message_for_all_clients(f'{nickname} left the chat')
            break


def message_for_all_clients(message: str) -> None:
    for client in clients.keys():
        client.send(message.encode('utf-8'))


if __name__ == '__main__':
    HOST: str = '127.0.0.1'
    PORT: int = 3228
    NUMBER_OF_WAITING_CONNECTIONS: int = 5

    clients: dict[socket.socket, str] = {}

    server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(NUMBER_OF_WAITING_CONNECTIONS)

    print('Server start working...')
    receive_connection()
