
import os
from sys import path

from numpy.lib.polynomial import poly
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint
import operator


def rtangent(polygon: ListOfPoints, point: Point) -> Union[int, None]:
    print('szukam stycznej do otoczki')
    pprint(polygon)
    print('przechodzacej przez punkt ', point)
    
    if len(polygon) < 2: return None
    
    n = len(polygon)
    
    # indeksy wierzchołków do wyszukiwania binarnego
    l, r, m = 0, n, None
    
    is_left_up, is_mid_down = None, None
    

    
    # polygon[0] po prawej polygon[1] oraz polygon[0] nie jest po lewej względem polygon[-1]
    # a co gdy 3 punkty są współliniowe? 
    if orientation(point, polygon[1], polygon[0]) == -1 and orientation(point, polygon[-1], polygon[0]) != 1:
        return 0
    
    while True:
        m = (l + r) // 2
        
        is_mid_down = (orientation(point, polygon[(m+1)%n], polygon[m]) == -1)
        
        if is_mid_down and orientation(point, polygon[(m-1)%n], polygon[m]) != 1:
            return m
    
        is_left_up = (orientation(point, polygon[(l+1)%n], polygon[l]) == 1)
        
        if is_left_up:
            if is_mid_down:
                r = m
            else:
                if orientation(point, polygon[l], polygon[m]) == 1:
                    r = m
                else:
                    l = m
        else:
            if not is_mid_down:
                l = m
            else:
                if orientation(point, polygon[l], polygon[m]) == -1:
                    r = m
                else:
                    l = m
                    
    
def ltangent(polygon: ListOfPoints, point: Point) -> Union[int, None]:
    print('szukam stycznej do otoczki')
    pprint(polygon)
    print('przechodzacej przez punkt ', point)
    
    
    if len(polygon) < 2: return None
    
    n = len(polygon)
    
    l, r, m  = 0, n, None
    
    is_left_down, is_mid_down = None, None
    
    
    if orientation(point, polygon[-1], polygon[0]) == 1 and orientation(point, polygon[1], polygon[0]) != -1:
        return 0
    
    while True:
        m = (l + r) // 2
        
        is_mid_down = (orientation(point, polygon[(m+1)%n], polygon[m]) == -1) 
        
        if (not is_mid_down) and orientation(point, polygon[(m-1)%n], polygon[m]) == 1:
            return m
        
        is_left_down = (orientation(point, polygon[(l+1)%n], polygon[l]) == -1)
        
        if is_left_down:
            if not is_mid_down:
                r = m
            else:
                if orientation(point, polygon[l], polygon[m]) == -1:
                    r = m
                else:
                    l = m
        else:
            if is_mid_down:
                l = m
            else:
                if orientation(point, polygon[l], polygon[m]) == 1:
                    r = m
                else:
                    l = m
                    
        
def increase_with_sorting(point2_set: ListOfPoints) -> Union[ListOfPoints, None]:
    if len( point2_set ) < 3: return None
    
    # posortowanie punktów po wsp. x na początku, pozwoli na pominięcie kroku z sprawdzaniem należenia punktu do wnętrza otoczki 
    # ponieważ biorąc każdy kolejny punkt, mamy gwarancję, że nie należy od do obecnie rozważanej otoczki
    
    point2_set.sort(key = operator.itemgetter(0, 1))
    
    # bierzemy pierwsze 3 punkty i tworzymy z nich otoczkę
    convex_hull = point2_set[:3]

    # pprint(convex_hull)

    # musimy zapewnić, że wierzchołki wyjściowej otoczki są podane w kolejności przeciwnej do ruchu wskazówek zegara 
    if orientation(convex_hull[0], convex_hull[1], convex_hull[2]) == -1:
        convex_hull[1], convex_hull[2] = convex_hull[2], convex_hull[1]
    
    for i in range(3, len( point2_set )):
        # znajdujemy styczne
        print('obecnie znana otoczka')
        pprint(convex_hull)
        print(f'szukam lewej stycznej z {point2_set[i]}')
        # left_tangent_idx = left_tangent(convex_hull, point2_set[i])
        # left_tangent_idx = tangent_l(point2_set[i], convex_hull)
        left_tangent_idx = ltangent(convex_hull, point2_set[i])
        
        if left_tangent_idx is None:
            print('nie znaleziono lewej stycznej')
        else:
            print(f'znaleziono lewa styczna {left_tangent_idx}')
            
        
        # print(f'szukam prawej stycznej z {point2_set[i]}') 
        # right_tangent_idx = right_tangent(convex_hull, point2_set[i])
        # right_tangent_idx = tangent_r(point2_set[i], convex_hull)
        right_tangent_idx = rtangent(convex_hull, point2_set[i])
        
        # if right_tangent_idx is None:
        #     print('nie znaleziono prawej stycznej')
        # else:
        #     print(f'znaleziono prawa styczna {right_tangent_idx}')
        # aktualizujemy otoczkę (TODO PYTANIE czy da się aktualizować otoczkę w czasie stałym?)
        left_tangent_point = convex_hull[left_tangent_idx]
        right_tangent_point = convex_hull[right_tangent_idx]        

        deletion_side: Literal[-1, 0, 1] = orientation(left_tangent_point, right_tangent_point, point2_set[i])

        if deletion_side != 0:
            if orientation(left_tangent_point, right_tangent_point, convex_hull[(left_tangent_idx + 1) % len(convex_hull)]) == deletion_side:
                step = 0
            else: 
                step = -1
                
            left = (left_tangent_idx + 1) % len(convex_hull)
            
            while convex_hull[left] != right_tangent_point:
                convex_hull.pop(left)
                left = (left + step) % len(convex_hull)
                
            convex_hull.insert(left, point2_set[i])
        else:
            # point2_set[i] jest współliniowy z obydwoma punktami styczności oraz jest ponad nimi 
            # wtedy w finalnym zbiorze powinny znaleźć się tylko 2 punkty - lewy punkt styczności oraz point2_set[i]
            convex_hull = [point2_set[left_tangent_idx], point2_set[i]]

    return convex_hull


def main(): 
    file_path = '../debug/increase_data.json'
    # save_file_path = 'test_data/convex_hull3.json'
    
    point_count = 3000
    
    # points = rand_point2_set(point_count, 0, 10).tolist()
    # points = rand_rect_points(point_count, [[0, 0], [10, 0], [10, 10], [0, 10]]).tolist()
    points = load_points_from_json(file_path)

    # save_points_to_json(file_path, points, indent=4)
    pprint(points)
    print('-' * 10)
    
    # convex_hull = increase_with_sorting(points)
    
    # save_points_to_json(file_path, convex_hull, indent = 4)    
    
    plot = Plot(scenes=[Scene(points=[PointsCollection(points)])])
    
    # plot.add_scene(Scene(points=[PointsCollection(convex_hull, color='r')]))
    
    plot.draw()

    # pprint(convex_hull)
    
    
    
    
    # plot.draw()

if __name__ == "__main__": 
#     obecnie znana otoczka
# [[0.0, 0.028115298754645135],
#  [0.01523045649619581, 0.0],
#  [9.996688970065955, 0.0],
#  [10.0, 0.0026406644727150486],
#  [9.999950578062139, 10.0],
#  [0.025116610956338326, 10.0],
#  [0.0, 9.999951234026465]]
# szukam lewej stycznej z [10.0, 0.038506319393473154]
# znaleziono lewa styczna 3
# obecnie znana otoczka
# [[0.0, 0.05910278687448978], [10.0, 0.038506319393473154]]
# szukam lewej stycznej z [10.0, 0.06725244544593334]
# tangent_l zwraca None
# [10.0, 0.06725244544593334]
# [[0.0, 0.05910278687448978], [10.0, 0.038506319393473154]]
# nie znaleziono lewej stycznej

    point = [10.0, 0.038506319393473154]
    ch = [[0.0, 0.05910278687448978], [10.0, 0.038506319393473154]]
    a = tangent_l(point, ch)
    print(a)

