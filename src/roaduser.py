from carla.libcarla import Vector3D
from typing import Union, List
from random import randint
from json import dumps
from numpy import arccos
from math import degrees, sqrt

# TODO
# Comments


class RoadUser:
    def __init__(
        self, id: int, position: Vector3D, target_position: Vector3D, timestamp: str
    ) -> None:
        self.__id: int = id
        self.__positions: dict[str, Vector3D] = {
            timestamp: self.__add_deviation(position),
            timestamp: self.__add_deviation(position),
        }
        self.__target_position: Vector3D = target_position
        self.__orientation: Union[float, None] = None
        self.__velocity: Union[float, None] = None
        self.__distance: Union[float, None] = None

    def get_id(self) -> int:
        return self.__id

    def get_orientation(self) -> Union[float, None]:
        return self.__orientation

    def get_velocity(self) -> Union[float, None]:
        return self.__velocity

    def get_distance(self) -> Union[float, None]:
        return self.__distance

    def get_data(self) -> str:
        return dumps(
            {
                "id": self.__id,
                "distance": self.__distance,
                "velocity": self.__velocity,
                "orientation": self.__orientation,
            }
        )

    def set_position(
        self, position: Vector3D, target_position: Vector3D, timestamp: str
    ) -> None:
        if len(self.__positions) >= 2:
            del self.__positions[next(iter(self.__positions))]
        self.__positions[timestamp] = self.__add_deviation(position)
        self.__target_position = target_position
        self.__orientation = self.__vector_angle()
        self.__velocity = self.__get_velocity()
        self.__distance = self.__vector_length()

    # Need some investigation on how big the deviation actually is with GPS nowadays
    def __add_deviation(self, position: Vector3D, deviation: float = 0) -> Vector3D:
        position.x = position.x + randint(-deviation, deviation)
        position.y = position.y + randint(-deviation, deviation)
        position.z = position.z + randint(-deviation, deviation)
        return position

    def __get_velocity(self) -> Union[float, None]:
        timestamps: List[str] = list(self.__positions.keys())
        if len(timestamps) >= 2:
            return self.__vector_length() / (timestamps[1] - timestamps[0])
        print(
            f"[WARN][{self.__get_velocity.__name__}] Couldn't calculate the velocity due to insufficient data!"
        )
        return None

    def __vector_length(self) -> Union[float, None]:
        timestamps = list(self.__positions.keys())
        if len(timestamps) >= 2:
            x = self.__target_position.x - self.__positions[timestamps[1]].x
            y = self.__target_position.y - self.__positions[timestamps[1]].y
            z = self.__target_position.z - self.__positions[timestamps[1]].z
            return sqrt((x * x) + (y * y) + (z * z))
        print(
            f"[WARN][{self.__vector_length.__name__}] Couldn't calculate the vector length due to insufficient data!"
        )
        return None

    def __vector_angle(self) -> float:
        timestamps = list(self.__positions.keys())
        return degrees(
            arccos(
                self.__positions[timestamps[1]].y
                / sqrt(
                    self.__positions[timestamps[1]].x ** 2
                    + self.__positions[timestamps[1]].y ** 2
                )
            )
        )
