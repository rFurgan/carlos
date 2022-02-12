import logging
from actor import Hero
from carla import Client
from gnss import GnssReceiver
from common import EActorType


class Api:
    def __init__(self, hero_id, host, port):
        try:
            self._gnss_receivers = []
            self._subscribers = []
            self._hero = None
            self._client = Client(host, port)
            self._client.set_timeout(2.0)
            self._world = self._client.get_world()
            self._register_hero(hero_id)
        except RuntimeError:
            logging.error(f"Failed to connect to CARLA world {host}:{port}.")
            exit()
        except ValueError:
            logging.error(
                f"Invalid hero id. Id either doesn't exist or actor is not a vehicle."
            )
            exit()
        else:
            self._register_gnss_receivers()

    def __del__(self):
        for gnss_receiver in self._gnss_receivers:
            gnss_receiver.stop()

    def subscribe(self, callback):
        self._subscribers.append(callback)

    # TODO Create database and access to it

    def _register_hero(self, hero_id):
        hero = self._world.get_actor(hero_id)
        if hero == None or not EActorType.VEHICLE.value in hero.type_id:
            raise (ValueError)
        self._hero = Hero(hero_id, 150, self._subscribers)

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
                        0.5,
                    )
                )
