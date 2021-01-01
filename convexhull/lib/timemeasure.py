import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from timeit import default_timer as timer
from typing import Any, Callable
from pprint import pprint
import numpy as np
from lib.getrand import rand_point2_set, rand_rect_points
from pure.graham import graham
from pure.jarvis import jarvis
from pure.increase import increase_with_sorting
from pure.lowerupper import lower_upper
from pure.divide_conq import divide_conq

def get_exec_time(func: Callable, *args) -> float:
    """ Funkcja dokonująca pomiaru czasu działania funkcji func. 
    args - argumenty wywołania funkcji """

    print(func, 'test')
    tstart = timer()
    func(*args)
    tstop = timer()
    return (tstop - tstart)

    
def avg_exec_time(func: Callable, *args, times=1) -> float:
    """ Sredni czas wykonania funkcji func na argumentach args. 
    times -- liczba wywołań """
    
    total_exec_time = 0
    
    points, *adds = args
    
    for _ in range(times):
        total_exec_time += get_exec_time(func, points.copy())
        
    return total_exec_time / times



def exec_time_test(functions: list[Callable], point_generators: list[list[Callable]], args: list[list[Any]], ntests=1):
    exectimes = [ [0] * len(point_generators) for _ in range(len(functions)) ] 
    
    for n, func in enumerate(functions):
        for npg, (pointgenerator, arg) in enumerate(zip(point_generators, args)):
            points = pointgenerator(*arg)
            if func is not jarvis: points = points.tolist()
            if func is divide_conq: 
                exectimes[n][npg] = avg_exec_time(func, points, 3, times=ntests)
                break
            
            exectimes[n][npg] = avg_exec_time(func, points, times=ntests)        
            
    return exectimes
            
            
if __name__ == '__main__':
    funcs = [graham, jarvis, increase_with_sorting, lower_upper, divide_conq]
    pgener = [rand_point2_set, rand_rect_points]
    args = [[500, 0, 10], [100, [[0, 0], [10, 0], [10, 10], [0, 10]]]]
    ntests = 5
    
    exectimes = exec_time_test(funcs, pgener, args, ntests)
    
    pprint(exectimes) 
    
    
    
         
         
            
            