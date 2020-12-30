import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from random import randint
from typing import Callable
from lib.stack import Stack


def partition_cmp(arr: list, p: int, q: int, cmp: Callable = lambda x, y: x <= y) -> int: 
    """ Modyfikuje arr w miejscu. cmp powinien implementować <= dla elementów arr """

    i = p - 1
    
    pivot_idx = randint(p, q)
    pivot = arr[pivot_idx]
    
    # zamieniamy miejscami pivot z ostatnim elementem
    arr[pivot_idx], arr[q] = arr[q], arr[pivot_idx]

    for j in range(p, q):
        if cmp(arr[j], pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    arr[i + 1], arr[q] = arr[q], arr[i + 1]
    
    return i + 1
            
            
def qsort_iterative(arr: list, cmp: Callable = lambda x, y: x <= y):
    stack = Stack(len(arr))
    
    stack.push(0)
    stack.push(len(arr) - 1)
    
    while not stack.is_empty():
        q = stack.top()
        stack.pop()

        p = stack.top()
        stack.pop()
        
        pivot_idx = partition_cmp(arr, p, q, cmp=cmp)
        
        if pivot_idx - 1 > p:
            stack.push(p)
            stack.push(pivot_idx - 1)
            
        if pivot_idx + 1 < q:
            stack.push(pivot_idx + 1)
            stack.push(q)

            
            
if __name__ == '__main__':
    arr = [ i for i in range(10) ]
    arr.reverse()
    
    print(arr)
    
    # pivot_idx = partition_cmp(arr, 0, 9, lambda x, y: x <= y)
    
    # print(arr)
    # print(pivot_idx)
    
    
    qsort_iterative(arr)
    
    print(arr)
    