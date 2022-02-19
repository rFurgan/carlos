from common import Vector, Y_AXIS
from math import atan2, degrees, sqrt


def vector(point, foot):
    """Converts and returns a vector from the two given points 

    Args:
    point (Coordinate): Point the vector points to
    foot (Coordinate): Point the vector starts from

    Returns:
        Vector: Vector with the start at foot and end at point
    """
    return Vector(
        x=point.x - foot.x,
        y=point.y - foot.y,
        z=point.z - foot.z,
    )


def dot_product(vector_a, vector_b):
    """Calculates and returns the dot product of two given vectors 

    Args:
        vector_a (Vector): First vector to calculate dot product
        vector_b (Vector): Second vector to calculate dot product

    Returns:
        float: Result of the dot product between vector_a and vector_b
    """
    return vector_a.x * vector_b.x + vector_a.y * vector_b.y


def determinant(vector_a, vector_b):
    """Calculates and returns the determinant of two given vectors 

    Args:
        vector_a (Vector): First vector to calculate determinant
        vector_b (Vector): Second vector to calculate determinant

    Returns:
        float: Determinant of vector_a and vector_b
    """
    return vector_a.x * vector_b.y - vector_a.y * vector_b.x


def vector_length(vector_v):
    """Calculates and returns the of the given vectors 

    Args:
        vector_v (Vector): Vector to calculate the length of

    Returns:
        float: Length of the vector
    """
    return round(sqrt((vector_v.x ** 2) + (vector_v.y ** 2) + (vector_v.z ** 2)), 2)


def velocity(vector_v, t_before, t_after):
    """Calculates and returns the velocity from the given vector and timestamps (in km/h)

    Args:
        v (Vector): Represents the covered distance (in m)
        t_before (float): Timestamp of the position before (in s)
        t_after (float): Timestamp of the position afterwards (in s)

    Returns:
        float: Velocity from the given vector and timestamps (in km/h)
    """
    delta_t = abs(t_after - t_before)
    d = vector_length(vector_v)
    return round((d / delta_t) * 3.6, 2)


def angle_to_y_axis(vector_v):
    """Calculates and returns the angle to y-axis (0-360 degrees)

    Args:
        vector_v (Vector): Vector to calculate the angle between the y-axis (in m)

    Returns:
        float: Angle between given vector and y-axis (0-360 degrees)
        None: Given vector has the length 0 and therefore cannot calculate the angle
    """
    if vector_v.x == 0 and vector_v.y == 0:
        return None
    dot = dot_product(Y_AXIS, vector_v)
    det = determinant(Y_AXIS, vector_v)
    angle = round(degrees(atan2(det, dot)), 2)
    return angle if angle >= 0 else 360 + angle


def angle_between_vectors(vector_a, vector_b):
    """Calculates and returns the angle between two given vectors (0-360 degrees)

    Args:
        vector_a (Vector): First vector to calculate the angle between
        vector_b (Vector): Second vector to calculate the angle between

    Returns:
        float: Angle between the given vectors (0-360 degrees)
    """
    dot = dot_product(vector_a, vector_b)
    det = determinant(vector_a, vector_b)
    angle = round(degrees(atan2(det, dot)), 2)
    return angle if angle >= 0 else 360 + angle


def angular_speed(angle_a, angle_b, t_before, t_after):
    """Calculates and returns the angular speed between the given angles and the corresponding timestamps

    Args:
        angle_a (float): First angle to calculate the speed between
        angle_b (float): Second angle to calculate the speed between
        t_before (float): Timestamp before the change of the angle
        t_after (float): Timestamp after the change of the angle

    Returns:
        float: Angular speed to turn from angle_a to angle_b between the given timestamps
    """
    delta_theta = abs(angle_a - angle_b)
    delta_t = abs(t_after - t_before)
    return round(delta_theta / delta_t, 2)
