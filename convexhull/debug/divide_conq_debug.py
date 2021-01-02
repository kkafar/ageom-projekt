from lib.mytypes import *
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint
import operator


def merge_convex_hulls(left_convex_hull: List[Point], right_convex_hull: List[Point]) -> List[Point]:
    """ Łączenie dwóch rozdzielnych otoczek. Otoczki muszą być zadane w formie wierzchołków podanych w kolejności przeciwnej do 
    ruchu wskazówek zegara. Ponadto left_convex_hull powinno być lewą otoczką, a right_convex_hull prawą. """

    print('laczenie otoczek')
    print('lewa otoczka')
    pprint(left_convex_hull)
    print('prawa otoczka')
    pprint(right_convex_hull)
    
    

    left_ch_size = len(left_convex_hull)
    print(f'rozmiar lewej: {left_ch_size}')    
    right_ch_size = len(right_convex_hull)
    print(f'rozmiar prawej: {right_ch_size}')


    # znajdujemy prawy skrajny punkt lewej otoczki 
    left_ch_rightmost_idx = index_of_max(left_convex_hull, cmp_idx=0)
    print(f'skrajny punkt lewej otoczki {left_convex_hull[left_ch_rightmost_idx]}')
    right_ch_leftmost_idx = index_of_min(right_convex_hull, cmp_idx=0)
    print(f'skrajny punkt prawej otoczki {right_convex_hull[right_ch_leftmost_idx]}')
    
    left = left_convex_hull[left_ch_rightmost_idx]
    right = right_convex_hull[right_ch_leftmost_idx]
    left_idx = left_ch_rightmost_idx
    right_idx = right_ch_leftmost_idx
    

    print('gorna styczna')
    # górna styczna
    while orientation(left, right, right_convex_hull[(right_idx - 1) % right_ch_size]) == 1 or orientation(right, left, left_convex_hull[(left_idx + 1) % left_ch_size]) == -1:
        print(f'punkty:\n{left}\n{right}\n{right_convex_hull[(right_idx - 1) % right_ch_size]}\ntworza skret w lewo\nLUB')
        print(f'punkty\n{right}\n{left}\n{left_convex_hull[(left_idx + 1) % left_ch_size]}\ntworza skret w prawo')
        # podnosimy punkt na prawej otoczce
        while orientation(left, right, right_convex_hull[(right_idx - 1) % right_ch_size]) == 1:
            print(f'punkty:\n{left}\n{right}\n{right_convex_hull[(right_idx - 1) % right_ch_size]}\ntworza skret w lewo')
            right_idx = (right_idx - 1) % right_ch_size
            right = right_convex_hull[right_idx]

        # podnosimy punkt na lewej otoczce
        while orientation(right, left, left_convex_hull[(left_idx + 1) % left_ch_size]) == -1:
            print(f'punkty\n{right}\n{left}\n{left_convex_hull[(left_idx + 1) % left_ch_size]}\ntworza skret w prawo')
            left_idx = (left_idx + 1) % left_ch_size
            left = left_convex_hull[left_idx]
            
            
    upper_tangent_left_idx = left_idx
    upper_tangent_right_idx = right_idx
    
    print(f'gorna styczna\n{left_convex_hull[upper_tangent_left_idx]}\n{right_convex_hull[upper_tangent_right_idx]}')
    
            
    print('dolna styczna')
    # dolna styczna
    left = left_convex_hull[left_ch_rightmost_idx]
    right = right_convex_hull[right_ch_leftmost_idx]
    left_idx = left_ch_rightmost_idx
    right_idx = right_ch_leftmost_idx
            
    while orientation(left, right, right_convex_hull[(right_idx + 1) % right_ch_size]) == -1 or orientation(right, left, left_convex_hull[(left_idx - 1) % left_ch_size]) == 1:
        print(f'punkty:\n{left}\n{right}\n{right_convex_hull[(right_idx + 1) % right_ch_size]}\ntworza zakret w prawo\nLUB') 
        print(f'punkty:\n{right}\n{left}\n{left_convex_hull[(left_idx - 1) % left_ch_size]}\ntworza zakret w lewo')
        # opuszczamy punkt na prawej otoczce
        while orientation(left, right, right_convex_hull[(right_idx + 1) % right_ch_size]) == -1:
            print(f'punkty:\n{left}\n{right}\n{right_convex_hull[(right_idx + 1) % right_ch_size]}\ntworza zakret w prawo') 
            right_idx = (right_idx + 1) % right_ch_size
            right = right_convex_hull[right_idx]

        # opuszczamy punkt na lewej otoczce
        while orientation(right, left, left_convex_hull[(left_idx - 1) % left_ch_size]) == 1:
            print(f'punkty:\n{right}\n{left}\n{left_convex_hull[(left_idx - 1) % left_ch_size]}\ntworza zakret w lewo')
            left_idx = (left_idx - 1) % left_ch_size
            left = left_convex_hull[left_idx]
            
            
    lower_tangent_left_idx = left_idx
    lower_tangent_right_idx = right_idx
    
    print(f'dolna styczna\n{left_convex_hull[lower_tangent_left_idx]}\n{right_convex_hull[lower_tangent_right_idx]}')    

    
    merged_convex_hull = [ ]

    while upper_tangent_left_idx != lower_tangent_left_idx:
        merged_convex_hull.append(left_convex_hull[upper_tangent_left_idx])
        upper_tangent_left_idx = (upper_tangent_left_idx + 1) % left_ch_size
    else:
        merged_convex_hull.append(left_convex_hull[lower_tangent_left_idx])
        
        
    while lower_tangent_right_idx != upper_tangent_right_idx:
        merged_convex_hull.append(right_convex_hull[lower_tangent_right_idx])
        lower_tangent_right_idx = (lower_tangent_right_idx + 1) % right_ch_size    
    else:
        merged_convex_hull.append(right_convex_hull[lower_tangent_right_idx])
    
    
    print("Zloczone:")
    pprint(merged_convex_hull)
    return merged_convex_hull 




def divide_conq(point2_set: List[Point], k: int) -> Union[list[Point], None]:
    if len(point2_set) < 3 or k <= 0: return None     

    
    def divide_conq_rec(point2_set: list[Point], side: Literal[0, 1]) -> list[Point]:
        side_message = 'left' if side == 0 else 'right'
        print('divide_conq_rec ' + side_message)
        pprint(point2_set)

        if len(point2_set) <= k: return point2_set
    
        left_convex_hull = divide_conq_rec(point2_set[ : len(point2_set) // 2], 0)
        right_convex_hull = divide_conq_rec(point2_set[len(point2_set) // 2 : ], 1)
    
        return merge_convex_hulls(left_convex_hull, right_convex_hull)
    
    point2_set.sort(key = operator.itemgetter(0, 1))    

    print('Posortowany zbior')
    pprint(point2_set)
    print('-' * 20)

    return divide_conq_rec(point2_set, 0)
    
    




def main():
    points_save_path = './divide_conq_data/points.json'

    points = rand_point2_set(10, 0, 10).tolist()
    # points = load_points_from_json(points_save_path)
    
    save_points_to_json(points_save_path, points, 4)

    pprint(points)

    print("--" * 10)

    plot = Plot(scenes=[Scene(
        points=[
            PointsCollection(points)
        ]
   )])


    convex_hull = divide_conq(points, 2)
    
    pprint(convex_hull)
    
    plot.add_scene(Scene(
        points=[
            PointsCollection(points),
            PointsCollection(convex_hull, marker='s', color='r')
        ]
    ))
    plot.draw()
    
if __name__ == "__main__":
    main()