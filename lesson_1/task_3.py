"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""

WORDS = ['attribute', 'класс', 'функция', 'type']

WORDS_ERROR = []

for elem in WORDS:
    try:
        elem = bytes(elem, 'ascii')
    except UnicodeEncodeError:
        WORDS_ERROR.append(elem)

print(WORDS_ERROR)
