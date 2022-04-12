import socket
import threading
import re
from typing import Optional, Tuple

from bidict import bidict

from logging_config import log


class Server:
    HOST: str = '0.0.0.0'
    PORT: int = 3228
    NUMBER_OF_WAITING_CONNECTIONS: int = 5

    clients: bidict[socket.socket, str] = bidict()

    server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.log = log

    def start(self):
        self.server.bind((self.HOST, self.PORT))
        self.server.listen(self.NUMBER_OF_WAITING_CONNECTIONS)
        self.log.debug(f'Server start working on {self.HOST}:{self.PORT}...')
        self._receive_connection()

    def _receive_connection(self) -> None:
        while True:
            client, address = self.server.accept()
            self.log.debug(f'Connected from {str(address)}')
            message_thread = threading.Thread(target=self._get_a_message_from_client, args=(client,))
            message_thread.start()

    def _get_a_message_from_client(self, client: socket.socket) -> None:
        self._set_client_nickname(client)
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message.startswith('/'):
                    self._handle_command(message, client)
                else:
                    self._message_for_all_clients(f'{self.clients[client]}: {message}')
            except:
                nickname = self.clients.pop(client)
                self.log.debug(f'{nickname} left the chat')
                self._message_for_all_clients(f'{nickname} left the chat')
                break

    def _message_for_all_clients(self, message: str) -> None:
        for client in self.clients.keys():
            client.send(message.encode('utf-8'))
            self.log.info(f'Message for all members: {message}')

    def _set_client_nickname(self, client: socket.socket) -> None:
        client.send('Input your nickname: '.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        while nickname in self.clients.values():
            client.send('This nickname already exists, please try again: '.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.log.debug(f'New user try to set a name ({nickname}), but it already exists')
        self._message_for_all_clients(f'{nickname} connected to the chat')
        self.clients[client] = nickname
        client.send(
            f'You are connect to the chat as {nickname}\nInput "/commands" to get a list of commands'.encode('utf-8'))
        self.log.debug(f'New user set a name: {nickname}')

    def _handle_command(self, message: str, client: socket.socket) -> None:
        receiver_client = None
        if message.startswith('/members'):
            response = f'Current members: {[member for member in self.clients.values()]}'
        elif message.startswith('/to'):
            response, receiver_client = self._get_receiver_and_message(message)
        elif message.startswith('/commands'):
            response = 'Commands:\n- "/members" list of current members\n' \
                       '- "/to <nickname>" send private message to member with nickname <nickname>'
        else:
            response = 'Command not found'

        if receiver_client:
            self._send_private_message(response, receiver_client, client)
        else:
            client.send(response.encode('utf-8'))
            self.log.debug(f'{self.clients[client]} got response ({response}) to command "{message}"')

    def _get_receiver_and_message(self, message: str) -> Tuple[str, Optional[socket.socket]]:
        receiver = re.findall(r'^(?:\S+\s){1}(\S+)', message)[0]
        receiver_client = self.clients.inverse.get(receiver)
        if receiver_client:
            response = message.partition(f'/to {receiver} ')[2]
            response = '<empty message>' if not response else response
        else:
            response = f'Member with nickname {receiver} not found'
        return response, receiver_client

    def _send_private_message(self, message: str, receiver: socket.socket, client: socket.socket):
        status = receiver.sendall(f'{self.clients[client]} (private): {message}'.encode('utf-8'))
        if status is None:
            client.send('Message delivered'.encode('utf-8'))
            self.log.debug(f'Message from {self.clients[client]} successfully delivered to {self.clients[receiver]}')
            self.log.info(f'{self.clients[client]} (private to {self.clients[receiver]}): {message}')
        else:
            client.send(
                f'Message from {self.clients[client]} not delivered to {self.clients[receiver]}'.encode('utf-8'))


if __name__ == '__main__':
    server = Server()
    server.start()
