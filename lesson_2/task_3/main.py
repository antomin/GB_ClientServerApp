"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import yaml

DATA = {
    'items': ['Printer', 'Scaner', 'Компьютер'],
    'all_quantity': 3,
    'price': {
        'dollars': '1000$',
        'euro': '947€',
        'rubles': '62000₽'
    }
}


def save_to_yaml(new_data):
    with open('file.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(new_data, file, allow_unicode=True, default_flow_style=False)


def check_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    print(data == DATA)


save_to_yaml(DATA)
check_file('file.yaml')
