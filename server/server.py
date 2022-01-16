import select
import socket
import sys
from JIMProtocol import MessageBuilder
import baselogerconfig
from log_config import log


class Server:
    _server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создает сокет TCP
    connections = []

    def __init__(self, ip="localhost", port=7777):
        self._server_socket.bind((ip, port))  # Присваивает порт 8888
        self._server_socket.listen(5)  # Переходит в режим ожидания запросов;
        # одновременно обслуживает не более 5 запросов
        self._server_socket.settimeout(0.5) # Необходимо, чтобы не ждать появление данных в сокете
        print('Server started...')

    @log
    def run(self):
        while True:
            try:
                client, addr = self._server_socket.accept()  # Принять запрос на соединение
            except OSError as ex:
                pass # timeout вышел и ничего оне произошло
            else:
                print("Получен запрос на соединение от %s" % str(addr))
                self.connections.append(client)
            finally:
                r = []
                w = []
                try:
                    r, w, e = select.select(self.connections, self.connections,[],0)
                except Exception as e:
                    pass #Исключение произойдет, если какой-то клиент отключился
                        # Ничего не делаем...
                for client in r:
                    data = client.recv(1024)  # Принять не более 1024 байтов данных
                    parsed_msg = self.parse_message(data)
                    try:
                        if parsed_msg.action == "presence" and (client in w):
                            self.send_responce(client, 200, "{} is currently present.".format(parsed_msg.user.name))
                    except:
                        self.connections.remove(client)

    @log
    def parse_message(self, msg):
        msg = msg.decode("ascii")
        print(msg)
        parsed_msg = MessageBuilder.get_object_of_json(msg)
        return parsed_msg

    @log
    def send_responce(self, client, code, alert=None):
        gen_response = MessageBuilder.create_response_message(code, alert)
        gen_response_json = gen_response.encode_to_json()
        client.send(gen_response_json.encode('ascii'))


if __name__ == '__main__':
    if (len(sys.argv))> 1:
        server = Server(str(sys.argv[1]), int(sys.argv[2]))
        server.run()
    else:
        server = Server()
        server.run()
