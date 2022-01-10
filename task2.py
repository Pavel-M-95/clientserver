'''Каждое из слов «class», «function», «method» записать в байтовом типе
 без преобразования в последовательность кодов
 (не используя методы encode и decode) и определить тип, содержимое и длину
  соответствующих переменных.
'''
var = [b'class', b'function', b'method']

for line in var:
    print(40 * '#')
    print('тип переменной: {}\n'.format(type(line)))
    print('содержание переменной - {}\n'.format(line))
    print('длинна строки: {}\n'.format(len(line)))
