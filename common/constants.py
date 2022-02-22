from typing import Dict
from common import Vector
from .enums import EActorType, EVehicleType

Y_AXIS: Vector = Vector(0, 1, 0)

MAX_STORE_SIZE: int = 30

ROAD_USER_CODE: Dict[EVehicleType, int] = {
    EVehicleType.CAR: 0,
    EActorType.PEDESTRIAN: 1,
    EVehicleType.MOTORCYCLE: 2,
    EVehicleType.TRUCK: 3,
    EVehicleType.BIKE: 4,
}
