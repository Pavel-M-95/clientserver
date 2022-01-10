'''Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе'''


var = [b'attribute', b'класс', b'функция'  b'type']

for i in var:
    print(type(i))

# строки записанные на кириллице не распознаются

"""
  File "C:\Users\User\Desktop\Python\lesson\task3.py", line 5
    var = [b'attribute', b'класс', b'функция'  b'type']
                                      ^
SyntaxError: bytes can only contain ASCII literal characters

"""
