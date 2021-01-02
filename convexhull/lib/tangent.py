from lib.det import*

def tangent(p, Q, accur=0):  # Q-zbior punktow w formie otoczki
    # wykorzystujemy binary search na otoczce - jesli dany wierzcholek jest po prawej stronie punktu tworzacej styczna
    # lewostronna z p,
    ln = len(Q)

    def tangetUtil(p, Q, l, r):
        if r < l:  # zdarza sie tylko, gdy punkt jest wewnatrz otoczki
            return None

        mid = (l + r) // 2
        if det(Q[0], Q[1], p) > 0 and det(Q[ln - 1], Q[0], p) > 0:
            if (det(Q[0], p, Q[mid]) < 0) or (det(p, Q[mid], Q[(mid + 1) % ln]) < 0 and \
                                              det(p, Q[mid], Q[(mid - 1) % ln]) < 0) or \
                    (det(p, Q[mid], Q[(mid + 1) % ln]) < 0 and det(p, Q[mid], Q[(mid - 1) % ln]) >= 0):
                return tangetUtil(p, Q, mid + 1, r)

        else:
            if det(Q[0], p, Q[mid]) >= 0 and \
                    ((det(p, Q[mid], Q[(mid + 1) % ln]) < 0 and det(p, Q[mid], Q[(mid - 1) % ln]) >= 0) or \
                     (det(p, Q[mid], Q[(mid + 1) % ln]) < 0 and det(p, Q[mid], Q[
                         (mid - 1) % ln]) < 0)):  # chyba nie potrzebne sprawdz na koncu
                return tangetUtil(p, Q, mid + 1, r)

        if det(p, Q[mid], Q[(mid + 1) % ln]) >= 0 and det(p, Q[mid], Q[(mid - 1) % ln]) >= 0 \
                or (det(p, Q[mid], Q[(mid + 1) % ln]) == 0 and (Q[mid][0] <= p[0] <= Q[(mid + 1) % ln][0]) and \
                    (Q[mid][1] <= p[1] <= Q[(mid + 1) % ln][1])):

            while (det(p, Q[mid], Q[(mid + 1) % ln]) == 0):
                mid = (mid + 1) % ln  # jesli jest styczna wspolliniowa, to bierzmy pod uwage punkt blizszy
            return mid

        else:
            return tangetUtil(p, Q, l, mid - 1)

    return tangetUtil(p, Q, 0, ln - 1)