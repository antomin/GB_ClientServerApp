"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы, Название ОС, Код продукта, Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

import csv
import re

FILES = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def get_data(files_lst: list) -> list:
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    for file in files_lst:
        with open(file, 'r', encoding='utf-8') as current_file:
            file_read = current_file.read()
            os_prod_list.append(re.search(r'(?<=Изготовитель системы:).*', file_read).group().strip())
            os_name_list.append(re.search(r'(?<=Название ОС:).*', file_read).group().strip())
            os_code_list.append(re.search(r'(?<=Код продукта:).*', file_read).group().strip())
            os_type_list.append(re.search(r'(?<=Тип системы:).*', file_read).group().strip())

    for idx in range(0, len(FILES)):
        main_data.append([idx + 1, os_prod_list[idx], os_name_list[idx], os_code_list[idx], os_type_list[idx]])

    return main_data


def write_to_csv(new_csv: str):
    with open(new_csv, 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file)
        file_writer.writerows(get_data(FILES))


write_to_csv('data_report.csv')
