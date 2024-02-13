def find_furthest_point(reference_point, other_points):
    furthest_point = None
    max_distance = 0

    for point in other_points:
        distance = reference_point.distance_to(point)
        if distance > max_distance:
            max_distance = distance
            furthest_point = point

    return furthest_point, max_distance