from common import Vector, Y_AXIS
from math import atan2, degrees, sqrt


def get_vector(point, foot):
    return Vector(
        x=point.x - foot.x,
        y=point.y - foot.y,
        z=point.z - foot.z,
    )


def get_dot_product(a, b):
    return a.x * b.x + a.y * b.y


def get_determinant(a, b):
    return a.x * b.y - a.y * b.x


def get_vector_length(v):
    return round(sqrt((v.x ** 2) + (v.y ** 2) + (v.z ** 2)))


def get_velocity(v, t):
    d = get_vector_length(v)
    return round((d / t) * 3.6)


def get_angle_to_y_axis(v):
    if v.x == 0 and v.y == 0:
        return None
    dot = get_dot_product(Y_AXIS, v)
    det = get_determinant(Y_AXIS, v)
    angle = int(degrees(atan2(det, dot)))
    return angle if angle >= 0 else 360 + angle


def get_angle_between_vectors(a, b):
    dot = get_dot_product(a, b)
    det = get_determinant(a, b)
    return int(degrees(atan2(det, dot)))
