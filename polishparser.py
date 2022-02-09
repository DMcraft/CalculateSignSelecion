#!/usr/bin/env python
#----------------------------------------------------------------------------
# Created By  : Anton Grigoryev @griganton
# Credits: Dmitriy Aldunin @DMcraft
# ---------------------------------------------------------------------------
"""Calculation by the Reverse Polish notation method

Вычисление формулы методом обратной польской нотации
на основе кода автора "Антон Григорьев @griganton"
Источник https://habr.com/ru/post/273253/

"""

import operator

OPERATORS = {'+': (1, operator.add), '-': (1, operator.sub),
             '*': (2, operator.mul), '/': (2, operator.truediv)}


def parse(formula_string: str):
    """Парсер исходной строки (генератор)

    получает на вход строку, возвращает числа в формате float, операторы и скобки в формате str

    """

    number = ''
    for s in formula_string:
        if s in '1234567890.': # если символ - цифра, то собираем число
            number += s  
        elif number: # если символ не цифра, то выдаём собранное число и начинаем собирать заново
            yield float(number) 
            number = ''
        if s in OPERATORS or s in "()": # если символ - оператор или скобка, то выдаём как есть
            yield s 
    if number:  # если в конце строки есть число, выдаём его
        yield float(number)


def shunting_yard(parsed_formula):
    """Алгоритм сортировочной станции (генератор)
    
    получает на вход итерируемый объект из чисел и операторов в инфиксной нотации, 
    возвращает числа и операторы в обратной польской записи.

    """

    stack = []  # в качестве стэка используем список
    for token in parsed_formula:
        # если элемент - оператор, то отправляем дальше все операторы из стека, 
        # чей приоритет больше или равен пришедшему,
        # до открывающей скобки или опустошения стека.
        # здесь мы пользуемся тем, что все операторы право-ассоциативны
        if token in OPERATORS: 
            while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                yield stack.pop()
            stack.append(token)
        elif token == ")":
            # если элемент - закрывающая скобка, выдаём все элементы из стека, до открывающей скобки,
            # а открывающую скобку выкидываем из стека.
            while stack:
                x = stack.pop()
                if x == "(":
                    break
                yield x
        elif token == "(":
            # если элемент - открывающая скобка, просто положим её в стек
            stack.append(token)
        else:
            # иначе делаем вывод, что элемент - число, отправим его сразу на выход
            # необходимость прямой проверки, что это число, под ?
            yield token
    while stack:
        yield stack.pop()


#   
#   Функция, получает на вход итерируемый объект чисел и операторов в обратной польской нотации,
#   возвращает результат вычисления:
def calc(polish):
    """Вычислитель 
    
    Функция, получает на вход итерируемый объект чисел и операторов в обратной польской нотации,
    возвращает результат вычисления.

    """

    stack = []
    for token in polish:
        #print(token,end=" ")
        if token in OPERATORS:  # если приходящий элемент - оператор,
            y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
            stack.append(OPERATORS[token][1](x, y)) # вычисляем оператор, возвращаем в стек
        else:
            stack.append(token)
    return stack[0] # результат вычисления - единственный элемент в стеке        


def polish_entry(formula_string: str) -> str:
    """Сборка обратной польской нотации
    """

    str_polsk = ''
    for s in shunting_yard(parse(formula_string)):
        str_polsk += str(s) + ' '
    return str_polsk


def eval_(formula):
    """Вычислитель арифметического выражения
    """

    return calc(shunting_yard(parse(formula)))


#   Выполнение программы с запросом из терминала
if __name__ == '__main__':
    print('Вычисление выражения с разложением в обратную польскую нотацию')
    print('учитываются операторы (+, -, /, *)')
    str_formula = input('Введите числовое выражение: ')
    print('Обратная польская нотация:')
    print(polish_entry(str_formula), ' = ', eval_(str_formula))