from typing import Dict
from common import Vector
from .enums import EActorType, EVehicleType

Y_AXIS: Vector = Vector(0, 1, 0)

MAX_STORE_SIZE: int = 30

REMOTE_HOST: str = "feif-pc351b"
REMOTE_PORT: int = 4000

LOCAL_HOST: str = "127.0.0.1"
LOCAL_PORT: int = 2000

DB_USER: str = "root"
DB_PASSWORD: str = "1234"
DB_HOST: str = "localhost"
DB_PORT: int = 3306

ROAD_USER_CODE: Dict[EVehicleType, int] = {
    EVehicleType.CAR: 0,
    EActorType.PEDESTRIAN: 1,
    EVehicleType.MOTORCYCLE: 2,
    EVehicleType.TRUCK: 3,
    EVehicleType.BIKE: 4,
}
