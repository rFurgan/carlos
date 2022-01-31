from hero import Hero
from carla import Client
from gnss_receiver import GnssReceiver
from common.datatypes import EActorType
from common.exceptions import HeroError


class Api:
    def __init__(self, hero_id, host="127.0.0.1", port=2000):
        try:
            self._gnss_receivers = []
            self._hero = None
            self._client = Client(host, port)
            self._client.set_timeout(2.0)
            self._world = self._client.get_world()
            self._register_hero(hero_id)
        except RuntimeError:
            print(f"[ERROR] Failed to connect to CARLA world ${host}:${port}.")
            exit()
        except HeroError:
            print(
                f"[ERROR] Invalid hero id. Id either doesn't exist or actor is not a vehicle."
            )
            exit()
        else:
            self._register_gnss_receivers()

    def __del__(self):
        for gnss_receiver in self._gnss_receivers:
            del gnss_receiver
        del self._hero

    def _register_hero(self, hero_id):
        hero = self._world.get_actor(hero_id)
        if hero == None or not EActorType.VEHICLE.value in hero.type_id:
            raise (HeroError)
        self._hero = Hero(hero_id)

    def _register_gnss_receivers(self):
        for actor in self._world.get_actors():
            if (
                EActorType.VEHICLE.value in actor.type_id
                or EActorType.PEDESTRIAN.value in actor.type_id
            ):
                self._gnss_receivers.append(
                    GnssReceiver(
                        actor,
                        self._hero.on_position_data,
                        2,
                    )
                )
