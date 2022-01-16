import os
import sys
import json


def load_config(is_server=True):
    config_keys = [
        'DEFAULT_PORT',
        'MAX_CONNECTIONS',
        'MAX_PACKAGE_LENGTH',
        'ENCODING',
        'ACTION',
        'TIME',
        'USER',
        'ACCOUNT_NAME',
        'PRESENCE',
        'RESPONSE',
        'ERROR'
    ]

    if not is_server:
        config_keys.append('DEFAULT_IP_ADDRESS')
    if not os.path.exists('config.json'):
        print('Конфигурация отсутствует')
        sys.exit(1)
    with open('config.json') as config:
        CONFIGS = json.load(config)
    loaded_configs_keys = list(CONFIGS.keys())
    for key in config_keys:
        if key not in loaded_configs_keys:
            print(f'Ключ в файле конфигурации отстутвует: {key}')
            sys.exit(1)
    return CONFIGS


def send_message(opened_socket, message, CONFIGS):
    json_message = json.dumps(message)
    response = json_message.encode(CONFIGS.get('ENCODING'))
    opened_socket.send(response)


def get_message(opened_socket, CONFIGS):
    response = opened_socket.recv(CONFIGS.get('MAX_PACKAGE_LENGTH'))
    if isinstance(response, bytes):
        json_response = response.decode(CONFIGS.get('ENCODING'))
        response_dict = json.loads(json_response)
        if isinstance(response_dict, dict):
            return response_dict
        raise ValueError
    raise ValueError

