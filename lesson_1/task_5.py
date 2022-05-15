"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""

import chardet
import subprocess

SITES = ['yandex.ru', 'youtube.com']

for site in SITES:
    response = subprocess.Popen(['ping', '-c', '5', site], stdout=subprocess.PIPE)
    for line in response.stdout:
        current_code = chardet.detect(line)['encoding']
        unicode_line = line.decode(current_code).encode('utf-8')
        print(unicode_line.decode('utf-8'), end='')



