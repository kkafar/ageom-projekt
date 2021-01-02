from divide import *
from det import *
from tangentBothsides import *

def compr(p, q, current,
          accur=10 ** (-6)):  # jezeli p jest po prawej  odcinka [current,q] - jest 'wiekszy', to zwracamy 1
    if det(current, p, q) > accur:
        return -1
    elif det(current, p, q) < accur:
        return 1
    else:
        return 0


def nextvert(C, curr, plot=None, ans=None, points=None, accur=10 ** (-7)):  # dla danego punktu wspolzednymi z Q[i][j] jesli jest to punkt nalezacy do finalnej otoczki, to
    # zwraca nastepny punkt nalezacy do finalnej otoczki zadanego w takich samych wspolzednych Q[nxt[0]][nxt[1]]
    i, j = curr
    nxt = (i, (j + 1) % len(C[i]))
    print(nxt)
    for k in range(len(C)):
        if k == i:
            continue

        t = tangent_r(C[i][j], C[k])
        if t == None:
            continue

        if det(C[i][j], C[nxt[0]][nxt[1]], C[k][t]) < accur and (k, t) != (curr):
            if det(C[i][j], C[nxt[0]][nxt[1]], C[k][t]) > -accur:
                if length([C[k][t], C[i][j]]) > length([C[nxt[0]][nxt[1]], C[i][j]]):
                    nxt = (k, t)
                    continue
            nxt = (k, t)

    return nxt


def chanUtil(points, m):
    Q = divide(points, m)
    C = []
    for i in range(len(Q)):
        C.append(Graham(Q[i]))

    curr = (0, 0)
    ans = []
    i = 0
    while i < m:
        ans.append(C[curr[0]][curr[1]])
        if nextvert(C, curr) == (0, 0):
            return ans
        curr = nextvert(C, curr)
        i += 1

    return None


def chan(points):
    n = len(points)
    m = 4
    hoax = None
    while hoax == None:
        hoax = chanUtil(points, m)
        m = min(n, m * m)

    return hoax