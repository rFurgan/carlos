from datatypes import Vector
from math import degrees, sqrt
from numpy import arccos


class DataCalculator:
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
        distance = DataCalculator.get_vector_length(distance_vector)
        time_difference = timestamp_after - timestamp_before
        return distance / time_difference

    @staticmethod
    def get_vector_length(vector):
        return round(sqrt((vector.x ** 2) + (vector.y ** 2) + (vector.z ** 2)))

    @staticmethod
    def get_cross_product(vector_1, vector_2):
        return (
            vector_1.x * vector_2.x + vector_1.y * vector_2.y + vector_1.z * vector_2.z
        )

    @staticmethod
    def get_angle_between_vectors(vector_1, vector_2):
        return int(
            arccos(
                DataCalculator.get_cross_product(vector_1, vector_2)
                / (
                    DataCalculator.get_vector_length(vector_1)
                    * DataCalculator.get_vector_length(vector_2)
                )
            )
        )
