from random import randint
from copy import deepcopy
from lib.det import *
from lib.tangent import *
from lib.util import *
from pure.graham import graham
import matplotlib.colors as mcolors
from lib.geometric_tool_lab import *

def compr(p, q, current,
          accur=10 ** (-7)):  # jezeli p jest po prawej  odcinka [current,q] - jest 'wiekszy', to zwracamy 1
    if det(current, p, q) >= accur:
        return -1
    elif det(current, p, q) <= accur:
        return 1
    else:
        return 0


def nextvert(C, curr,accur=10**(-7)):  # dla danego punktu wspolzednymi z Q[i][j] jesli jest to punkt nalezacy do finalnej otoczki, to
    # zwraca nastepny punkt nalezacy do finalnej otoczki zadanego w takich samych wspolzednych Q[nxt[0]][nxt[1]]
    i, j = curr
    nxt = (i, (j + 1) % len(C[i]))


    for k in range(len(C)):


        t = tangent_r(C[i][j], C[k])
        if t == None:
            print("zle")
            continue

        if  det(C[i][j],C[nxt[0]][nxt[1]],C[k][t])<accur and (k,t)!=(curr):
            if det(C[i][j],C[nxt[0]][nxt[1]],C[k][t])>-accur:
                if length([C[k][t],C[i][j]]) <= length([C[nxt[0]][nxt[1]],C[i][j]]):
                    continue
            nxt=(k,t)

    return nxt


def chanUtil(points, m):
    Q = divide(points, m)
    C = []
    for i in range(len(Q)):
        C.append(graham(Q[i]))

    curr = (0, 0)
    ans = []
    i = 0

    while i < m:
        ans.append(C[curr[0]][curr[1]])

        nxt = nextvert(C, curr)
        if nxt == (0, 0):
            return ans
        curr = nxt
        i += 1

    return None


def chan(points):
    plot = None
    n = len(points)
    m = 4
    hoax = None
    while hoax == None:
        hoax = chanUtil(points, m)
        m = min(n, m * m)

    return hoax


