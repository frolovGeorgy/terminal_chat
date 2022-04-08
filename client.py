import socket
import threading


class Client:
    HOST: str = '127.0.0.1'
    PORT: int = 3228

    def __init__(self):
        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))
        self.nickname = self._set_nickname()
        receive_thread = threading.Thread(target=self._receive_a_message)
        send_thread = threading.Thread(target=self._send_a_message)
        receive_thread.start()
        send_thread.start()

    def _receive_a_message(self) -> None:
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                print(message)
            except:
                print('Something went wrong')
                self.client.close()
                break

    def _send_a_message(self) -> None:
        while True:
            message = input()
            self.client.send(message.encode('utf-8'))

    def _set_nickname(self) -> str:
        message = self.client.recv(1024).decode('utf-8')
        nickname = input(message)
        self.client.send(nickname.encode('utf-8'))
        message = self.client.recv(1024).decode('utf-8')
        while message == 'This nickname already exists, please try again: ':
            nickname = input(message)
            self.client.send(nickname.encode('utf-8'))
            message = self.client.recv(1024).decode('utf-8')
        print(message)
        return nickname


if __name__ == '__main__':
    client = Client()
