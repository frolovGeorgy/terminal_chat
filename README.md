+ сервер:
  + на TCP порт принимает запросы от клиентов;
  + поддерживает минимум 2-х клиентов единовременно;
  + доставляет сообщение адресату;
  + об успехе или неуспехе сообщает отправителю;
  + логирует сообщения клиентов в syslog.
+ клиенты:
  + получают сообщения от сервера;
  + отправляют сообщения;
  + получают подтверждение о доставке.


Создание образа
```
$ docker build -t terminal_chat .
```
Запуск сервера
```
$ docker run -p 3228:3228 terminal_chat server.py
```
Подключение к серверу
```
$ docker run -p 3228:3228 terminal_chat client.py
```