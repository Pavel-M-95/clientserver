import argparse
import json
import logging
import select
import sys
import socket
import time

import logs.configuration_server
from utils.decorators import log

from utils.utils import load_configs, get_message, send_message

CONFIGS = dict()

SERVER_LOGGER = logging.getLogger('server')


@log
def handle_message(message, messages_list, client, CONFIGS):
    global SERVER_LOGGER
    SERVER_LOGGER.debug(f'Обработка сообщения от клиента : {message}')
    if CONFIGS.get('ACTION') in message \
            and message[CONFIGS.get('ACTION')] == CONFIGS.get('PRESENCE') \
            and CONFIGS.get('TIME') in message \
            and CONFIGS.get('USER') in message \
            and message[CONFIGS.get('USER')][CONFIGS.get('ACCOUNT_NAME')] == 'Guest':
        return {CONFIGS.get('RESPONSE'): 200}
    return {
        CONFIGS.get('RESPONSE'): 400,
        CONFIGS.get('ERROR'): 'Bad Request'
    }


def arg_parser(CONFIGS):
    global SERVER_LOGGER
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=CONFIGS['DEFAULT_PORT'], type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с некорректного порта {listen_port}.'
                               'Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    return listen_address, listen_port


def main():
    global CONFIGS, SERVER_LOGGER
    CONFIGS = load_configs()
    listen_address, listen_port = arg_parser(CONFIGS)
    SERVER_LOGGER.info(f'Сервер запущен на порту: {listen_port}, по адресу: {listen_address}.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []

    transport.listen(CONFIGS.get('MAX_CONNECTIONS'))

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    handle_message(get_message(client_with_message, CONFIGS), messages, client_with_message, CONFIGS)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                CONFIGS['ACTION']: CONFIGS['MESSAGE'],
                CONFIGS['SENDER']: messages[0][0],
                CONFIGS['TIME']: time.time(),
                CONFIGS['MESSAGE_TEXT']: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message, CONFIGS)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
