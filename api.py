from carla import Client
from hero import Hero
from datatypes import EActorType
from gnss_receiver import GnssReceiver

class Api:
    def __init__(self):
        self._host = "127.0.0.1"
        self._port = 2000
        self._hero = None
        self._gnss_receivers = {}

    def start(self, hero_id):
        self._connect(self._host, self._port)
        self._register_hero(hero_id)
        self._register_gnss_receiver()

    def subscribe(self, callback):
        if (self._hero != None):
            self._hero.subscribe(callback)
        else:
            print(f"[ERROR] Call 'subscribe' after 'start'. Hero not initialized yet.")
            exit()

    def _connect(self, host, port):
        try:
            self._client = Client(host, port)
            self._client.set_timeout(2.0)
            self._world = self._client.get_world()
        except RuntimeError:
            print(f"[ERROR] Failed to connect to CARLA world ${host}:${port}.")
            exit()

    def _register_hero(self, hero_id):
        hero = self._world.get_actor(hero_id)
        if hero == None:
            print(
                f"[ERROR] Hero with the id '{hero_id}' doesn't exit."
            )
            exit()
        self._hero = Hero(hero_id, 100)

    def _register_gnss_receiver(self):
        for actor in self._world.get_actors():
            if (
                EActorType.VEHICLE.value in actor.type_id
                or EActorType.PEDESTRIAN.value in actor.type_id
            ):
                self._gnss_receivers[actor.id] = GnssReceiver(
                    actor, self._world, self._hero.on_position_data
                )
