from carla import Client
from common.logger import Logger
from road_users.road_user import RoadUser
from road_users.hero import Hero
from sys import exit
from json import dumps

# TODO Docstring


class EType(enumerate):
    vehicle = "vehicle"
    pedestrian = "pedestrian"


class Carlos:
    """
    return
        None
    """

    def __init__(self, argv):
        self._logger = Logger(Carlos.__name__)
        self._hero = None
        self._world = None
        self._client = None
        self._road_users = {}
        try:
            if len(argv) <= 1:
                raise ValueError
            self._hero_id = int(argv[1])
        except ValueError:
            self._logger.error("Hero id missing or not an Integer. Exiting program")
            exit()

    """
    return
        None
    """

    def __del__(self):
        self._destroy_actors()

    """
    hero_id: int
    host: str (default="127.0.0.1")
    port: int (default=2000)

    return
        None
    """

    def start(self, host="127.0.0.1", port=2000):
        self._connect(host, port)
        self._register_actors(self._hero_id)

    """
    id: int (default = None)

    return str
    """

    def get_data(self, id=None) -> str:
        if id == None:
            dataset = {}
            for ru_id in self._road_users:
                dataset[ru_id] = self._road_users[ru_id].get_data()
            return dumps(dataset, indent=4)
        return dumps(self._road_users[id].get_data(), indent=4)

    """
    id: int (default = None)

    return str
    """

    def get_latest_data(self, id=None) -> str:
        if id == None:
            dataset = {}
            for ru_id in self._road_users:
                dataset[ru_id] = self._road_users[ru_id].get_latest_data()
            return dumps(dataset, indent=4)
        return dumps(self._road_users[id].get_latest_data(), indent=4)

    """
    host: str
    port: int

    return
        None
    """

    def _connect(self, host, port):
        try:
            self._logger.info(f"Connecting to world '{host}:{port}'")
            if self._client == None:
                self._client = Client(host, port)
                self._client.set_timeout(2.0)
            if self._world == None:
                self._world = self._client.get_world()
            self._logger.info(f"Connected successfully")
        except RuntimeError:
            self._logger.error("Failed to connect to host world. Exiting program")
            exit()

    """
    hero_id: int

    return
        None
    """

    def _register_actors(self, hero_id) -> None:
        hero_callbacks = []
        if self._hero == None:
            hero_actor = self._world.get_actor(hero_id)
            if hero_actor != None:
                self._hero = Hero(hero_actor, self._world, hero_callbacks)
                self._road_users[hero_id] = self._hero
            else:
                self._logger.error("Hero id does not exist in current world")
                exit()
        else:
            self._logger.warn("Hero already registered")

        for actor in self._world.get_actors():
            if actor.id != hero_id and (
                EType.vehicle in actor.type_id or EType.pedestrian in actor.type_id
            ):
                self._road_users[actor.id] = RoadUser(actor, self._world)
                hero_callbacks.append(self._road_users[actor.id].on_hero_data)

    """
    return
        None
    """

    def _destroy_actors(self) -> None:
        for id in list(self._road_users):
            del self._road_users[id]
