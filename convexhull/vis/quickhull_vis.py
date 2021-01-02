from copy import deepcopy
from det import *
def furthest(a, b, considering):
    n = len(considering)
    i = 0
    ans = None
    while i < n:
        if det(a, b, considering[i]) < 0:  # rozwazany wierzcholek jest po prawej stronie ab
            if ans == None or det(a, b, considering[i]) < det(a, b,
                                                              ans):  # |det(a,b,c)| = 1/2|ab|*h, gdzie h jest wysokoscia z c na ab
                ans = considering[i]
        i += 1
    return ans


def insideTriangle(a, b, c, i):
    accur = 10 ** (-7)
    if det(a, b, i) > -accur and det(b, c, i) > -accur and det(c, a, i) > -accur:
        return True
    return False


def removeInner(a, b, c, considering):
    new = []
    for i in considering:
        if not insideTriangle(a, b, c, i):
            new.append(i)
    considering.clear()
    considering += new


def quickHullUtil(a, b, considering, plot=None, hull=None):
    if len(considering) == 0:
        return []

    if plot != None:
        plot.add_scene(Scene(points=[PointsCollection(deepcopy(considering)),
                                     PointsCollection(deepcopy(hull), color='green')],
                             lines=[LinesCollection([[a, b]], color='yellow')]))

    c = furthest(a, b, considering)
    if c == None:
        return []
    considering.remove(c)

    if plot != None:
        hull.append(c)
        plot.add_scene(Scene(points=[PointsCollection(deepcopy(considering)),
                                     PointsCollection(deepcopy(hull), color='green'),
                                     PointsCollection([c], color='red')],
                             lines=[LinesCollection([[a, b]], color='yellow')]))

    if plot != None:
        plot.add_scene(Scene(points=[PointsCollection(deepcopy(considering), color='blue'),
                                     PointsCollection(deepcopy(hull), color='green')],
                             lines=[LinesCollection([[a, c], [b, c]], color='yellow')]))

    removeInner(a, c, b, considering)

    if plot != None:
        plot.add_scene(Scene(points=[PointsCollection(deepcopy(considering), color='blue'),
                                     PointsCollection(deepcopy(hull), color='green')],
                             lines=[LinesCollection([[a, b], [a, c], [b, c]], color='yellow')]))

        z = quickHullUtil(a, c, considering, plot, hull)

        plot.add_scene(Scene(points=[PointsCollection(deepcopy(considering), color='blue'),
                                     PointsCollection(deepcopy(hull), color='green')],
                             lines=[LinesCollection([[b, c]], color='yellow')]))

        return z + [c] + quickHullUtil(c, b, considering, plot, hull)

    return quickHullUtil(a, c, considering) + [c] + quickHullUtil(c, b, considering)


def quickHull(points, visual=False):
    a = min(points, key=lambda x: x)
    b = max(points, key=lambda x: x)

    considering = deepcopy(points)

    if visual == True:
        plot = Plot(scenes=[Scene(points=[PointsCollection(deepcopy(considering), color='blue')])])
        plot.add_scene(Scene(points=[PointsCollection(deepcopy(considering), color='blue'),
                                     PointsCollection([a, b], color='red')]))

    considering.remove(a)
    considering.remove(b)

    if visual:
        hull = [a, b]
        hoax = [a] + quickHullUtil(a, b, considering, plot, hull) + [b] + quickHullUtil(b, a, considering, plot, hull)
        plot.add_scene(
            Scene(points=[PointsCollection(deepcopy(points)), PointsCollection(deepcopy(hoax), color='green')],
                  lines=[LinesCollection(makeFullSheaf(hoax), color='yellow')]))
        return plot

    return [a] + quickHullUtil(a, b, considering) + [b] + quickHullUtil(b, a, considering)