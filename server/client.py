import socket
import sys
from JIMProtocol import MessageBuilder
import baselogerconfig
# from log_config import log


class Client:
    _client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, server_address='localhost', port=7777):
        self._client_socket.connect((server_address, port))  # Соединиться с сервером
        self.login = None

    def run(self):
        while True:
            self.sendMsg("presence")
            response = self._client_socket.recv(1024)
            response, alert = self.parse_response(response)

    def get_data(self):
        data = None
        while data is None:
            data = self._client_socket.recv(1024)

    def parse_response(self, response):
        response = response.decode("ascii")
        print(response)
        parsed_response = MessageBuilder.get_object_of_json(response)
        print(parsed_response.response)
        print(parsed_response.alert)
        return parsed_response.response, parsed_response.alert

    def sendMsg(self, type="presence"):
        if self.login is None:
            #self.login = input("Login:")
            self.login = "User"
        gen_message = MessageBuilder.create_presence_message(self.login)
        gen_message_json = gen_message.encode_to_json()
        self._client_socket.send(gen_message_json.encode('ascii'))

    def __del__(self):
        self._client_socket.close()


if __name__ =='__main__':
    if (len(sys.argv)) == 2:
        client = Client(str(sys.argv[1]), int(sys.argv[2]))
        client.run()
    else:
        client = Client()
        client.run()
