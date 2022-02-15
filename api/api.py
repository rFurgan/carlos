import mariadb
import logging
import sys
from actor import Hero
from carla import Client
from gnss import GnssReceiver
from common import EActorType


class Api:
    def __init__(self):
        self._gnss_receivers = []
        self._subscribers = []
        self._hero = None
        self._cursor = None
        self._database = None

    def __del__(self):
        for gnss_receiver in self._gnss_receivers:
            gnss_receiver.stop()
        self._database.close()

    def subscribe(self, callback):
        self._subscribers.append(callback)

    def start(
        self,
        hero_id,
        sim_host,
        sim_port,
        db_user,
        db_password,
        db_host,
        db_port,
        db_override,
        db_name="carla",
    ):
        self._connect_to_simulation(sim_host, sim_port)
        self._database = self._connect_to_database(
            db_user, db_password, db_host, db_port
        )
        self._cursor = self._database.cursor()
        self._create_database(db_override, db_name)
        self._register_hero(hero_id)
        self._register_gnss_receivers()
        return self._database

    def _connect_to_simulation(self, host, port):
        try:
            self._client = Client(host, port)
            self._client.set_timeout(2.0)
            self._world = self._client.get_world()
        except RuntimeError:
            logging.error(f"Failed to connect to CARLA world {host}:{port}.")
            sys.exit(1)
        except ValueError:
            logging.error(
                f"Invalid hero id. Id either doesn't exist or actor is not a vehicle."
            )
            sys.exit(1)

    def _connect_to_database(self, user, password, host, port):
        try:
            self._database = mariadb.connect(
                user=user,
                password=password,
                host=host,
                port=port,
            )
        except mariadb.Error as error:
            print(f"An error occurred while connecting to the database: {error}")
            sys.exit(1)
        return self._database

    def _create_database(self, override, name="carla"):
        if override:
            self._cursor.execute(f"DROP DATABASE IF EXISTS {name}")
        self._cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name}")
        self._cursor.execute(f"USE {name}")

    def _register_hero(self, hero_id):
        hero = self._world.get_actor(hero_id)
        if hero == None or not EActorType.VEHICLE.value in hero.type_id:
            raise (ValueError)
        self._hero = Hero(hero_id, 150, self._subscribers, self._cursor, self._database)

    def _register_gnss_receivers(self):
        for actor in self._world.get_actors():
            if (
                EActorType.VEHICLE.value in actor.type_id
                or EActorType.PEDESTRIAN.value in actor.type_id
            ):
                self._cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS actor_{actor.id} (pkTimestamp FLOAT NOT NULL, orientation INT, velocity INT, distance_to_hero INT, angle_to_hero INT, PRIMARY KEY (pkTimestamp));"
                )
                self._gnss_receivers.append(
                    GnssReceiver(
                        actor,
                        self._hero.on_position_data,
                        0.5,
                    )
                )
