from carla.libcarla import Vector3D
from random import randint
import math

# TODO
# Comments


class RoadUser:
    def __init__(self, id, position, target_position, timestamp) -> None:
        self.__id = id
        self.__positions = {
            timestamp: self.__add_deviation(position),
            timestamp: self.__add_deviation(position),
        }
        self.__target_position = target_position
        self.__orientation = 0.0
        self.__velocity = 0.0
        self.__distance = 0.0

    def get_id(self) -> int:
        return self.__id

    def get_orientation(self) -> float:
        return self.__orientation

    def get_velocity(self) -> float:
        return self.__velocity

    def get_distance(self) -> float:
        return self.__distance

    def set_position(self, position, target_position, timestamp) -> None:
        if len(self.__positions) >= 2:
            del self.__positions[next(iter(self.__positions))]
        self.__positions[timestamp] = self.__add_deviation(position)
        self.__target_position = target_position
        self.__orientation = self.__vector_angle()
        self.__velocity = self.__get_velocity()
        self.__distance = self.__vector_length()

    def __add_deviation(self, position, deviation=10) -> Vector3D:
        position.x = position.x + randint(-deviation, deviation)
        position.y = position.y + randint(-deviation, deviation)
        position.z = position.z + randint(-deviation, deviation)
        return position

    def __get_velocity(self) -> float:
        timestamps = list(self.__positions.keys())
        if len(timestamps) >= 2:
            return self.__vectorLength() / (timestamps[1] - timestamps[0])
        print(
            f"[ERROR][{self.__get_velocity.__name__}] Couldn't calculate the velocity due to insufficient data!"
        )
        return 0.0

    def __vector_length(self) -> float:
        timestamps = list(self.__positions.keys())
        if len(timestamps) >= 2:
            x = self.__target_position.x - self.__positions[timestamps[1]].x
            y = self.__target_position.y - self.__positions[timestamps[1]].y
            z = self.__target_position.z - self.__positions[timestamps[1]].z
            return math.sqrt((x * x) + (y * y) + (z * z))
        print(
            f"[ERROR][{self.__vector_length.__name__}] Couldn't calculate the vector length due to insufficient data!"
        )
        return 0.0

    def __vector_angle(self) -> float:
        timestamps = list(self.__positions.keys())
        if len(timestamps) >= 2:
            opposite = abs(
                self.__positions[timestamps[1]].x - self.__positions[timestamps[0]].x
            )
            adjacent = abs(
                self.__positions[timestamps[1]].y - self.__positions[timestamps[0]].y
            )
            return math.atan2(opposite, adjacent)
        print(
            f"[ERROR][{self.__vector_angle.__name__}] Couldn't calculate the vector angle due to insufficient data!"
        )
        return 0.0
