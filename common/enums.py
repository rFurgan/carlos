from enum import Enum


class EActorType(Enum):
    """
    Enum that holds the two different main types of traffic users 
    """
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"


class EVehicleType(Enum):
    """
    Enum that holds the different types of vehicles 
    """
    MOTORCYCLE = "motorcycle"
    TRUCK = "truck"
    BIKE = "bike"
    CAR = "car"
