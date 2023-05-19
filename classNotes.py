from math import *
def path(p1, p2, size):
    d = dist(p1, p2)
    if d==0:
        return []
    ans = []
    bx = p2[0]- p1[0]
    by = p2[1] - p1[1]
    sx = size * bx / d
    sy = size * by / d

    tot = 0
    while tot < d:
        ans.append((p1[0] + sx * tot/d, p1[1] + sy*tot/d))
        tot += size

    return ans

print(path ( (10, 20), (200, 50), 10))