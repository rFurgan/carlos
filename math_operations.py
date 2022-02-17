from common import Vector, Y_AXIS
from math import atan2, degrees, sqrt


def vector(point, foot):
    return Vector(
        x=point.x - foot.x,
        y=point.y - foot.y,
        z=point.z - foot.z,
    )


def dot_product(a, b):
    return a.x * b.x + a.y * b.y


def determinant(a, b):
    return a.x * b.y - a.y * b.x


def vector_length(v):
    return round(sqrt((v.x ** 2) + (v.y ** 2) + (v.z ** 2)), 2)


def velocity(v, t_before, t_after):
    delta_t = abs(t_after - t_before)
    d = vector_length(v)
    return round((d / delta_t) * 3.6, 2)


def angle_to_y_axis(v):
    if v.x == 0 and v.y == 0:
        return None
    dot = dot_product(Y_AXIS, v)
    det = determinant(Y_AXIS, v)
    angle = round(degrees(atan2(det, dot)), 2)
    return angle if angle >= 0 else 360 + angle


def angle_between_vectors(a, b):
    dot = dot_product(a, b)
    det = determinant(a, b)
    angle = round(degrees(atan2(det, dot)), 2)
    return angle if angle >= 0 else 360 + angle


def angular_speed(angle_a, angle_b, t_before, t_after):
    delta_theta = abs(angle_a - angle_b)
    delta_t = abs(t_after - t_before)
    return round(delta_theta / delta_t, 2)
