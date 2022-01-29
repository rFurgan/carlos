from common.datatypes import Vector
from math import degrees, sqrt
from numpy import arccos


class Operations:
    @staticmethod
    def get_vector(point, foot):
        return Vector(
            x=point.longitude - foot.longitude,
            y=point.latitude - foot.latitude,
            z=point.altitude - foot.altitude,
        )

    @staticmethod
    def get_angle_to_y_axis(direction_vector):
        if direction_vector.x == 0 and direction_vector.y == 0:
            return None
        return int(
            degrees(
                arccos(
                    direction_vector.y
                    / sqrt(direction_vector.x ** 2 + direction_vector.y ** 2)
                )
            )
        )

    @staticmethod
    def get_velocity(distance_vector, timestamp_before, timestamp_after):
        distance = Operations.get_vector_length(distance_vector)
        distance_in_m = distance / 1000
        time_difference = abs(timestamp_after - timestamp_before)
        time_difference_in_h = time_difference / 3600
        return distance_in_m / time_difference_in_h

    @staticmethod
    def get_vector_length(vector):
        # Altitude / z coordinate is troublesome in CARLA
        # Changes on flat road and falsifies the calculations
        # return round(sqrt((vector.x ** 2) + (vector.y ** 2) + (vector.z ** 2)))
        return round(sqrt((vector.x ** 2) + (vector.y ** 2)))

    @staticmethod
    def get_cross_product(vector_1, vector_2):
        return (
            # TODO check if this is also troublesome with z-axis
            vector_1.x * vector_2.x + vector_1.y * vector_2.y + vector_1.z * vector_2.z
        )

    @staticmethod
    def get_angle_between_vectors(vector_1, vector_2):
        return int(
            arccos(
                Operations.get_cross_product(vector_1, vector_2)
                / (
                    Operations.get_vector_length(vector_1)
                    * Operations.get_vector_length(vector_2)
                )
            )
        )
