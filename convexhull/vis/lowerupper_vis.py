from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint
import operator



def lower_upper_vis(point2_set: ListOfPoints) -> tuple[ListOfPoints, Plot]:
    upper_ch_segments = [ ] 
    lower_ch_segments = [ ] 
    plot = Plot(scenes = [])
    plot.add_scene(Scene(points=[
        PointsCollection(point2_set)
    ]))

    # aby istniała otoczka, potrzebujemy mieć co najmniej 3 punkty
    if len(point2_set) < 3: return None

    point2_set.sort(key = operator.itemgetter(0, 1))
    
    upper_ch = [ point2_set[0], point2_set[1] ] 
    lower_ch = [ point2_set[0], point2_set[1] ]

    upper_ch_segments.append([upper_ch[0], upper_ch[1]])
    lower_ch_segments.append([lower_ch[0], lower_ch[1]])

    # wyznaczenie górnej otoczki
    for i in range( 2, len(point2_set) ):
        plot.add_scene(Scene(
            points=[
                PointsCollection(point2_set, marker='.'),
                PointsCollection(upper_ch[:-1], marker='s', color='r'),
                PointsCollection([upper_ch[-1]], marker='d', color='m'),
                PointsCollection([point2_set[i]], marker='^', color='g')
            ],
            lines=[
                LinesCollection(upper_ch_segments.copy(), linestyle='-', color='r'),
                LinesCollection([[upper_ch[-1], point2_set[i]]], linestyle='--', color='g')
            ]
        ))
    


        while len(upper_ch) > 1 and orientation(upper_ch[-2], upper_ch[-1], point2_set[i]) != -1:
            plot.add_scene(Scene(
                points=[
                    PointsCollection(point2_set, marker='.'),
                    PointsCollection(upper_ch.copy(), marker='s', color='r'),
                    PointsCollection([point2_set[i]], marker='^', color='g')
                ],
                lines=[
                    LinesCollection(upper_ch_segments.copy(), linestyle='-', color='r'),
                    LinesCollection([[upper_ch[-2], point2_set[i]]], linestyle='--', color='m'),
                    LinesCollection([[upper_ch[-1], point2_set[i]]], linestyle='--', color='g')
                ]
            ))

            upper_ch.pop()

            upper_ch_segments.pop()
            
            plot.add_scene(Scene(
                points=[
                    PointsCollection(point2_set, marker='.'),
                    PointsCollection(upper_ch.copy(), marker='s', color='r'),
                    PointsCollection([point2_set[i]], marker='^', color='g')
                ],
                lines=[
                    LinesCollection(upper_ch_segments.copy(), linestyle='-', color='r'),
                    LinesCollection([[upper_ch[-1], point2_set[i]]], linestyle='--', color='g')
                ]
            ))

        upper_ch.append(point2_set[i])

        upper_ch_segments.append([upper_ch[-2], upper_ch[-1]])


    plot.add_scene(Scene(
        points=[
            PointsCollection(point2_set, marker='.'),
            PointsCollection(upper_ch.copy(), marker='s', color='r')
        ],
        lines=[
            LinesCollection(upper_ch_segments.copy(), linestyle='-', color='r')
        ]
    ))


    # wyznaczenie dolnej otoczki
    for i in range(2, len(point2_set) ):
        plot.add_scene(Scene(
            points=[
                PointsCollection(point2_set, marker='.'),
                PointsCollection(upper_ch.copy(), marker='s', color='r'),
                PointsCollection(lower_ch[:-1], marker='s', color='r'),
                PointsCollection([lower_ch[-1]], marker='d', color='m'),
                PointsCollection([point2_set[i]], marker='^', color='g')
            ],
            lines=[
                LinesCollection(upper_ch_segments, linestyle='-', color='r'),
                LinesCollection(lower_ch_segments.copy(), linestyle='-', color='r'),
                LinesCollection([[lower_ch[-1], point2_set[i]]], linestyle='--', color='g')
            ]
        ))

        while len(lower_ch) > 1 and orientation(lower_ch[-2], lower_ch[-1], point2_set[i]) != 1:
            plot.add_scene(Scene(
                points=[
                    PointsCollection(point2_set, marker='.'),
                    PointsCollection(upper_ch.copy(), marker='s', color='r'),
                    PointsCollection(lower_ch.copy(), marker='s', color='r'),
                    PointsCollection([point2_set[i]], marker='^', color='g')
                ],
                lines=[
                    LinesCollection(upper_ch_segments, linestyle='-', color='r'),
                    LinesCollection(lower_ch_segments.copy(), linestyle='-', color='r'),
                    LinesCollection([[lower_ch[-2], point2_set[i]]], linestyle='--', color='m'),
                    LinesCollection([[lower_ch[-1], point2_set[i]]], linestyle='--', color='g')
                ]
            ))

            lower_ch.pop()

            lower_ch_segments.pop()
            
            plot.add_scene(Scene(
                points=[
                    PointsCollection(point2_set, marker='.'),
                    PointsCollection(upper_ch.copy(), marker='s', color='r'),
                    PointsCollection(lower_ch.copy(), marker='s', color='r'),
                    PointsCollection([point2_set[i]], marker='^', color='g')
                ],
                lines=[
                    LinesCollection(upper_ch_segments, linestyle='-', color='r'),
                    LinesCollection(lower_ch_segments.copy(), linestyle='-', color='r'),
                    LinesCollection([[lower_ch[-1], point2_set[i]]], linestyle='--', color='g')
                ]
            ))

        lower_ch.append(point2_set[i])

        lower_ch_segments.append([lower_ch[-2], lower_ch[-1]])

        
    plot.add_scene(Scene(
        points=[
            PointsCollection(point2_set, marker='.'),
            PointsCollection(upper_ch.copy(), marker='s', color='r'),
            PointsCollection(lower_ch.copy(), marker='s', color='r')
        ],
        lines=[
            LinesCollection(upper_ch_segments, linestyle='-', color='r'),
            LinesCollection(lower_ch_segments.copy(), linestyle='-', color='r')
        ]
    ))
    

    # połączenie w odpowienid sposób list wynikowych i zwrócenie 
    lower_ch.reverse()
    upper_ch.extend(lower_ch)

    return upper_ch, plot



def main(): 
    test_point2_set = rand_point2_set(10, 0, 10).tolist()

    pprint(test_point2_set)
    print('-' * 10)

    ch, plot = lower_upper_vis(test_point2_set)

    pprint(ch)

    plot.draw()






if __name__ == "__main__": 
    main()
