
import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pure.jarvis import jarvis
from pprint import pprint
import operator 


def merge_convex_hulls_vis(left_convex_hull: ListOfPoints, right_convex_hull: ListOfPoints, points: ListOfPoints, scenes: ListOfPoints) -> ListOfPoints:
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

    left_convex_hull_lc = LinesCollection([
        [ left_convex_hull[i], left_convex_hull[(i+1) % len(left_convex_hull)] ]
        for i in range(len(left_convex_hull))
    ], linestyle='--', color='forestgreen')

    right_convex_hull_lc = LinesCollection([
        [ right_convex_hull[i], right_convex_hull[(i+1) % len(right_convex_hull)] ]
        for i in range(len(right_convex_hull))
    ], linestyle='--', color='darkorange')


    scenes.append(Scene(
        points=[
            PointsCollection(points, marker='.'),
            PointsCollection(left_convex_hull, marker='s', color='forestgreen'),
            PointsCollection(right_convex_hull, marker='s', color='darkorange'),
            PointsCollection([left], marker='x', color='r'),
            PointsCollection([right], marker='x', color='r')
        ],
        lines=[
            left_convex_hull_lc,
            right_convex_hull_lc,
            LinesCollection([[left, right]], linestyle='dotted', color='r')
        ]
    ))
    

    # górna styczna
    left_flag, right_flag = True, True
    while   orientation(left, right, right_convex_hull[(right_idx - 1) % right_ch_size]) != -1 and right_flag \
            or \
            orientation(right, left, left_convex_hull[(left_idx + 1) % left_ch_size]) != 1 and left_flag:
                
        left_flag, right_flag = False, False
        
        # podnosimy punkt na prawej otoczce
        left_right_orient = orientation(left, right, right_convex_hull[(right_idx - 1) % right_ch_size])
        while left_right_orient != -1:
            if left_right_orient == 0 and dist_sq(left, right) >= dist_sq(left, right_convex_hull[(right_idx - 1) % right_ch_size]):
                right_flag = False
                break
            
            right_idx = (right_idx - 1) % right_ch_size
            right = right_convex_hull[right_idx]
            left_right_orient = orientation(left, right, right_convex_hull[(right_idx - 1) % right_ch_size])
            scenes.append(Scene(
                points=[
                    PointsCollection(points, marker='.'),
                    PointsCollection(left_convex_hull, marker='s', color='forestgreen'),
                    PointsCollection(right_convex_hull, marker='s', color='darkorange'),   
                    PointsCollection([left], marker='x', color='r'),
                    PointsCollection([right], marker='x', color='r')                     
                ],
                lines=[
                    left_convex_hull_lc,
                    right_convex_hull_lc,
                    LinesCollection([[left, right]], linestyle='dotted', color='r')
                ]
            ))
        else:
            right_flag = True

        # podnosimy punkt na lewej otoczce
        right_left_orient = orientation(right, left, left_convex_hull[(left_idx + 1) % left_ch_size])
        while right_left_orient != 1:
            if right_left_orient == 0 and dist_sq(right, left) >= dist_sq(right, left_convex_hull[(left_idx + 1) % left_ch_size]):
                left_flag = False
                break
            
            left_idx = (left_idx + 1) % left_ch_size
            left = left_convex_hull[left_idx]
            right_left_orient = orientation(right, left, left_convex_hull[(left_idx + 1) % left_ch_size])
            scenes.append(Scene(
                points=[
                    PointsCollection(points, marker='.'),
                    PointsCollection(left_convex_hull, marker='s', color='forestgreen'),
                    PointsCollection(right_convex_hull, marker='s', color='darkorange'),   
                    PointsCollection([left], marker='x', color='r'),
                    PointsCollection([right], marker='x', color='r')                     
                ],
                lines=[
                    left_convex_hull_lc,
                    right_convex_hull_lc,
                    LinesCollection([[left, right]], linestyle='dotted', color='r')
                ]
            ))
        else:
            left_flag = True
            
            
    upper_tangent_left_idx = left_idx
    upper_tangent_right_idx = right_idx

    upper_tangent_lc = LinesCollection([
        [ left_convex_hull[upper_tangent_left_idx], right_convex_hull[upper_tangent_right_idx] ]
    ], linestyle='dotted', color='r')
    
            
    # dolna styczna
    left = left_convex_hull[left_ch_rightmost_idx]
    right = right_convex_hull[right_ch_leftmost_idx]
    left_idx = left_ch_rightmost_idx
    right_idx = right_ch_leftmost_idx
            
    left_flag, right_flag = True, True
    while   orientation(left, right, right_convex_hull[(right_idx + 1) % right_ch_size]) != 1 and right_flag \
            or \
            orientation(right, left, left_convex_hull[(left_idx - 1) % left_ch_size]) != -1 and left_flag:
        left_flag, right_flag = False, False

        # opuszczamy punkt na prawej otoczce
        left_right_orient = orientation(left, right, right_convex_hull[(right_idx + 1) % right_ch_size])
        while left_right_orient != 1:
            if left_right_orient == 0 and dist_sq(left, right) >= dist_sq(left, right_convex_hull[(right_idx + 1) % right_ch_size]):
                right_flag = False
                break
            right_idx = (right_idx + 1) % right_ch_size
            right = right_convex_hull[right_idx]
            left_right_orient = orientation(left, right, right_convex_hull[(right_idx + 1) % right_ch_size])
            scenes.append(Scene(
                points=[
                    PointsCollection(points, marker='.'),
                    PointsCollection(left_convex_hull, marker='s', color='forestgreen'),
                    PointsCollection(right_convex_hull, marker='s', color='darkorange'),   
                    PointsCollection([left], marker='x', color='r'),
                    PointsCollection([right], marker='x', color='r')                     
                ],
                lines=[
                    left_convex_hull_lc,
                    right_convex_hull_lc,
                    upper_tangent_lc,
                    LinesCollection([[left, right]], linestyle='dotted', color='r')
                ]
            ))   
        else:
            right_flag = True
            

        # opuszczamy punkt na lewej otoczce
        right_left_orient = orientation(right, left, left_convex_hull[(left_idx - 1) % left_ch_size])
        while orientation(right, left, left_convex_hull[(left_idx - 1) % left_ch_size]) != -1:
            if right_left_orient == 0 and dist_sq(right, left) >= dist_sq(right, left_convex_hull[(left_idx - 1) % left_ch_size]):
                left_flag = False
                break
                    
            left_idx = (left_idx - 1) % left_ch_size
            left = left_convex_hull[left_idx]
            right_left_orient = orientation(right, left, left_convex_hull[(left_idx - 1) % left_ch_size])
            
            scenes.append(Scene(
                points=[
                    PointsCollection(points, marker='.'),
                    PointsCollection(left_convex_hull, marker='s', color='forestgreen'),
                    PointsCollection(right_convex_hull, marker='s', color='darkorange'),   
                    PointsCollection([left], marker='x', color='r'),
                    PointsCollection([right], marker='x', color='r')                     
                ],
                lines=[
                    left_convex_hull_lc,
                    right_convex_hull_lc,
                    upper_tangent_lc,
                    LinesCollection([[left, right]], linestyle='dotted', color='r')
                ]
            ))
        else:
            left_flag = True
            
            
    lower_tangent_left_idx = left_idx
    lower_tangent_right_idx = right_idx
    
    lower_tangent_lc = LinesCollection([
        [ left_convex_hull[lower_tangent_left_idx], right_convex_hull[lower_tangent_right_idx] ]
    ], linestyle='dotted', color='r')

    scenes.append(Scene(
        points=[
            PointsCollection(points, marker='.'),
            PointsCollection(left_convex_hull, marker='s', color='forestgreen'),
            PointsCollection(right_convex_hull, marker='s', color='darkorange'),                  
        ],
        lines=[
            left_convex_hull_lc,
            right_convex_hull_lc,
            upper_tangent_lc,
            lower_tangent_lc
        ]
    ))

    
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
    
    return merged_convex_hull 


def divide_conq_vis(point2_set: ListOfPoints, k: int) -> Union[Tuple[ListOfPoints, Plot], None]:
    if len(point2_set) < 3 or k <= 0: return None     

    plot = Plot(scenes=[Scene(points=[PointsCollection(point2_set)])])
    

    def divide_conq_rec_viz(points: ListOfPoints, scenes: ListOfPoints) -> ListOfPoints:
        if len(points) <= 2:
            scenes.append(Scene(
                points=[
                    PointsCollection(point2_set, marker='.'),
                    PointsCollection(points, marker='s', color='r')
                ],
                lines=[
                    LinesCollection([
                        [ points[0], points[1 % len(points)] ]
                    ], linestyle='--', color='r')
                ]
            ))
            return points
        elif len(points) <= k:
            convex_hull = jarvis(np.array(points))
            scenes.append(Scene(
                points=[
                    PointsCollection(point2_set, marker='.'),
                    PointsCollection(convex_hull, marker='s', color='r')
                ],
                lines=[
                    LinesCollection([
                        [ points[i], points[(i + 1) % len(points)] ]
                        for i in range(len(points))
                    ], linestyle='--', color='r')
                ]
            ))
            return convex_hull

        scenes.append(Scene(
            points=[
                PointsCollection(point2_set, marker='.'),
                PointsCollection(points, color='orchid'),
            ]
        ))

        left_points = points[ : len(points) // 2]
        right_points = points[len(points) // 2 : ] 
        
        scenes.append(Scene(
            points=[
                PointsCollection(point2_set, marker='.'),
                PointsCollection(left_points, color='forestgreen'),
                PointsCollection(right_points, color='darkorange')
            ]
        ))


        left_convex_hull = divide_conq_rec_viz(left_points, scenes)

        scenes.append(Scene(
            points=[
                PointsCollection(point2_set, marker='.'),
                PointsCollection(left_points, color='forestgreen'),
                PointsCollection(right_points, color='darkorange'),
                PointsCollection(left_convex_hull, marker='s', color='r')
            ],
            lines=[
                LinesCollection([
                    [ left_convex_hull[i], left_convex_hull[(i + 1) % len(left_convex_hull)] ] 
                    for i in range(len(left_convex_hull))
                ], linestyle='--', color='r')
            ]
        ))

        right_convex_hull = divide_conq_rec_viz(right_points, scenes)

        scenes.append(Scene(
            points=[
                PointsCollection(point2_set, marker='.'),
                PointsCollection(left_points, color='forestgreen'),
                PointsCollection(right_points, color='darkorange'),
                PointsCollection(right_convex_hull, marker='s', color='r')
            ],
            lines=[
                LinesCollection([
                    [ left_convex_hull[i], left_convex_hull[(i + 1) % len(left_convex_hull)] ] 
                    for i in range(len(left_convex_hull))
                ], linestyle='--', color='r'),
                LinesCollection([
                    [ right_convex_hull[i], right_convex_hull[(i + 1) % len(right_convex_hull)] ]
                    for i in range(len(right_convex_hull))
                ], linestyle='--', color='r')
            ]
        ))



        merged_convex_hull = merge_convex_hulls_vis(left_convex_hull, right_convex_hull, point2_set, scenes)

        scenes.append(Scene(
            points=[
                PointsCollection(point2_set, marker='.'),
                PointsCollection(left_points, color='forestgreen'),
                PointsCollection(right_points, color='darkorange'),
                PointsCollection(merged_convex_hull, marker='s', color='r')
            ],
            lines=[
                LinesCollection([
                    [ merged_convex_hull[i], merged_convex_hull[(i + 1) % len(merged_convex_hull)] ]
                    for i in range(len(merged_convex_hull))
                ], linestyle='--', color='r')
            ]
        ))

        return merged_convex_hull
     

    point2_set.sort(key = operator.itemgetter(0, 1))    
    
    scenes = [Scene(points=[PointsCollection(point2_set)])]
    

    convex_hull = divide_conq_rec_viz(point2_set, scenes)

    scenes.append(Scene(
        points=[
            PointsCollection(point2_set, marker='.'),
            PointsCollection(convex_hull, marker='s', color='r')
        ],
        lines=[
            LinesCollection([
                [ convex_hull[i], convex_hull[(i + 1) % len(convex_hull)] ]
                for i in range(len(convex_hull))
            ], linestyle='solid', color='r')
        ]
    ))

    
    plot.add_scenes(scenes=scenes)

    

    return convex_hull, plot



def main():
    # points_save_path = './divide_conq_data/points.json'

    # points = rand_point2_set(30, 0, 10).tolist()
    points = rand_rect_points(100, [[0, 0], [10, 0], [10, 10], [0, 10]]).tolist()

    # points = load_points_from_json(points_save_path)
    
    # save_points_to_json(points_save_path, points, 4)

    pprint(points)


    print("--" * 10)


    convex_hull, plot = divide_conq_vis(points, 5)
    
    pprint(convex_hull)
    

    plot.draw()
    
if __name__ == "__main__":
    main()