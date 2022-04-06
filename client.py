import socket
import threading


def receive_a_message() -> None:
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print('Something went wrong')
            client.close()
            break


def send_a_message() -> None:
    while True:
        message = input()
        client.send(message.encode('utf-8'))


def set_nickname() -> str:
    message = client.recv(1024).decode('utf-8')
    nickname = input(message)
    client.send(nickname.encode('utf-8'))
    message = client.recv(1024).decode('utf-8')
    while message == 'This nickname already exists, please try again: ':
        nickname = input(message)
        client.send(nickname.encode('utf-8'))
        message = client.recv(1024).decode('utf-8')
    print(message)
    return nickname


if __name__ == '__main__':
    HOST: str = '127.0.0.1'
    PORT: int = 3228

    client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    nickname = set_nickname()

    receive_thread = threading.Thread(target=receive_a_message)
    send_thread = threading.Thread(target=send_a_message)

    receive_thread.start()
    send_thread.start()
