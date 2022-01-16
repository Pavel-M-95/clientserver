import json
import time


class JSONMessageEncoder(json.JSONEncoder):
    """
    Собственный JSONEncoder расширяющий стандартный JSONEncoder,
    необходим для закодирования пользовательских объектов в формат,
    сериализуемый в JSON
    """
    def default(self, obj):
        return obj.__dict__


class MessageBuilder:
    """
    Класс описывающий фабричные методы, генерирующие соответствующие сообщения
    """
    def __init__(self, msg):
        """
        Генерируем сообщение из словаря в зависимости от любого количества элементов
        """
        for key, val in msg.items():
            if isinstance(val, dict):
                sub_val = MessageBuilder(val)
                setattr(self, key, sub_val)
            else:
                setattr(self, key, val)

    def encode_to_json(self):
        """
        Кодируем объект в json
        :return: json представление MessageBuilder
        """
        return JSONMessageEncoder().encode(self)

    @staticmethod
    def get_object_of_json(json_obj):
        """
        Декодируем из json в MessageBuilder
        :return: presence message (type = MessageBuilder)
        """
        return json.JSONDecoder(object_hook=MessageBuilder).decode(json_obj)

    @staticmethod
    def create_presence_message(name, time=time.ctime()):
        """
        Формирует сообщение о присутствии(presence message)
        :param name: Имя пользователя
        :param time: время, по умолчанию текущее.
        :return: presence message (type = MessageBuilder)
        """
        return MessageBuilder({"action": "presence", "time": time,
                               "user":
                                   {"name": name,
                                    "status": "here"}})

    @staticmethod
    def create_response_message(code, alert=None):
        """
        Формирует сообщение ответа сервера (response message)
        :param code: Код ответа
        :param alert: Дополнительный параметр "уведомление"
        :return: response message (type = MessageBuilder)
        """
        return MessageBuilder({"response": code, "alert": alert})


if __name__ =='__main__':
    # ПРИМЕР ИСПОЛЬЗОВАНИЯ
    msg = MessageBuilder({"response": 200, "alert": "default"})
    name = "User123"
    msg2 = MessageBuilder(
        {"action": "presence", "time": time.ctime(), "user": {"name": name, "status": "here"}})
    msg3 = MessageBuilder.create_presence_message(name="newUser")
    msg4 = MessageBuilder.create_response_message(200, "default")

    # Выводим в json файлы чисто для примера, на практике смысла в этом особо нет
    with open('msg.json', 'w') as outfile:
        json.dump(msg.__dict__, outfile)  # msg.__dict__ - Применимо только к простым объектам
    with open('msg2.json', 'w') as outfile:
        json.dump(JSONMessageEncoder().encode(msg2), outfile)
    with open('msg3.json', 'w') as outfile:
        json.dump(JSONMessageEncoder().encode(msg3), outfile)
    with open('msg4.json', 'w') as outfile:
        json.dump(JSONMessageEncoder().encode(msg4), outfile)
    # Декодируем сообщение из json обратно в
    json_exemple_msg = JSONMessageEncoder().encode(msg2)
    decoded_obj = json.JSONDecoder(object_hook=MessageBuilder).decode(json_exemple_msg)
    # можем обратиться по нужным атрибутам
    print(decoded_obj.action)