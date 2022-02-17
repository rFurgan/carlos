from common import Vector
from .enums import EActorType, EVehicleType

Y_AXIS = Vector(0, 1, 0)

MAX_STORE_SIZE = 30

REMOTE_HOST = "feif-pc351b"
REMOTE_PORT = 4000

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 2000

DB_USER = "root"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = 3306

ROAD_USER_CODE = {
    EVehicleType.CAR: 0,
    EActorType.PEDESTRIAN: 1,
    EVehicleType.MOTORCYCLE: 2,
    EVehicleType.TRUCK: 3,
    EVehicleType.BIKE: 4,
}
