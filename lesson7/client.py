import argparse
import json
import logging
import sys
import socket
import time
import logs.configuration_client
from utils.decorators import Log
from errors import ReqFieldMissingError, ServerError

from utils.utils import load_configs, send_message, get_message

CONFIGS = dict()
SERVER_LOGGER = logging.getLogger('client')


@Log()
def create_presence_message(CONFIGS, account_name='Guest'):
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    SERVER_LOGGER.info('Создание сообщения для отпарвки на сервер.')
    return message


def get_user_message(sock, CONFIGS, account_name='Guest'):
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        SERVER_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        CONFIGS['ACTION']: CONFIGS['MESSAGE'],
        CONFIGS['TIME']: time.time(),
        CONFIGS['ACCOUNT_NAME']: account_name,
        CONFIGS['MESSAGE_TEXT']: message
    }
    SERVER_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


def handle_server_message(message, CONFIG):
    if CONFIG['ACTION'] in message and message[CONFIG['ACTION']] == CONFIG['MESSAGE'] and \
            CONFIG['SENDER'] in message and CONFIG['MESSAGE_TEXT'] in message:
        print(f'Получено сообщение от пользователя '
              f'{message[CONFIG["SENDER"]]}:\n{message[CONFIG["MESSAGE_TEXT"]]}')
        SERVER_LOGGER.info(f'Получено сообщение от пользователя '
                    f'{message[CONFIG["SENDER"]]}:\n{message[CONFIG["MESSAGE_TEXT"]]}')
    else:
        SERVER_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@Log()
def arg_parser(CONFIGS):
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=CONFIGS['DEFAULT_IP_ADDRESS'], nargs='?')
    parser.add_argument('port', default=CONFIGS['DEFAULT_PORT'], type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        SERVER_LOGGER.critical('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        SERVER_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


@Log()
def handle_response(message, CONFIGS):
    SERVER_LOGGER.info('Обработка сообщения от сервера.')
    if CONFIGS.get('RESPONSE') in message:
        if message[CONFIGS.get('RESPONSE')] == 200:
            SERVER_LOGGER.info('Успешная обработка сообшения от сервера.')
            return '200 : OK'
        SERVER_LOGGER.critical('Обработка сообщения от сервера провалилась.')
        return f'400 : {message[CONFIGS.get("ERROR")]}'
    raise ValueError


def main():
    global CONFIGS
    CONFIGS = load_configs(is_server=False)
    server_address, server_port, client_mode = arg_parser(CONFIGS)
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence_message(CONFIGS), CONFIGS)
        answer = handle_response(get_message(transport, CONFIGS), CONFIGS)
        print(client_mode)
        SERVER_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        SERVER_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        SERVER_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        SERVER_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        SERVER_LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            print(client_mode)
            if client_mode == 'send':
                try:
                    send_message(transport, get_user_message(transport, CONFIGS), CONFIGS)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    SERVER_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    handle_server_message(get_message(transport, CONFIGS), CONFIGS)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    SERVER_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
