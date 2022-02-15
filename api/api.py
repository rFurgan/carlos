import mariadb
import logging
import sys
import time
from datetime import datetime
from actor import Hero
from carla import Client
from common import VehicleTypes, EActorType, Coordinate
from threading import Thread


class Api:
    def __init__(self):
        self._subscribers = []
        self._hero = None
        self._cursor = None
        self._database = None
        self._thread = None
        self._stop = False

    def __del__(self):
        self._stop = True
        if self._database != None:
            self._database.close()
        if self._thread != None:
            self._thread.join()

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
        self._register_types()
        self._register_hero(hero_id)
        self._thread = Thread(target=self._register_gnss_receivers)
        self._thread.daemon = True
        self._thread.start()
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

    def _register_types(self):
        self._cursor.execute(
            f"CREATE TABLE IF NOT EXISTS actors (pkId VARCHAR(255) NOT NULL, type VARCHAR(255) NOT NULL, PRIMARY KEY (pkId));"
        )
        for actor in self._world.get_actors():
            self._cursor.execute(
                f"INSERT INTO actors VALUES('{actor.id}', '{self._classify(actor.type_id)}')"
            )
        self._database.commit()

    def _register_gnss_receivers(self):
        tick = 0.5
        while not self._stop:
            current_time = round(time.time(), 3)
            time_now = datetime.now()
            for actor in self._world.get_actors():
                if (
                    EActorType.VEHICLE.value in actor.type_id
                    or EActorType.PEDESTRIAN.value in actor.type_id
                ):
                    self._cursor.execute(
                        f"CREATE TABLE IF NOT EXISTS actor_{actor.id} (pkTimestamp FLOAT NOT NULL, orientation INT, velocity INT, distance_to_hero INT, angle_to_hero INT, PRIMARY KEY (pkTimestamp));"
                    )
                    location = actor.get_transform().location
                    timestamp = time_now.second + round(
                        time_now.microsecond / 1000000, 3
                    )
                    self._hero.on_position_data(
                        actor.id,
                        self._classify(actor.type_id),
                        timestamp,
                        Coordinate(
                            x=location.x,
                            y=location.y,
                            z=location.z,
                        ),
                    )
            rest_time = round(time.time(), 3) - current_time
            rest_sleep = tick - rest_time
            if rest_sleep > 0:
                time.sleep(tick)

    def _classify(self, actor_type):
        for category in list(VehicleTypes.types.keys()):
            for type in VehicleTypes.types[category]:
                if type in actor_type:
                    return category.value
        return EActorType.PEDESTRIAN.value
