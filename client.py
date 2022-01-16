import json
import sys
import socket
import time

from util import load_config, send_message, get_message

CONFIGS = dict()


def create_presence_message(account_name):
    message = {
        CONFIGS.get('ACTION'): CONFIGS.get('PRESENCE'),
        CONFIGS.get('TIME'): time.time(),
        CONFIGS.get('USER'): {
            CONFIGS.get('ACCOUNT_NAME'): account_name
        }
    }
    return message


def handle_response(message):
    if CONFIGS.get('RESPONSE') in message:
        if message[CONFIGS.get('RESPONSE')] == 200:
            return '200 : OK'
        return f'400 : {message[CONFIGS.get("ERROR")]}'
    raise ValueError


def main():
    global CONFIGS
    CONFIGS = load_config(is_server=False)
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if not 65535 >= server_port >= 1024:
            raise ValueError
    except IndexError:
        server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
        server_port = CONFIGS.get('DEFAULT_PORT')
    except ValueError:
        print('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    presence_message = create_presence_message('Guest')
    send_message(transport, presence_message, CONFIGS)
    try:
        response = get_message(transport, CONFIGS)
        hanlded_response = handle_response(response)
        print(f'Ответ от сервера: {response}')
        print(hanlded_response)
    except (ValueError, json.JSONDecodeError):
        print('Ошибка декодирования сообщения')


if __name__ == '__main__':
    main()
