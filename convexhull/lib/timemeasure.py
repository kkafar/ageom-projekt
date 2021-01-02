import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from timeit import default_timer as timer
from typing import Any, Callable, List
from pprint import pprint
import numpy as np


def get_exec_time(func: Callable, *args, points = []) -> float:
    """ Funkcja dokonująca pomiaru czasu działania funkcji func. 
    args - argumenty wywołania funkcji """

    tstart = timer()
    func(points, *args)
    tstop = timer()
    return (tstop - tstart)

    
def avg_exec_time(func: Callable, *args, points = [], times = 1) -> float:
    """ Sredni czas wykonania funkcji func na argumentach args. 
    times -- liczba wywołań """
    
    total_exec_time = 0
    
    for _ in range(times):
        points_copy = points.copy()
        total_exec_time += get_exec_time(func, *args, points = points_copy)
        
    return total_exec_time / times