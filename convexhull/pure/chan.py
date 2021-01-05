<<<<<<< HEAD
from random import randint
from copy import deepcopy
=======
# from lib.divide import *
>>>>>>> 123669c1ef09155ac2ad3bd07464e0fc1e7b680f
from lib.det import *
from lib.tangent import *
from lib.util import *
from pure.graham import graham
import matplotlib.colors as mcolors
from lib.geometric_tool_lab import *


def divide(points, m):
    n = len(points)
    for i in range(1,
                   n):  # gwarantuje, ze w pierwszym zbiorze Qi pierwszy element jest najnizszy, czyli nalezy do otoczki ostatecznej
        if points[i][1] < points[0][1]:
            buf = points[i]
            points[i] = points[0]
            points[0] = buf

    k = math.ceil(n / m)
    Q = [[] for i in range(k)]
    i = 0
    while i < n:
        for j in range(k):
            if i == n:
                break
            Q[j].append(points[i])
            i += 1
    if len(Q[0]) > m:
        return None

    return Q


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
<<<<<<< HEAD


=======
>>>>>>> 123669c1ef09155ac2ad3bd07464e0fc1e7b680f
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


