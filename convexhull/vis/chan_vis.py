from random import randint
from copy import deepcopy
from lib.det import *
from lib.tangent import *
from lib.util import *
from pure.graham import graham
import matplotlib.colors as mcolors
from lib.geometric_tool_lab import *


def randomColor():
    return list(mcolors.CSS4_COLORS)[randint(0, len(list(mcolors.CSS4_COLORS)) - 1)]


def compr(p, q, current,
          accur=10 ** (-7)):  # jezeli p jest po prawej  odcinka [current,q] - jest 'wiekszy', to zwracamy 1
    if det(current, p, q) >= accur:
        return -1
    elif det(current, p, q) <= accur:
        return 1
    else:
        return 0


def nextvert(C, curr, plot=None, ans=None,
             points=None,accur=10**(-7)):  # dla danego punktu wspolzednymi z Q[i][j] jesli jest to punkt nalezacy do finalnej otoczki, to
    # zwraca nastepny punkt nalezacy do finalnej otoczki zadanego w takich samych wspolzednych Q[nxt[0]][nxt[1]]
    i, j = curr
    nxt = (i, (j + 1) % len(C[i]))
    for k in range(len(C)):
        if k == i:
            continue

        t = tangent_r(C[i][j], C[k])
        if t == None:
            print("zle")
            continue

        if plot != None:
            plot.add_scene(
                Scene(points=[PointsCollection(points), PointsCollection(np.copy(ans), color='green'),
                              PointsCollection(C[k], color='red'),
                              PointsCollection([C[k][t]], color='black'),
                              PointsCollection([C[nxt[0]][nxt[1]]], color='violet')],
                      lines=[LinesCollection(makeSheaf(ans), color='yellow'),
                             LinesCollection([[ans[len(ans) - 1], C[nxt[0]][nxt[1]]]], color='violet'),
                             LinesCollection([[ans[len(ans) - 1], C[k][t]]], color='firebrick'),
                             LinesCollection(makeFullSheaf(C[k]), color='red')]))

       # if compr(C[nxt[0]][nxt[1]], C[k][t], C[i][j]) > 0 and (k, t) != (curr):
        #    nxt = (k, t)
        if  det(C[i][j],C[nxt[0]][nxt[1]],C[k][t])<accur and (k,t)!=(curr):
            if det(C[i][j],C[nxt[0]][nxt[1]],C[k][t])>-accur:
                if length([C[k][t],C[i][j]]) <= length([C[nxt[0]][nxt[1]],C[i][j]]):
                    continue
            nxt=(k,t)

    return nxt


def chanUtil(points, m, plot=None):
    Q = divide(points, m)
    C = []
    for i in range(len(Q)):
        C.append(graham(Q[i]))

    if plot != None:
        Color=[randomColor() for i in range(len(Q))]
        pkt = [PointsCollection(Q[i], color=Color[i]) for i in range(len(Q))]

        plot.add_scene(Scene(points=pkt))

        lns = [LinesCollection(makeFullSheaf(C[i]), color=Color[i]) for i in range(len(C))]
        pkt = [PointsCollection(C[i],color=Color[i]) for i in range(len(Q))]

        plot.add_scene(Scene(points=pkt, lines=lns))

    curr = (0, 0)
    ans = []
    i = 0

    while i < m:
        ans.append(C[curr[0]][curr[1]])
        if plot != None:
            plot.add_scene(
                Scene(points=[PointsCollection(points), PointsCollection(np.copy(ans), color='green')],
                      lines=[LinesCollection(makeSheaf(ans), color='yellow')]))

        nxt = nextvert(C, curr, plot, ans, points)
        if nxt == (0, 0):
            return ans
        curr = nxt
        i += 1

    return None


def chan_vis(points, visual=False):
    plot = None
    if visual:
        plot = Plot(scenes=[Scene(points=[PointsCollection(points)])])
    n = len(points)
    m = 4
    hoax = None
    while hoax == None:
        hoax = chanUtil(points, m, plot)
        m = min(n, m * m)

    if visual == True:
        plot.add_scene(Scene(points=[PointsCollection(points), PointsCollection(hoax, color='green')],
                             lines=[LinesCollection(makeFullSheaf(hoax), color='yellow')]))
        return plot

    return hoax


