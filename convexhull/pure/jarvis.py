import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint


def jarvis(points: ListOfPoints) -> ListOfPoints:
    """ Punkty powinny być w formie np.array (w celu obsługi indeksowania tablicowego) """
    
    # Tolerancja dla 0
    EPS = 1e-8

    convex_hull = []

    # znajdujemy indeks punktu o najmniejszej rzędnej (jeżeli jest wiele - 
    # to bierzemy ten z nich o najmniejszej odciętej)
    start_idx = index_of_min(points, 1)

    # zbieramy indeksy punktów na otoczce
    convex_hull.append(start_idx)

    rand_idx = 0 if start_idx != 0 else 1
    
    prev = start_idx

    while True:
        imax = rand_idx
            
        for i in range(len(points)):
            if i != prev and i != imax:
                orient = orientation(points[prev], points[imax], points[i], EPS)
                # jeżeli punkt jest po prawej stronie rozważanego wektora,
                #to jest nowym kandydatem na punkt otoczki
                if orient == -1:
                    imax = i
                    
                # jeżeli jest zerem (z dokładnością do tolerancji)
                # to sprawdzamy odległośc i bierzemy ten dalszy
                elif orient == 0 and (dist(points[prev], points[imax]) < dist(points[prev], points[i])):
                    imax = i
                    
                        
        # po wykonaniu tej pęli w imax znajduje sie indeks punktu "do którego kąt skierowany jest najmniejszy"
        # ==> należy on do otoczki 

        # jeżeli dojedziemy do punktu początkowego to kończymy
        if imax == start_idx:
            break;

        convex_hull.append(imax)
        
        prev = imax

    return points[convex_hull]

    
    
    
def main(): 
    points = rand_point2_set(10, 0, 10)
    
    pprint(points)
    
    print('--' * 10)
    
    convex_hull = jarvis(points)

    pprint(convex_hull)

    
    plot = Plot(scenes=[Scene(
        points=[
            PointsCollection(points),
            PointsCollection(convex_hull, marker='d', color='r')
        ]
    )])
    
    plot.draw()
    

if __name__ == '__main__':
    main()

    