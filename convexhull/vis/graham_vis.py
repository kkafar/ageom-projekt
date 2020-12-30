import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")


from typing import Callable
from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint
from lib.stack import Stack
from lib.sorting import qsort_iterative
import operator 



def get_point_cmp(ref_point: Point, eps: float = 1e-7) -> Callable:
    def point_cmp(point1, point2):
        orient = orientation(ref_point, point1, point2, eps)
        
        # jeżeli punkt q, leży po prawej stronie odcinka (p0, p) to q _le_ p ==> return True
        if orient == -1:
            return False
        elif orient == 1:
            return True
        elif dist_sq(ref_point, point1) <= dist_sq(ref_point, point2):
            return True
        else:
            return False

    return point_cmp


def graham_vis(points):
    """ points - lista/tablica punktów (modyfikuje ją w trakcie!) """
    
    plot = Plot(scenes=[Scene(points=[PointsCollection(np.copy(points), marker='.')])])
    linestack = Stack()
    
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
    # dzielimy przez 2, bo każdy punkt wnosi 2 do rozmiaru tablicy (np.array)
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
    
    linestack.push([points[0], points[1]])
    linestack.push([points[1], points[2]])
    
    
    for i in range(3, new_size, 1):
        plot.add_scene(Scene(points=[PointsCollection(points[:new_size], marker='.'),
                                    PointsCollection(s.s[:s.itop], color='r', marker='s'),
                                    PointsCollection([s.top()], color='green', marker='s'),
                                    PointsCollection([points[i]], color='indigo', marker='x')],
                            lines=[LinesCollection(linestack.s[:linestack.itop], color='red'),
                                    LinesCollection([linestack.top()], color='green'),
                                    LinesCollection([[s.top(), points[i]]], color='indigo', linestyle='--')]))
            
        # jeżeli jest po lewej to dodajmey go na stos
        while orientation(s.sec(), s.top(), points[i], 1e-7) != 1:
            s.pop()
                
            linestack.pop()
            plot.add_scene(Scene(points=[PointsCollection(points[:new_size], marker='.'),
                                        PointsCollection(s.s[:s.itop], color='r', marker='s'),
                                        PointsCollection([s.top()], color='green', marker='s'),
                                        PointsCollection([points[i]], color='indigo', marker='x')],
                                lines=[LinesCollection(linestack.s[:linestack.itop], color='r'),
                                        LinesCollection([linestack.top()], color='green'),
                                        LinesCollection([[s.top(), points[i]]], color='indigo', linestyle='--')]))

        s.push(points[i])
        linestack.push([s.sec(), s.top()])
        plot.add_scene(Scene(points=[PointsCollection(points[:new_size], marker='.'),
                                    PointsCollection(s.s[:s.itop], color='r', marker='s'),
                                    PointsCollection([s.top()], color='green', marker='s')],
                            lines=[LinesCollection(linestack.s[:linestack.itop], color='r'),
                                    LinesCollection([linestack.top()], color='green')]))
        
    linestack.push([s.top(), points[0]])
    plot.add_scene(Scene(points=[PointsCollection(points[:new_size], marker='.'),
                                    PointsCollection(s.s[:s.itop+1], color='r', marker='s')],
                        lines=[LinesCollection(linestack.s[:linestack.itop+1], color='r')]))
    plot.scenes.insert(0, Scene(points=[PointsCollection(np.copy(points[:new_size]), marker='.'),
                                        PointsCollection(s.s[:s.itop+1], color='r', marker='s')],
                                lines=[LinesCollection(linestack.s[:linestack.itop+1], color='r')]))
    return s.s[:s.itop+1], plot

    
    
if __name__ == '__main__': 
    points = rand_point2_set(3, 0, 10).tolist()
    
    pprint(points)
    
    print('--' * 10)
    
    convex_hull, plot = graham_vis(points)
    
    pprint(convex_hull)
    plot.draw()    

    
    
    
    