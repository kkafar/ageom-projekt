
import os
from sys import path
path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from lib.mytypes import ListOfPoints
from lib.geometric_tool_lab import *
from lib.util import *
from lib.getrand import *
from pprint import pprint
import operator


def lower_upper(point2_set: ListOfPoints) -> ListOfPoints:
    """ Algorytm wyzaczania otoczki wypukłej zbioru punktów płaszczyzny """

    # aby istniała otoczka, potrzebujemy mieć co najmniej 3 punkty
    if len(point2_set) < 3: return None

    point2_set.sort(key = operator.itemgetter(0, 1))
    
    upper_ch = [ point2_set[0], point2_set[1] ] 
    lower_ch = [ point2_set[0], point2_set[1] ]

    # wyznaczenie górnej otoczki
    for i in range( 2, len(point2_set) ):
        while len(upper_ch) > 1 and orientation(upper_ch[-2], upper_ch[-1], point2_set[i]) != -1:
            upper_ch.pop()

        upper_ch.append(point2_set[i])

    # wyznaczenie dolnej otoczki
    for i in range(2, len(point2_set) ):
        while len(lower_ch) > 1 and orientation(lower_ch[-2], lower_ch[-1], point2_set[i]) != 1:
            lower_ch.pop()

        lower_ch.append(point2_set[i])

    # połączenie w odpowienid sposób list wynikowych i zwrócenie 
    lower_ch.reverse()
    upper_ch.extend(lower_ch)

    return upper_ch



def main(): 
    test_point2_set = rand_point2_set(10, 0, 10).tolist()

    pprint(test_point2_set)
    print('-' * 10)

    ch = lower_upper(test_point2_set)

    pprint(ch)

    # plot.draw()






if __name__ == "__main__": 
    main()














