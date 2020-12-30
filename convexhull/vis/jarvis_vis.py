import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint


def jarvis_vis(points: ListOfPoints) -> Tuple[ListOfPoints, Plot]:
    """  """
    
    plot = Plot(scenes=[Scene(points=[PointsCollection(points, marker='.')])])
    lines = []
    count = 0

    # Tolerancja dla 0
    EPS = 1e-8

    # znajdujemy indeks punktu o najmniejszej rzędnej (jeżeli jest wiele - 
    # to bierzemy ten z nich o najmniejszej odciętej)
    istart = 0
    convex_hull = []
    
    # rozmiar tablicy dzielimy przez 2, ponieważ każdy punkt jest liczony za 2 w np.array
    for i in range(len(points)):
        if points[i][1] < points[istart][1]:
            istart = i
        elif points[i][1] == points[istart][1] and points[i][0] < points[istart][0]:
            istart = i
     
    # zbieramy indeksy punktów na otoczce
    convex_hull.append(istart)

    irand = 0 if istart != 0 else 1
    
    vec = points[irand] - points[istart]
    prev = istart
    while True:
#         print('jarvis: petla while')
        imax = irand
        
        plot.add_scene(Scene(points=[PointsCollection(points, marker='.'), 
                                    PointsCollection(points[convex_hull], color='r')],
                            lines=[LinesCollection(lines[:count], color='r')]))
        count += 1
            
            
        for i in range(points.size // 2):
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
                    
                plot.add_scene(Scene(points=[PointsCollection(points, marker='.'), 
                                            PointsCollection(points[convex_hull], color='r'),
                                            PointsCollection([points[i]], color='indigo'),
                                            PointsCollection([points[imax]], color='green')],
                                    lines=[LinesCollection(lines[:count], color='r'),
                                            LinesCollection([[points[prev], points[i]]], color='indigo', linestyle='--'),
                                            LinesCollection([[points[prev], points[imax]]], color='green', linestyle='--')]))

                        
        # dlaczego to od razu dodaje całą otoczkę? xDD
        lines.append([points[prev], points[imax]])
                        
                
        # po wykonaniu tej pęli w imax znajduje sie indeks punktu "do którego kąt skierowany jest najmniejszy"
        # ==> należy on do otoczki (chyba, że inny punkt jest wspóliniowy? to co wtedy??)
        # W TYM MIEJSCU NALEŻY DODAĆ KRAWĘDŹ DO WIZUALIZACJI! (zapamiętać ją)
        # jeżeli dojedziemy do punktu początkowego to kończymy
        if imax == istart:
            break;


        convex_hull.append(imax)
        vec = points[imax] - points[prev]
        prev = imax
    
    
    plot.scenes.insert(0, Scene(points=[PointsCollection(points, marker='.'),
                                        PointsCollection(points[convex_hull], color='r')],
                                lines=[LinesCollection(lines[:count], color='r')]))
    plot.add_scene(Scene(points=[PointsCollection(points, marker='.'), 
                                PointsCollection(points[convex_hull], color='r')],
                        lines=[LinesCollection(lines[:count], color='r')]))
    return points[convex_hull], plot

    
    
    
def main(): 
    points = rand_point2_set(10, 0, 10)
    
    pprint(points)
    
    print('--' * 10)
    
    convex_hull, plot = jarvis_vis(points)

    pprint(convex_hull)
    
    plot.draw()
    

if __name__ == '__main__':
    main()

    