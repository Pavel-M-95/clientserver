import locale

resurs_string = ['сетевое программирование', 'сокет', 'декоратор']

with open('resurs.txt', 'w+') as f_n:
    for i in resurs_string:
        f_n.write(i + '\n')
    f_n.seek(0)

print(f_n) # печатаем объект файла, что бы узнать его кодировку

file_coding = locale.getpreferredencoding()

# Читаем из файла
with open('resurs.txt', 'r', encoding=file_coding) as f_n:
    for i in f_n:
        print(i)

    f_n.seek(0)