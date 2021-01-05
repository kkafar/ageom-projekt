# import math


# def divide(points, m):
#     n = len(points)
#     for i in range(1,
#                    n):  # gwarantuje, ze w pierwszym zbiorze Qi pierwszy element jest najnizszy, czyli nalezy do otoczki ostatecznej
#         if points[i][1] < points[0][1]:
#             buf = points[i]
#             points[i] = points[0]
#             points[0] = buf

#     k = math.ceil(n / m)
#     Q = [[] for i in range(k)]
#     i = 0
#     while i < n:
#         for j in range(k):
#             if i == n:
#                 break
#             Q[j].append(points[i])
#             i += 1
#     if len(Q[0]) > m:
#         return None

#     return Q
