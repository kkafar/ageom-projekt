
import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint
import operator


def right_tangent(polygon: ListOfPoints, point: Point) -> Union[int, None]:
    """ Zwraca punkt styczności (w formie indeksu) wielokąta WYPUKŁEGO polygon z prawą styczną poprowadzoną z punktu 
    nie należącego do wielokąta - point """
    
    n = len(polygon)

    if n < 3: return None
    
    
    # v_i > v_j <=> v_j znajduje się po lewej stronie odcinka point-v_i 
    # mówimy, że krawędż e_i = v_i -> v_(i+1) jest skierowana w dół, jeżeli v_i > v_(i+1)\
    
    # sprawdzamy czy v0 nie jest szukanym punktem styczności
    if orientation(polygon[0], polygon[1], point) == 1 and orientation(polygon[-1], polygon[0], point) == -1:
        return 0
    
    left = 0
    right = n
    
    
    # punkt styczności zawsze istnieje
    while True:
        mid = (left + right) // 2
        
        # sprawdzamy czy v_mid jest szukanym punktem styczności
        is_mid_down: bool = (orientation(polygon[mid], polygon[(mid + 1) % n], point) == 1)
        
        if is_mid_down and orientation(polygon[mid - 1], polygon[mid], point) == -1: 
            return mid % n
        
        # jeżeli mid nie był punktem stycznośći, to musimy zdecydować w którym łańcuchu go szukamy
        # [left, mid] czy [mid, right]
        
        is_left_up: bool = (orientation(polygon[left % n], polygon[(left + 1) % n], point) == -1)
        
        if is_left_up:
            if is_mid_down:
                # zawężamy się do [left, mid]
                right = mid
                
            else:
                # jeżeli v_left > v_mid
                if orientation(point, polygon[left], polygon[mid]) == 1:
                    # zawężamy się do [left, mid]
                    right = mid
                else:
                    # zawężamy się do [mid, right]
                    left = mid
        
        else:
            if not is_mid_down:
                left = mid
                
            else:
                # jeżeli v_mid > v_left
                if orientation(point, polygon[mid % n], polygon[left % n]) == 1:
                    right = mid
                
                else:
                    left = mid
                    
    
def left_tangent(polygon: ListOfPoints, point: Point) -> Union[Point, None]:
    """ Zwraca punkt styczności (w formie indeksu) wielokąta WYPUKŁEGO polygon z LEWĄ styczną poprowadzoną z punktu 
    nie należącego do wielokąta - point """

    n = len(polygon)
    
    if n < 3: return None
    

    left = 0
    right = n
    
    # v_i > v_j <=> v_j znajduje się po lewej stronie odcinka point-v_i 
    # mówimy, że krawędż e_i = v_i -> v_(i+1) jest skierowana w dół, jeżeli v_i > v_(i+1)\
    
    # sprawdzamy czy v0 nie jest szukanym punktem styczności
    if orientation(point, polygon[1], polygon[0]) == 1 and orientation(point, polygon[-1], polygon[0]) == 1:
        return 0
    
    # punkt stycznośći zawsze istnieje ==> pętla się zakończy
    while True:
        mid = (left + right) // 2

        is_mid_down: bool = (orientation(point, polygon[mid % n], polygon[(mid + 1) % n]) == 1)
        
        # sprawdzamy czy polygon[mid] nie jest szukanym punktem styczności
        if (not is_mid_down) and orientation(point, polygon[(mid - 1) % n], polygon[mid % n]) == 1:
            return mid % n
        
        # jeżeli polygon[mid] nie był punktem styczności 
        
        is_left_down: bool = (orientation(point, polygon[left], polygon[(left + 1) % n]) == 1)
        
        if is_left_down:
            if not is_mid_down:
                right = mid
            else:
                if orientation(point, polygon[mid % n], polygon[left % n]) == 1:
                    right = mid
                else:
                    left = mid
                    
        else:
            if is_mid_down:
                left = mid
            else:
                if orientation(point, polygon[left % n], polygon[mid % n]) == 1:
                    right = mid
                else:
                    left = mid
                 
        
        
def increase_with_sorting(point2_set: ListOfPoints) -> Union[ListOfPoints, None]:
    if len( point2_set ) < 3: return None
    
    # posortowanie punktów po wsp. x na początku, pozwoli na pominięcie kroku z sprawdzaniem należenia punktu do wnętrza otoczki 
    # ponieważ biorąc każdy kolejny punkt, mamy gwarancję, że nie należy od do obecnie rozważanej otoczki
    
    point2_set.sort(key = operator.itemgetter(0, 1))
    
    # bierzemy pierwsze 3 punkty i tworzymy z nich otoczkę
    convex_hull = point2_set[:3]

    # musimy zapewnić, że wierzchołki wyjściowej otoczki są podane w kolejności przeciwnej do ruchu wskazówek zegara
    if orientation(convex_hull[0], convex_hull[1], convex_hull[2]) == -1:
        convex_hull[1], convex_hull[2] = convex_hull[2], convex_hull[1]
    
    
    for i in range(3, len( point2_set )):
        # jeżeli obecnie sprawdzany punkt nie należy do wnętrza otoczki (convex_hull) to:
            # znajdujemy styczne do otoczki przechodzące przez obecnie sprawdzany punkt
            # aktualizujemy otoczkę poprzez
                # wszysktie punktu pomiędzy punktami styczności zastępujemy tym jednym, nowym

        # znajdujemy styczne 
        left_tangent_idx = left_tangent(convex_hull, point2_set[i])
        right_tangent_idx = right_tangent(convex_hull, point2_set[i])
        
        # aktualizujemy otoczkę (TODO PYTANIE czy da się aktualizować otoczkę w czasie stałym?)
        left_tangent_point = convex_hull[left_tangent_idx]
        right_tangent_point = convex_hull[right_tangent_idx]        

        deletion_side: Literal[-1, 1] = orientation(left_tangent_point, right_tangent_point, point2_set[i])

        if orientation(left_tangent_point, right_tangent_point, convex_hull[(left_tangent_idx + 1) % len(convex_hull)]) == deletion_side:
            step = 0
        else: 
            step = -1
            
        left = (left_tangent_idx + 1) % len(convex_hull)
        
        while convex_hull[left] != right_tangent_point:
            convex_hull.pop(left)
            left = (left + step) % len(convex_hull)
            
        convex_hull.insert(left, point2_set[i])

    return convex_hull


def main(): 
    # file_path = 'test_data/points3.json'
    # save_file_path = 'test_data/convex_hull3.json'
    
    point_count = 30
    
    point_set = rand_point2_set(point_count, 0, 10).tolist()
    # point_set = load_points_from_json(file_path)

    # save_points_to_json(file_path, point_set, indent=4)
    pprint(point_set)
    print('-' * 10)
    
    convex_hull = increase_with_sorting(point_set)
    
    # save_points_to_json(save_file_path, convex_hull, indent = 4)    
    
    pprint(convex_hull)
    
    
    
    
    # plot.draw()

if __name__ == "__main__": 
    main()


