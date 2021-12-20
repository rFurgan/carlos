from road_users.road_user import RoadUser
from common.road_user_data import RoadUserData

# TODO Docstring
# TODO Check how to document inheritance


class Hero(RoadUser):
    """
    id: int
    actor: Actor
    world: World
    hero_callbacks: Callback[]
    """

    def __init__(self, actor, world, hero_callbacks):
        super().__init__(actor, world)
        self._data = {}
        self._hero_callbacks = hero_callbacks

    """
    timestamp: float
    position: Vector3D
    """

    def on_data(self, timestamp, position):
        self._data[timestamp] = RoadUserData(self._data, timestamp, position, True)
        for hero_callback in self._hero_callbacks:
            hero_callback(timestamp, position)
