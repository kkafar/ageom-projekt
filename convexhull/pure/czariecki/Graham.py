from det import*

def Graham(points, accur=10 ** (-6)):
    lwst = min(points, key=lambda x: (x[1], x[0]))
    points.remove(lwst)

    ###sortowanie wzgledem katow
    import functools
    def compare(p, q):
        if det(lwst, p, q) > accur:
            return -1
        elif det(lwst, p, q) < (-accur):
            return 1
        else:
            return 0

    points.sort(key=functools.cmp_to_key(compare))


    from collections import deque
    stack = deque()
    stack.append(lwst)
    stack.append(points[0])
    vect = [lwst, points[0]]
    i = 1

    while (i < len(points)):
        if det(vect[0], vect[1], points[i]) > accur:
            stack.append(points[i])
            vect[0] = vect[1]
            vect[1] = points[i]
            i += 1


        elif det(vect[0], vect[1], points[i]) < (-accur):
            vect[1] = vect[0]
            stack.pop()  # usuniecie vect[1]
            stack.pop()  # usuniecie vect[0](niestety trzeba tak, zeby sie dostac nizej stosu)
            vect[0] = stack.pop()
            stack.append(vect[0])
            stack.append(vect[1])

        else:
            if length([vect[0], points[i]]) > length(vect):  # postepujemy analogicznie do wyzszego przypadku, chyba ze vect, to dwa pierwsze wierzcholki

                vect[1] = vect[0]
                stack.pop()  # usuniecie vect[1]
                if stack.pop() == lwst:  # usuniecie vect[0] i jednoczesne rozpatrzenie przypadku szczegolnego
                    vect[0] = lwst
                    vect[1] = points[i]
                    stack.append(vect[0])
                    stack.append(vect[1])
                vect[0] = stack.pop()
                stack.append(vect[0])
                stack.append(vect[1])
            else:
                i += 1
    points.append(lwst)
    return list(stack)
