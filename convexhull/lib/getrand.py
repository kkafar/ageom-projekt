""" Moduł dostarczający funkcji generujących zbiory / wartości losowe """

import numpy as np
from typing import Tuple
from numpy import random

def dist(point_a, point_b):
    return np.sqrt((point_a[0] - point_b[0])** 2 + (point_a[1] - point_b[1])**2)

def rand_seg_point(point_a, point_b):
    """ Zwraca losowy punkt leżący na odcinku point_a, point_b """     
    
    rng = np.random.default_rng()
    
    point = np.empty(shape=2)
    
    # jeżeli odcinek jest pionowy to generujemy tylko rzędną punktu
    if point_a[0] == point_b[0]:
        min_y = min(point_a[1], point_b[1])
        max_y = max(point_a[1], point_b[1])
        point[0] = point_a[0]
        point[1] = rng.random() * (max_y - min_y) + min_y
        
    else:
        min_x = min(point_a[0], point_b[0])
        max_x = max(point_a[0], point_b[0])
        
        a = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
        b = (point_a[1] - a * point_a[0])
        
        param_t = rng.random() * (max_x - min_x) + min_x
        point[0] = param_t
        point[1] = a * param_t + b
         
    return point
        

def rand_rect_points(n: int, vertices):
    """ Zwraca tablicę n par [a, b] będących punktami leżącymi na bokach prostokąta o zadanych wierzchołkach\n
    n -- liczba punktów\n
    vertices -- lista/tablica wierzchołków w USTALONEJ KOLEJNOŚCI.\n
    Jeżeli podajemy vertices=[A, B, C, D] to AB, BC, CD, DA są bokami prostokąta oraz AB równoległe do CD
    i BC równoległe DA"""
    rng = np.random.default_rng()
    A, B, C, D = vertices[0], vertices[1], vertices[2], vertices[3]
    len_AB = dist(A, B)
    len_BC = dist(B, C)
    
    points = np.empty(shape=(n,2))
    
    for i in range(n):
        side = rng.random(1) * 2 * (len_AB + len_BC)
    
        if side < len_BC:
            points[i] = rand_seg_point(A, D)
        elif side < 2 * len_BC:
            points[i] = rand_seg_point(B, C)
        elif side < 2 * len_BC + len_AB:
            points[i] = rand_seg_point(A, B)
        else:
            points[i] = rand_seg_point(C, D)
    
    return points
    

#################################################################################
def rand_in_range(  low: float = 0, 
                    high: float = 0, 
                    data_type: str = 'float64') -> np.array:
    rng = random.default_rng()

    return np.array((rng.random(1) * (high - low) + low), dtype=data_type)
#################################################################################


#################################################################################
def rand_arr(n: int, 
            low: float, 
            high: float, 
            data_type: str = 'float64') -> np.array:
    """ Zwraca tablicę (np.array) n liczb losowych (data_type) z zakresu [low, high) """

    rg = np.random.default_rng()

    return np.array( (rg.random(n) * (high - low) + low), dtype=data_type)
#################################################################################


#################################################################################
def rand_point2_set(n: int, 
                    low: float = 0, 
                    high: float = 1, 
                    data_type: str = 'float64') -> np.array:
    """ Zwraca tablicę tablic [x, y] nlosowych punktów o współrzędnych z zakresu [low; high) """
    # rng = np.random.default_rng()
    return np.array(np.random.random((n, 2)) * (high - low) + low, dtype=data_type)
    # return np.array( list( zip( rng.random(n) * (high - low) + low, rng.random(n) * (high - low) + low  ) ) )
    # return np.array( [ [ rng.random() * (high - low) + low, rng.random() * (high - low) + low ] for _ in range(n) ] )
#################################################################################
# def rand_vector2(n: int = 1, low_x: float = 0, high_x: float = 1, low_y: float = 0, high_y: float = 1) -> np.array:
#     return np.full(n, Vector2(rand_in_range(low_x, high_x), rand_in_range(low_y, high_y), dtype=Vector2))
#################################################################################


#################################################################################
def rand_circle_points( n: int = 10,
                        x: float = 0, 
                        y: float = 0, 
                        r: float = 1, 
                        data_type: str = 'float64') -> np.array:
    """ Zwraca tablicę par [a, b] będących współrzędnymi n punktów, na okręgu o środku w [x, y] i promieniu r """
    rng = np.random.default_rng()

    circle = np.empty(n * 2, dtype=data_type).reshape(n, 2)

    for i in range(n):
        rn = rng.random() * 2 * np.pi
        circle[i][0] = r * np.cos(rn) + x
        circle[i][1] = r * np.sin(rn) + y

    return circle
#################################################################################


