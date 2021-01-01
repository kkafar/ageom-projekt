""" K. Kafara """

import json
import simplejson
from typing import Literal, Union
from lib.mytypes import ListOfPoints, ListOfSegments, Point, Segment
from random import randint
import matplotlib.colors as mcolors
import math
import numpy as np



def eq_eps(value: float, expected: float, eps: float = 1e-7) -> bool:
    """ == co do eps """
    return (value > expected - eps and value < expected + eps)

def le_eps(value: float, expected: float, eps: float = 1e-7) -> bool:
    "<= co do epsilonu"
    return (value < expected + eps)

def ge_eps(value: float, expected: float, eps: float = 1e-7) -> bool:
    ">= z dokladoscia do eps"
    return (value > expected - eps)


# Posługujemy się tym wyznacznikiem bazując na doświadczeniu z zad. 1 (poradził sobie najlepiej)
def det3x3( ux, uy, uz,
            vx, vy, vz,
            wx, wy, wz) -> float:
    """ Zwraca wyznacznik 3x3 obliczony metodą Sarussa (bez redukcji wyrazów) """
    return (ux * vy * wz) + (uy * vz * wx) + (uz * vx * wy) - (wx * vy * uz) - (wy * vz * ux) - (wz * vx * uy)


def orientation(p1: Point, p2: Point, p3: Point, eps: float = 1e-7) -> Literal[-1, 0, 1]:
    """ Zwraca\n
    -1 <- jeśli p3 znajdue się po prawej stronie (p1, p2)\n
    0 <- jesli p3 jest współliniowy z (p1, p2)\n
    1 <- jeśli p3 znajduje się po lewej stronie (p1, p2)\n
    eps <- tolerancja dla zera
    """
    det = det3x3(p1[0], p1[1], 1,
                 p2[0], p2[1], 1,
                 p3[0], p3[1], 1)
    if det < -eps:
        return -1
    elif det < eps:
        return 0
    else:
        return 1

        
def save_segments_to_json(path: str, lines: ListOfSegments, indent: int = None) -> None:
    with open(path, 'w') as file: 
        json.dump(lines, file, indent=indent)


def read_segments_from_json(path: str) -> ListOfSegments:
    with open(path, 'r') as file:
        return json.load(file)
    
    
def save_points_to_json(path: str, points: ListOfPoints, indent: int = None) -> None:
    with open(path, 'w') as file:
        file.write(simplejson.dumps(points, indent = indent)) 
    

def load_points_from_json(path: str) -> None:
    with open(path, 'r') as file:
        return simplejson.load(file)
        
    
def intersection(segment1: Segment, segment2: Segment, eps: float = 1e-9) -> Union[Point, None]:
    """ Sprawdza czy 2 odcinki się przecinają. Jeżeli tak to zwraca punkt przecięcia. 
    Podzane odcinki nie mogą przecinać się w więcej niż 1 punkcie. """

    denom = (segment1[0][1] - segment1[1][1]) * (segment2[1][0] - segment2[0][0]) - (segment1[1][0] - segment1[0][0]) * (segment2[0][1] - segment2[1][1])
    # print(f'denom: ({segment1[0][1]} - {segment1[1][1]}) * ({segment2[1][0]} - {segment2[0][0]}) - ({segment1[1][0]} - {segment1[0][0]}) * ({segment2[0][1]} - {segment2[1][1]})')
    # odcinki są równoległe
    if denom > -eps and denom < eps: return None

    numer = (segment1[0][1] - segment2[0][1]) * (segment2[1][0] - segment2[0][0]) + (segment1[0][0] - segment2[0][0]) * (segment2[0][1] - segment2[1][1])

    param_t = numer / denom 
    param_u = ((1 - param_t) * segment1[0][0] + param_t * segment1[1][0] - segment2[0][0]) / (segment2[1][0] - segment2[0][0])

    if (param_t > -eps and param_t < 1 + eps) and (param_u > -eps and param_u < 1 + eps):
        # print(f'intersection: t: {param_t}, u: {param_u}, numer: {numer}, denom: {denom}, segments:\n{segment1}\n{segment2}')
        return [(1 - param_t) * segment1[0][0] + param_t * segment1[1][0], (1 - param_t) * segment1[0][1] + param_t * segment1[1][1]]
    else:
        return None


def intersection_with_sweep(segment: Segment, sweep_y: float, eps: float = 1e-7) -> Union[Point, None]:
    """ Sprawdza przecięcie odcinka (niepoziomego) z poziomą prostą y = sweep_y """
    if eq_eps(segment[0][1], sweep_y, eps=1e-3):
        return segment[0]
    elif eq_eps(segment[1][1], sweep_y, eps=1e-3):
        return segment[1]

    denom = segment[1][1] - segment[0][1]

    if denom > -eps and denom < eps:
        return None      # odcinek jest poziomy, nie rozważamy takich

    param_t = (sweep_y - segment[0][1]) / denom

    if param_t > -eps and param_t < 1 + eps:
        return [(1-param_t) * segment[0][0] + param_t * segment[1][0], sweep_y]
    
    else:
        return None

        
        
def index_of_min(points: list[Point], cmp_idx = 0) -> Union[int, None]:
    """ Zwraca indeks pod którym znajduje się minimum zbioru danych. cmp_idx - indeks
    po którym mają być porównywane punkty."""

    if len(points) < 1 or cmp_idx < 0 or cmp_idx > 1: return None

    min_el = points[0]
    min_idx = 0

    for i in range(1, len(points)):
        if  points[i][cmp_idx] < min_el[cmp_idx] \
            or \
            points[i][cmp_idx] == min_el[cmp_idx] and points[i][1 - cmp_idx] < min_el[1 - cmp_idx]:
                
            min_el = points[i]
            min_idx = i
        
    return min_idx


def index_of_max(points: list[Point], cmp_idx = 0) -> Union[int, None]:
    """ Zwraca indeks pod którym znajduje się maksimum zbioru danych. cmp_idx - indeks
    po którym mają być porównywane punkty. """

    if len(points) < 1 or cmp_idx < 0 or cmp_idx > 1: return None
    
    max_el = points[0]  
    max_idx = 0
    
    for i in range(1, len(points)):
        if  points[i][cmp_idx] > max_el[cmp_idx] \
            or \
            points[i][cmp_idx] == max_el[cmp_idx] and points[i][1 - cmp_idx] > max_el[1 - cmp_idx]:
                
            max_el = points[i]
            max_idx = i
            
    return max_idx


def dist_sq(p1, p2):
    """ Zwraca kwadrat odległości pom. dwoma punktami"""
    return (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2

def swap_points(p, q):
    """ Zamienia współrzędne dwóch punktów """
    p[0], p[1], q[0], q[1] = q[0], q[1], p[0], p[1]

    
    
def divide(points,m): #dzieli zbior punktow na w miarae rowne podzbiory o rozmiarze m lub m-1
    n=len(points)
    for i in range(1,n):#gwarantuje, ze w pierwszym zbiorze Qi pierwszy element jest najnizszy, czyli nalezy do otoczki ostatecznej
        if points[i][1] < points[0][1]:
            buf=points[i]
            points[i] = points[0]
            points[0]=buf
            
    k=math.ceil(n/m)
    Q=[[] for i in range(k)]
    i=0
    while i<n:
        for j in range(k):
            if i==n:
                break
            Q[j].append(points[i])
            i+=1
    if len(Q[0]) > m:
        return None
            
    return Q

def makeSheaf(Points): #laczy punkty w kolejnosci jakiej sa podane
    Sheaf=[]
    for i in range(len(Points)-1):
        Sheaf.append([Points[i],Points[i+1]])
    return Sheaf

def makeFullSheaf(Points): #laczy punkty w kolejnosci jakiej sa podane, dodatkowo domyka cylk
    Sheaf=[]
    for i in range(len(Points)-1):
        Sheaf.append([Points[i],Points[i+1]])
    Sheaf.append([Points[len(Points)-1],Points[0]])
    return Sheaf

def length(v):
     return np.sqrt((v[1][0]-v[0][0])**2+(v[1][1]-v[0][1])**2)

def det(a,b,c):
    return a[0]*b[1]-a[0]*c[1]-b[0]*a[1]+b[0]*c[1]+c[0]*a[1]-c[0]*b[1]

def tangent(p, Q, accur=0):  # Q-zbior punktow w formie otoczki
    # wykorzystujemy binary search na otoczce - jesli dany wierzcholek jest po prawej stronie punktu tworzacej styczna
    # lewostronna z p, 
    ln = len(Q)

    def tangetUtil(p, Q, l, r):
        if r < l:  # zdarza sie tylko, gdy punkt jest wewnatrz otoczki
            return None

        mid = (l + r) // 2
        if det(Q[0], Q[1], p) > 0 and det(Q[ln - 1], Q[0], p) > 0:
            if (det(Q[0], p, Q[mid]) < 0) or (det(p, Q[mid], Q[(mid + 1) % ln]) < 0 and \
                                              det(p, Q[mid], Q[(mid - 1) % ln]) < 0) or \
                    (det(p, Q[mid], Q[(mid + 1) % ln]) < 0 and det(p, Q[mid], Q[(mid - 1) % ln]) >= 0):
                return tangetUtil(p, Q, mid + 1, r)

        else:
            if det(Q[0], p, Q[mid]) >= 0 and \
                    ((det(p, Q[mid], Q[(mid + 1) % ln]) < 0 and det(p, Q[mid], Q[(mid - 1) % ln]) >= 0) or \
                     (det(p, Q[mid], Q[(mid + 1) % ln]) < 0 and det(p, Q[mid], Q[
                         (mid - 1) % ln]) < 0)):  # chyba nie potrzebne sprawdz na koncu
                return tangetUtil(p, Q, mid + 1, r)

        if det(p, Q[mid], Q[(mid + 1) % ln]) >= 0 and det(p, Q[mid], Q[(mid - 1) % ln]) >= 0 \
                or (det(p, Q[mid], Q[(mid + 1) % ln]) == 0 and (Q[mid][0] <= p[0] <= Q[(mid + 1) % ln][0]) and \
                    (Q[mid][1] <= p[1] <= Q[(mid + 1) % ln][1])):

            while (det(p, Q[mid], Q[(mid + 1) % ln]) == 0):
                mid = (mid + 1) % ln  # jesli jest styczna wspolliniowa, to bierzmy pod uwage punkt blizszy
            return mid

        else:
            return tangetUtil(p, Q, l, mid - 1)

    
    return tangetUtil(p, Q, 0, ln - 1)

def randomColor():
    return list(mcolors.CSS4_COLORS)[randint(0,len(list(mcolors.CSS4_COLORS))-1)]


def compr(p,q,current,accur=10**(-6)):#jezeli p jest po prawej  odcinka [current,q] - jest 'wiekszy', to zwracamy 1
        if det(current,p,q)>accur:
            return -1
        elif det(current,p,q)<accur:
            return 1
        else:
            return 0
        