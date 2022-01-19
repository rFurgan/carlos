from carla import Client
from road_user import RoadUser
from datatypes import EActorType


class Api:
    def __init__(self):
        self._road_users = {}
        self._client = None
        self._world = None

    def __del__(self):
        for id in list(self._road_users):
            del self._road_users[id]

    def start(self, hero_id, host="127.0.0.1", port=2000):
        self._connect(host, port)
        self._register_actors(hero_id)

    def _connect(self, host, port):
        try:
            self._client = Client(host, port)
            self._client.set_timeout(2.0)
            self._world = self._client.get_world()
        except RuntimeError:
            exit()

    def _register_actors(self, hero_id):
        hero = self._world.get_actor(hero_id)
        if hero == None:
            exit()
        self._road_users[hero_id] = RoadUser(hero_id, hero, self._world)
        for actor in self._world.get_actors():
            if actor.id != hero_id and (
                EActorType.VEHICLE.value in actor.type_id
                or EActorType.PEDESTRIAN.value in actor.type_id
            ):
                self._road_users[actor.id] = RoadUser(
                    actor.id, actor, self._world, self._road_users[hero_id]
                )
