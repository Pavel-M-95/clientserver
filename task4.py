str = ['разработка', 'администрирование', 'protocol', 'standard']

for i in str:
    a = i.encode('utf-8')
    print(a, type(a))
    b = bytes.decode(a, 'utf-8')
    print(b, type(b))
    print('#' * 30)