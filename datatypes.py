from enum import Enum
from typing import NamedTuple


class EActorType(Enum):
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"


class Vector(NamedTuple):
    x: float
    y: float
    z: float


class Geoposition(NamedTuple):
    longitude: float
    latitude: float
    altitude: float


class Data(NamedTuple):
    id: int
    type: EActorType
    position: Geoposition
    orientation: int
    velocity: int
    distance_to_hero: float
    angle_to_hero: int


class HeroData(NamedTuple):
    distance_to_hero: float
    angle_to_hero: int
