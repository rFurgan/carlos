import logging
import sys
import time
import csv
import math_operations as mo
from hero import Hero
from actor import Actor
from carla import Client
from common import EActorType, Coordinate, VehicleTypes, ROAD_USER_CODE
from datetime import datetime
from threading import Thread


class Api:
    def __init__(self, host, port):
        self._actors = {}
        self._road_users = []
        self._stop = False
        self._thread = None
        self._hero = None
        self._header_written = False
        try:
            client = Client(host, port)
            client.set_timeout(2.0)
            world = client.get_world()
        except RuntimeError as error:
            logging.error(f"Something went wrong connecting: {error}")
            sys.exit(1)
        for actor in world.get_actors():
            if (
                EActorType.VEHICLE.value in actor.type_id
                or EActorType.PEDESTRIAN.value in actor.type_id
            ):
                if self._hero == None and mo.vector_length(actor.get_velocity()) > 0:
                    self._hero = Hero(actor.id, self._actors)
                self._road_users.append(actor)
                self._actors[actor.id] = Actor(
                    actor.id, self._classify_type(actor.type_id), 10
                )

    def start(self, tick):
        if self._hero == None:
            logging.error("No Hero initialized or found")
            sys.exit(1)
        self._thread = Thread(target=self._poll_data, args=[tick])
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._stop = True
        if self._thread != None:
            self._thread.join()

    def save_csv(self):
        with open(r"C:\Users\daydr\Desktop\data.csv", "a+", encoding="UTF-8") as f:
            writer = csv.writer(f)
            if not self._header_written:
                writer.writerow(self._header())
                self._header_written = True
            for actor_id in self._actors:
                writer.writerow(self._actors[actor_id].get_data())

    def _header(self):
        header = ["ID", "type"]
        header += self._data_header("velocity")
        header += self._data_header("orientation")
        header += self._data_header("angular_speed")
        header += self._data_header("distance_to_hero")
        header += self._data_header("angle_to_hero")
        return header

    def _data_header(self, data_type):
        header = []
        for count in range(10):
            header.append(f"{data_type}_{count}")
        return header

    def _poll_data(self, tick):
        while not self._stop:
            current_time = round(time.time(), 3)
            time_now = datetime.now()
            for actor in self._road_users:
                location = actor.get_transform().location
                timestamp = time_now.second + round(time_now.microsecond / 1000000, 3)
                self._hero.on_position_data(
                    actor.id,
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

    def _classify_type(self, actor_type):
        for category in list(VehicleTypes.types.keys()):
            for type in VehicleTypes.types[category]:
                if type in actor_type:
                    return ROAD_USER_CODE[category]
        return ROAD_USER_CODE[EActorType.PEDESTRIAN]
