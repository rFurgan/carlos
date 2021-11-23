from carla.libcarla import Vector3D
from random import randint
import math

# TODO
# Comments


class RoadUser:
    def __init__(self, id, position, targetPosition, timestamp) -> None:
        self.__id = id
        self.__positions = {
            timestamp: self.__addDeviation(position),
            timestamp: self.__addDeviation(position),
        }
        self.__targetPosition = targetPosition
        self.__orientation = 0.0
        self.__velocity = 0.0
        self.__distance = 0.0

    def getId(self) -> int:
        return self.__id

    def getOrientation(self) -> float:
        return self.__orientation

    def getVelocity(self) -> float:
        return self.__velocity

    def getDistance(self) -> float:
        return self.__distance

    def setPosition(self, position, targetPosition, timestamp) -> None:
        if len(self.__positions) >= 2:
            del self.__positions[next(iter(self.__positions))]
        self.__positions[timestamp] = self.__addDeviation(position)
        self.__targetPosition = targetPosition
        self.__orientation = self.__vectorAngle()
        self.__velocity = self.__getVelocity()
        self.__distance = self.__vectorLength3D()

    def __addDeviation(self, position, deviation=10) -> Vector3D:
        position.x = position.x + randint(-deviation, deviation)
        position.y = position.y + randint(-deviation, deviation)
        position.z = position.z + randint(-deviation, deviation)
        return position

    def __getVelocity(self) -> float:
        timestamps = list(self.__positions.keys())
        if len(timestamps) >= 2:
            return self.__vectorLength3D() / (timestamps[1] - timestamps[0])
        print(
            f"[ERROR][{self.__getVelocity.__name__}] Couldn't calculate due to insufficient data!"
        )
        return 0.0

    def __vectorLength3D(self) -> float:
        timestamps = list(self.__positions.keys())
        if len(timestamps) >= 2:
            x = self.__targetPosition.x - self.__positions[timestamps[1]].x
            y = self.__targetPosition.y - self.__positions[timestamps[1]].y
            z = self.__targetPosition.z - self.__positions[timestamps[1]].z
            return math.sqrt((x * x) + (y * y) + (z * z))
        print(
            f"[ERROR][{self.__vectorLength3D.__name__}] Couldn't calculate due to insufficient data!"
        )
        return 0.0

    def __vectorAngle(self) -> float:
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
            f"[ERROR][{self.__vectorAngle.__name__}] Couldn't calculate due to insufficient data!"
        )
        return 0.0
