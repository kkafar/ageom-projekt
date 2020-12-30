from det import *

def Jarvis(Points2, accur=10 ** (-6)):
    from copy import deepcopy
    Points = deepcopy(Points2)

    ##############################funkcje do szukania najblizszego wzgletem kata do ostatniego boku punktu
    def compr(p, q, current):
        if det(current, p, q) > accur:
            return -1
        elif det(current, p, q) < (-accur):
            return 1
        else:
            return 0

    def nextvert(p, ans=[], scenes=[]):
        nxt = Points[0]
        for i in range(1, len(Points)):
            if (compr(nxt, Points[i], p) > 0):
                nxt = Points[i]
        return nxt

    lwst = min(Points, key=lambda x: (x[1], x[0]))
    ans = []
    ans.append(lwst)
    Points.remove(lwst)
    p = nextvert(lwst)
    Points.append(lwst)
    ans.append(p)
    vect = [lwst, p]


    if scen:
        p = nextvert(p, ans, scenes)
    else:
        p = nextvert(p)
    while (p != ans[0]):

        # begin
        #######################################################################
        if scen:
            scenes.append(Scene([PointsCollection(Points2),
                                 PointsCollection(ans, color='green')],
                                [LinesCollection(makeSheaf(ans), color='green')]))
        ########################################################################
        if -accur < det(vect[0], vect[1], p) < accur:
            if length([vect[0], p]) <= length([vect[0], vect[1]]):
                Points.remove(p)
            else:
                ans.remove(vect[1])
                vect[1] = p
                ans.append(vect[1])
            if scen:
                p = nextvert(p, ans, scenes)
            else:
                p = nextvert(p)
            continue

        Points.remove(p)
        ans.append(p)

        vect[0] = vect[1]
        vect[1] = p
        if scen:
            p = nextvert(p, ans, scenes)
        else:
            p = nextvert(p, ans)


    return ans