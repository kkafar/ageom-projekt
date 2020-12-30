def det(a,b,c):
    return a[0]*b[1]-a[0]*c[1]-b[0]*a[1]+b[0]*c[1]+c[0]*a[1]-c[0]*b[1]


def length(v):
    return np.sqrt((v[1][0] - v[0][0]) ** 2 + (v[1][1] - v[0][1]) ** 2)