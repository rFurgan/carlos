from enum import Enum
from typing import NamedTuple


class EActorType(Enum):
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"


class ETimestampType(Enum):
    BEFORE = "before"
    AFTER = "after"


class Vector(NamedTuple):
    x: float
    y: float
    z: float


class Coordinate(NamedTuple):
    x: float
    y: float
    z: float


class CalculatedData(NamedTuple):
    position: Coordinate
    orientation: int
    velocity: int
    distance_to_hero: float
    angle_to_hero: int


class Data(NamedTuple):
    id: int
    timestamp: float
    data: CalculatedData


class Recent:
    def __init__(self, previous=None, current=None):
        self.previous = previous
        self.current = current


# # TODO Check
# class HeroData(NamedTuple):
#     distance_to_hero: float
#     angle_to_hero: int


# # TODO Check
# class CloseTimestamp(NamedTuple):
#     timestamp: float
#     type: ETimestampType
