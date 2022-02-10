#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Created By  : Dmitriy Aldunin @DMcraft
# Created Date: 08/02/2022
# version ='1.0'
# ---------------------------------------------------------------------------

""" Solving the problem of finding a combination of arithmetic signs

Нахождения возможных вариантов решения задачи на нахождение комбинаций
арифметических знаков между ряда чисел методом перебора.
Задача:
Дана последовательность чисел (1, 2, 3, 4, ...)
Расставить между ними знаки ( +, -, /, *) так, 
чтобы результат вычисления полученного выражения был равен заданному числу

Перечень операторов для генерации числовых выражений:
OPER = ['+', '-', '*', '/', ('#')] (# - знак конкатенации цифр)

"""


# Добавление текущего каталога как источника доп модулей
import sys
sys.path.append ('./') # текущий каталог

# Подключение модулей
from polishparser import *
from progressbar import ProgressBar


__author__ = "Dmitriy Aldunin"
__copyright__ = "Copyright 2022, D. Aldunin"
__credits__ = []
__license__ = "Apache 2.0"
__version__ = "1.0"
__email__ = "DMcraft@ctvi.ru"
__status__ = "Production"


# Начальные условия по умолчанию
FORMULA = "1 2 3 4 5 6 7 8 9 10"
OPERATION = "+ - * / #"
NUMBER_RESULT = "2022"

number_of_formula = FORMULA.split(' ')
operation_of_formula = OPERATION.split(' ')
formula_result = float(NUMBER_RESULT)


def calculate():
    """Основная функция по генерации вариантов числовых выражений 
    их вычисления и проверки на соответствие условиям задачи.
    
    """

    how_many_digits = len(number_of_formula)
    sign_buf = [0] * how_many_digits
    total_found = 0
    how_many_variant = len(operation_of_formula) ** (how_many_digits - 1)

    tik_tak = ProgressBar(how_many_variant)
    current_variant = 0
    while sign_buf[how_many_digits-1] < 1:
        str_formula = ""
        sign_buf[0] += 1
        for n in range(how_many_digits - 1):
            if sign_buf[n] > len(operation_of_formula) - 1:
                sign_buf[n] = 0
                if n < how_many_digits:
                    sign_buf[n + 1] += 1
            str_formula += number_of_formula[n]
            # проверка знака конкатенации цифр 
            if operation_of_formula[sign_buf[n]] != '#':
                str_formula += operation_of_formula[sign_buf[n]]
        str_formula += number_of_formula[how_many_digits - 1]
        # проверка условия выполнения задачи
        if calc(shunting_yard(parse(str_formula))) == formula_result:
            tik_tak.clearbar()
            print(str_formula,end=' = ')
            print(calc(shunting_yard(parse(str_formula))))
            print('  >>', polish_entry(str_formula))
            tik_tak.printbar(current_variant)
            total_found += 1
        # вывод информации о прогрессе вычислений
        current_variant += 1
        tik_tak.printifbar(current_variant)
    tik_tak.printbar(current_variant)
    print('')
    print('Всего найдено числовых выражений: {0}'.format(total_found))


def clear_input(input_string, allow_char):
    """Очистка вводимых данных от посторонних символов
    """

    output_string = ''
    input_string = " ".join(input_string.split())
    for s in input_string:
        if s in allow_char:
            output_string += s
    return output_string


def split_operators(input_string):
    """Формирование набора разрешенных операторов
    
    """

    oper = []
    for o in '+-*/#':
        if o in input_string:
            oper.append(o)
    return oper


def isfloat(value: str) -> bool:
    """Проверка является ли строка числом
    """

    try:
        float(value)
        return True
    except ValueError:
        return False


# MAIN execute
if __name__ == '__main__':
    print('Проверка решения задачи и нахождения возможных вариантов решения методом перебора')
    print('Задача:')
    print('Дана последовательность цифр (1, 2, 3, 4, ...)')
    print('Расставить между ними знаки ( +, -, /, *) так,')
    print('чтобы результат вычисления полученного выражения был равен заданному числу')
    print('Введите последовательность цифр')
    str_temp = clear_input(input('по умолчанию ({}): '.format(FORMULA)),' 123456789.')
    if len(str_temp) > 0:
        number_of_formula = str_temp.split(' ')
    print('Введите перечень используемых операторов, + - * / (# - знак конкатенации цифр)')
    str_temp = clear_input(input('по умолчанию ({}): '.format(OPERATION)), ' +-*/#')
    if len(str_temp) > 0:
        operation_of_formula = split_operators(str_temp)
    print('Введите результат выражения')
    str_temp = clear_input(input('по умолчанию ({}): '.format(NUMBER_RESULT)), '.1234567890')
    if isfloat(str_temp):
        formula_result = float(str_temp)

    print(f'\nНачало поиска решения числовых выражений при которых результат равен {formula_result}')
    print('Используется последовательность чисел:', ' '.join(number_of_formula))
    print('Операторы участвующие в подборе:', ' '.join(operation_of_formula))

    calculate()

    input('Завершить работу... (Enter)')
