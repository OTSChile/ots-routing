from itertools import combinations
from models.point import Point

def held_karp(points):
    n = len(points)
    C = {}

    # Initialize for subsets of one element
    for k in range(1, n - 1):
        C[(1 << k, k)] = (Point.distance_to(points[0], points[k]), 0)

    # Iterate over subsets of size 2 to n-1 (excluding final point)
    for subset_size in range(2, n - 1):
        for subset in combinations(range(1, n - 1), subset_size):
            bits = sum(1 << bit for bit in subset)
            for k in subset:
                prev = bits & ~(1 << k)
                res = [(C[(prev, m)][0] + Point.distance_to(points[m], points[k]), m) for m in subset if m != k]
                C[(bits, k)] = min(res, key=lambda x: x[0])

    # Connect with the final point
    bits = (2 ** (n - 1) - 2)  # Exclude the final point
    res = [(C[(bits, k)][0] + Point.distance_to(points[k], points[-1]), k) for k in range(1, n - 1)]
    opt, parent = min(res, key=lambda x: x[0])

    # Reconstruct the optimal path
    path = [0]
    for i in range(n - 2):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits
    path.append(n - 1)

    return opt, list(reversed(path))