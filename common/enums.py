from enum import Enum


class EActorType(Enum):
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"


class ETimestampType(Enum):
    BEFORE = "before"
    AFTER = "after"


class EVehicleType(Enum):
    MOTORCYCLE = "motorcycle"
    TRUCK = "truck"
    BIKE = "bike"
    CAR = "car"
