import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")


from typing import Callable, overload
from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint
from lib.stack import Stack
from lib.sorting import qsort_iterative



def get_point_cmp(ref_point: Point, eps: float = 1e-7) -> Callable:
    def point_cmp(point1, point2):
        orient = orientation(ref_point, point1, point2, eps)
        
        # jeżeli punkt point2, leży po prawej stronie odcinka (ref_point, point1) to point2 _le_ point1 ==> False
        if orient == -1:
            return False
        elif orient == 1:
            return True
        elif dist_sq(ref_point, point1) <= dist_sq(ref_point, point2):
            return True
        else:
            return False

    return point_cmp


def graham(points: ListOfPoints) -> ListOfPoints:
    """ points - lista/tablica punktów (modyfikuje ją w trakcie!) """
    
    # znajdujemy indeks punktu o najmniejszej rzędnej (jeżeli jest wiele - 
    # to bierzemy ten z nich o najmniejszej odciętej)
    istart = index_of_min(points, 1)

    # wierzchołek poczatkowy umieszczamy na pierwszej pozycji w tablicy
    points[istart], points[0] = points[0], points[istart]    

    

    # sortujemy punkty względem kąta skierowanego jaki tworzy wektor (points[i] - points[istart])
    # Jeżeli jakieś 2 tworzą ten sam kąt ==> to mniejszy jest ten znajdujący się bliżej points[0]
    # wykorzystywane jest to poniżej 
    qsort_iterative(points, get_point_cmp(points[0]))

    # Usuwamy punkty o równych kątach
    # Działa to tak, że iterujemy po całej tablicy, przepisując 'unikalne' punkty na początek tablicy. 
    # W dalszej części algorytmu rozważamy tylko początkoy fragment tablicy zawierający punkty unikalne.
    i, new_size = 1, 1
    while i < len(points):
        # jeżeli kolejne punkty są współliniowe to pomijamy je tak długo, aż dojdziemy do ostatniego z nich
        while (i < len(points) - 1) and (orientation(points[0],
                                                          points[i],
                                                          points[i + 1], 1e-7) == 0):  
            i += 1
        
        # bierzemy ostatni z tych o równym kącie (dzięki odpowiedniemu komparatorowi w qsort jest on
        # położony najdalej w tablicy
        points[new_size] = points[i]
        new_size += 1
        i += 1
    
    
    # dodajemy pierwsze 3 punkty na stos (wiemy, że pierwsze 2 należą do otoczki)
    s = Stack()
    s.push(points[0])
    s.push(points[1])
    s.push(points[2])
    
    for i in range(3, new_size, 1):
        # jeżeli jest po lewej to dodajmey go na stos
        while orientation(s.sec(), s.top(), points[i], 1e-7) != 1:
            s.pop()

        s.push(points[i])

    return s.s[:s.itop+1]

    
    
if __name__ == '__main__': 
    points = rand_point2_set(10000, 0, 10).tolist()
    
    pprint(points)
    
    print('--' * 10)
    
    convex_hull = graham(points)
    
    pprint(convex_hull)

    plot = Plot(scenes=[Scene(
        points=[
            PointsCollection(points),
            PointsCollection(convex_hull, color='r', marker='s')
        ],
        lines=[
            LinesCollection([
                [ convex_hull[i], convex_hull[(i+1) % len(convex_hull)] ]
                for i in range(len(convex_hull))
            ], linestyle='--', color='r')
        ]
    )])
    
    plot.draw()

    
    
    
    