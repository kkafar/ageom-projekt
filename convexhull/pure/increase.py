
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


def rltangent(polygon: ListOfPoints, point: Point):
    n = len(polygon)
    
    right = index_of_max(polygon, cmp_idx=0)
    
    left = right
    
    # print('wyznaczam styczne do')
    # pprint(polygon)
    # print('punkt odniesienia', point)

    
    # print('lewa styczna')
    left_orient = orientation(point, polygon[left % n], polygon[(left-1)%n])  
    while left_orient != -1:
        # print(f'{polygon[(left-1)%n]} NIE po prawej {point} -> {polygon[left%n]}')
        if left_orient == 0 and dist_sq(point, polygon[left]) >= dist_sq(point, polygon[(left-1)%n]):
            # print('przerywam dzialanie petli left')
            break
        left = (left-1) % n
        left_orient = orientation(point, polygon[left % n], polygon[(left-1)%n]) 
        
    # print('prawa styczna')
    right_orient = orientation(point, polygon[right%n], polygon[(right+1)%n]) 
    while right_orient != 1:
        # print(f'{polygon[(right+1)%n]} NIE po lewej {point} -> {polygon[right%n]}')
        if right_orient == 0 and dist_sq(point, polygon[right]) >= dist_sq(point, polygon[(right+1)%n]):
            # print('przerywam dzialanie petli right')
            break
        right = (right+1)%n
        right_orient = orientation(point, polygon[right%n], polygon[(right+1)%n]) 
        
        
    return left, right

    

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
        # print('obecnie znana otoczka')
        # pprint(convex_hull)

        rltang = rltangent(convex_hull, point2_set[i])
        # print(f'szukam lewej stycznej z {point2_set[i]}')
        # left_tangent_idx = left_tangent(convex_hull, point2_set[i])
        # left_tangent_idx = tangent_l(point2_set[i], convex_hull)
        # left_tangent_idx = ltangent(convex_hull, point2_set[i])
        left_tangent_idx = rltang[0]
            
        # print(f'szukam prawej stycznej z {point2_set[i]}') 
        # right_tangent_idx = right_tangent(convex_hull, point2_set[i])
        # right_tangent_idx = tangent_r(point2_set[i], convex_hull)
        # right_tangent_idx = rtangent(convex_hull, point2_set[i])
        right_tangent_idx = rltang[1]
        
        # print('znalezione styczne')
        # print(convex_hull[left_tangent_idx])
        # print(convex_hull[right_tangent_idx])
        
        # if right_tangent_idx is None:
        #     print('nie znaleziono prawej stycznej')
        # else:
        #     print(f'znaleziono prawa styczna {right_tangent_idx}')
        # aktualizujemy otoczkę (TODO PYTANIE czy da się aktualizować otoczkę w czasie stałym?)
        left_tangent_point = convex_hull[left_tangent_idx]
        right_tangent_point = convex_hull[right_tangent_idx]        

        deletion_side: Literal[-1, 0, 1] = orientation(left_tangent_point, right_tangent_point, point2_set[i])

        if deletion_side != 0:
            lrlnext_orient = orientation(left_tangent_point, right_tangent_point, convex_hull[(left_tangent_idx + 1) % len(convex_hull)])
            if lrlnext_orient == deletion_side or lrlnext_orient == 0:
                step = 0
            else: 
                step = -1
                
            left = (left_tangent_idx + 1) % len(convex_hull)
            
            while convex_hull[left % len(convex_hull)] != right_tangent_point:
                convex_hull.pop(left % len(convex_hull))
                left = (left + step) % len(convex_hull)
                
            convex_hull.insert(left % len(convex_hull), point2_set[i])
        else:
            # point2_set[i] jest współliniowy z obydwoma punktami styczności oraz jest ponad nimi 
            # wtedy w finalnym zbiorze powinny znaleźć się tylko 2 punkty - lewy punkt styczności oraz point2_set[i]
            convex_hull = [point2_set[left_tangent_idx], point2_set[i]]

    return convex_hull


def main(): 
    file_path = '../debug/increase_data.json'
    # save_file_path = 'test_data/convex_hull3.json'
    
    point_count = 5000
    
    # points = rand_point2_set(point_count, 0, 10).tolist()
    # points = rand_rect_points(point_count, [[0, 0], [10, 0], [10, 10], [0, 10]]).tolist()
    points = load_points_from_json(file_path)

    # save_points_to_json(file_path, points, indent=4)
    pprint(points)
    print('-' * 10)
    
    convex_hull = increase_with_sorting(points)
    
    # save_points_to_json(file_path, convex_hull, indent = 4)    
    # save_points_to_json(file_path, points, indent=4)
    
    plot = Plot(scenes=[Scene(points=[PointsCollection(points)])])
    
    plot.add_scene(Scene(points=[PointsCollection(points), PointsCollection(convex_hull, color='r')]))
    
    plot.draw()

    # pprint(convex_hull)
    
    
    
    
    # plot.draw()

if __name__ == "__main__": 
    main()