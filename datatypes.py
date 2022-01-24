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


class Geoposition(NamedTuple):
    longitude: float
    latitude: float
    altitude: float


class CalculatedData(NamedTuple):
    position: Geoposition
    orientation: int
    velocity: int
    distance_to_hero: float
    angle_to_hero: int


class HeroData(NamedTuple):
    distance_to_hero: float
    angle_to_hero: int


class Data(NamedTuple):
    id: int
    timestamp: float
    data: CalculatedData


class CloseTimestamp(NamedTuple):
    timestamp: float
    type: ETimestampType
