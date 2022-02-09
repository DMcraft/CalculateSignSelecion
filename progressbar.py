#!/usr/bin/env python
#----------------------------------------------------------------------------
# Created By  : Dmitriy Aldunin @DMcraft
# Created Date: 08/02/2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" Progress Bar for use in command line

Модуль содержит класс ProgressBar(), осуществляющий вывод информации о
ходы выполнения процесса.

"""

from time import time

# Строка выполнения
class ProgressBar():
    """ Progress Bar for use in command line

    На вход подается информация о полном ожидаемом количестве условных единиц,
    количество которых принимается за 100%. Фиксируется время начала процесса, поэтому
    для точного определения оставшегося времени, рекомендуется инициализировать объект
    перед непосредственным началом измеряемого процесса.

    """
    __DELAYMID = 0.7

    def __init__(self, status_full: int) -> None:
        self.__status_full = status_full
        self.__time_start_stamp = time()
        self.__time_print = 0.0 # type:float

    def printbar(self, status: int):
        """Вывод информации о ходе выполнения процесса.
        
        На вход подается информация о киличестве выполенных условных единиц. 

        """
        
        n_status = 20 
        procent_status = 100
        time_todo = time() - self.__time_start_stamp
        time_left = time_todo / (1 if status == 0 else status) * self.__status_full
        print('Выполнение [', end='')
        if status < self.__status_full:
            n_status = int(20.0 / self.__status_full * status)
            procent_status = int(100.0 / self.__status_full * status)
        print('#' * n_status, '-' * (20 - n_status), sep='>', end='')
        print(f'] {procent_status:0>3}% ({status}/{self.__status_full}) [{time_todo:.1f}/{time_left:.1f} сек.]', end='\r')
        self.__time_print = time()

    def printifbar(self,status: int):
        """ Вывод информации о ходе выполнения процесса, не чаще определенного интервала времени  

        На вход подается информация о киличестве выполенных условных единиц.  

        """

        if self.__time_print + self.__DELAYMID < time():
            self.printbar(status)


    def clearbar(self):
        """Очистка текущей строки терминала
        """

        print('\r', ' ' * 79, '\r', sep='', end='')


    def __str__(self):
        return f"ProgressBar start {time() - self.__time_start_stamp} seconds ago,  with {self.__status_full} full point"