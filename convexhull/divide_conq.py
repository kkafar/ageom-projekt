from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint
import operator


def merge_convex_hulls(left_convex_hull: list[Point], right_convex_hull: list[Point]) -> list[Point]:
    """ Łączenie dwóch rozdzielnych otoczek. Otoczki muszą być zadane w formie wierzchołków podanych w kolejności przeciwnej do 
    ruchu wskazówek zegara. Ponadto left_convex_hull powinno być lewą otoczką, a right_convex_hull prawą. """

    left_ch_size = len(left_convex_hull)
    right_ch_size = len(right_convex_hull)


    # znajdujemy prawy skrajny punkt lewej otoczki 
    left_ch_rightmost_idx = index_of_max(left_convex_hull, cmp_idx=0)
    right_ch_leftmost_idx = index_of_min(right_convex_hull, cmp_idx=0)

    
    left = left_convex_hull[left_ch_rightmost_idx]
    right = right_convex_hull[right_ch_leftmost_idx]
    left_idx = left_ch_rightmost_idx
    right_idx = right_ch_leftmost_idx
    

    # górna styczna
    while orientation(left, right, right_convex_hull[(right_idx - 1) % right_ch_size]) != -1 or orientation(right, left, left_convex_hull[(left_idx + 1) % left_ch_size]) != 1:

        # podnosimy punkt na prawej otoczce
        while orientation(left, right, right_convex_hull[(right_idx - 1) % right_ch_size]) != -1:
            right_idx = (right_idx - 1) % right_ch_size
            right = right_convex_hull[right_idx]

        # podnosimy punkt na lewej otoczce
        while orientation(right, left, left_convex_hull[(left_idx + 1) % left_ch_size]) != 1:
            left_idx = (left_idx + 1) % left_ch_size
            left = left_convex_hull[left_idx]
            
            
    upper_tangent_left_idx = left_idx
    upper_tangent_right_idx = right_idx
    
            
    # dolna styczna
    left = left_convex_hull[left_ch_rightmost_idx]
    right = right_convex_hull[right_ch_leftmost_idx]
    left_idx = left_ch_rightmost_idx
    right_idx = right_ch_leftmost_idx
            
    while orientation(left, right, right_convex_hull[(right_idx + 1) % right_ch_size]) != 1 or orientation(right, left, left_convex_hull[(left_idx - 1) % left_ch_size]) != -1:
        
        # opuszczamy punkt na prawej otoczce
        while orientation(left, right, right_convex_hull[(right_idx + 1) % right_ch_size]) != 1:
            right_idx = (right_idx + 1) % right_ch_size
            right = right_convex_hull[right_idx]

        # opuszczamy punkt na lewej otoczce
        while orientation(right, left, left_convex_hull[(left_idx - 1) % left_ch_size]) != -1:
            left_idx = (left_idx - 1) % left_ch_size
            left = left_convex_hull[left_idx]
            
            
    lower_tangent_left_idx = left_idx
    lower_tangent_right_idx = right_idx
        
        
    merged_convex_hull = [ ]

    while upper_tangent_left_idx != ((lower_tangent_left_idx + 1) % left_ch_size):
        merged_convex_hull.append(left_convex_hull[upper_tangent_left_idx])
        upper_tangent_left_idx = (upper_tangent_left_idx + 1) % left_ch_size
        
    while lower_tangent_right_idx != ((upper_tangent_right_idx + 1) % right_ch_size):
        merged_convex_hull.append(right_convex_hull[lower_tangent_right_idx])
        lower_tangent_right_idx = (lower_tangent_right_idx + 1) % right_ch_size    
    
    return merged_convex_hull 




def divide_conq(point2_set: list[Point]) -> Union[list[Point], None]:
    if len(point2_set) <= 2: return point2_set
    
    left_convex_hull = divide_conq(point2_set[ : len(point2_set) // 2])
    right_convex_hull = divide_conq(point2_set[len(point2_set) // 2 : ])
    
    return merge_convex_hulls(left_convex_hull, right_convex_hull)




def main():
    random_points = rand_point2_set(10, 0, 10).tolist()

    pprint(random_points)

    print("--" * 10)

    convex_hull = divide_conq(random_points)
    
    
    pprint(convex_hull)
    
    
if __name__ == "__main__":
    main()