import logging
import sys
import time
import csv
import carla
import pathlib

from math_operations import MathOperations as mo
from hero import Hero
from actor import Actor
from typing import Dict, List, Union
from common import *
from datatypes import Subscription
from datetime import datetime
from threading import Thread


class Api:
    """Class that provides the access to the program as a whole

    Note:
        Only use this class to work with, the other classes are not to be accessed from the outside
        Refer to the example.py file for an example of the usage

    Args:
        host (string): Address of the host where the Carla world is running
        port (int): Port to the host where the Carla world is running
        relevance_radius (int): Radius of distance that filters out actors that are out of range from the hero
        max_entry_count (int): Amount of entries to be stored for CSV file to be created
        hero_id (int, optional): Id of the actor to be assigned as hero
    """

    def __init__(
        self,
        host: str,
        port: int,
        relevance_radius: float,
        max_entry_count: int,
        hero_id: int = -1,
    ) -> None:
        self._actors: Dict[int, Actor] = {}
        self._road_users: List[carla.Actor] = []
        self._subscribers: List[Subscription] = []
        self._stop: bool = False
        self._thread: Union[Thread, None] = None
        self._hero: Union[Hero, None] = None
        self._hero_id: int = hero_id
        self._relevance_radius: float = relevance_radius
        self._max_entry_count: int = max_entry_count
        self._header_written: bool = False
        try:
            client: carla.Client = carla.Client(host, port)
            client.set_timeout(5.0)
            world: carla.World = client.get_world()
        except RuntimeError as err:
            logging.error(f"Something went wrong connecting: {err}")
            sys.exit(1)
        for actor in world.get_actors():
            if (
                EActorType.VEHICLE.value in actor.type_id
                or EActorType.PEDESTRIAN.value in actor.type_id
            ):
                if self._hero_id != -1 and actor.id == self._hero_id:
                    self._hero = Hero(
                        actor.id,
                        self._actors,
                        self._subscribers,
                        self._relevance_radius,
                    )
                elif (
                    self._hero_id == -1
                    and self._hero == None
                    and actor.get_velocity() > 0
                ):
                    self._hero = Hero(
                        actor.id,
                        self._actors,
                        self._subscribers,
                        self._relevance_radius,
                    )
                self._road_users.append(actor)
                self._actors[actor.id] = Actor(
                    actor.id, self._classify_type(actor.type_id), self._max_entry_count
                )

    def start(self, tick: float, error_range: float = 0) -> None:
        """Method to start a thread to poll and calulate the data of all present actors in the connected Carla world

        Args:
            tick (float): Time in seconds how often the position of the actors is to be polled
            error_range (float, optional): Range from which a random error is generated that falsifies the positions
        """
        if self._hero == None:
            logging.error("No Hero initialized or found")
            sys.exit(1)
        self._thread = Thread(target=self._poll_data, args=[tick, error_range])
        self._thread.daemon = True
        self._thread.start()

    def stop(self) -> None:
        """Method to stop the polling of positions and calculation of data by killing the thread and main loop"""
        self._stop = True
        if self._thread != None:
            self._thread.join()

    def save_csv(self, path: str, filename: str) -> None:
        """Method to save collected data into a .csv file on the given path with the given filename

        Args:
            path (string): Path where the file should be saved to
            filename (string): Name of the file the data should be saved to
        """
        with open(pathlib.Path(path, filename), "a", encoding="UTF-8") as f:
            writer = csv.writer(f)
            if not self._header_written:
                writer.writerow(self._header())
                self._header_written = True
            for actor_id in self._actors:
                writer.writerow(self._actors[actor_id].get_data())

    def subscribe(self, subscription: Subscription) -> None:
        """Method to add callback function to which the calculated data will be forwarded to in runtime

        Args:
            subscription (Subscription): Callback function with one argument holding the data in JSON format
        """
        self._subscribers.append(subscription)

    def unsubscribe(self, subscription: Subscription) -> None:
        """Method to remove callback function to which the calculated data is forwarded to in runtime

        Args:
            subscription (Subscription): Callback function that should be removed
        """
        for index in range(len(self._subscribers)):
            if self._subscribers[index] == subscription:
                self._subscribers.pop(index)
                break

    def _header(self) -> List[str]:
        """Creates a header line for the created CSV file

        Returns:
            List[str]: An array holding all headers for the created CSV file
        """
        header: List[str] = ["ID", "type"]
        header += self._data_header("velocity")
        header += self._data_header("orientation")
        header += self._data_header("angular_speed")
        header += self._data_header("accelaration")
        header += self._data_header("distance_to_hero")
        header += self._data_header("angle_to_hero")
        return header

    def _data_header(self, data_type: str) -> List[str]:
        """Creates multiple headers for each column

        Args:
            data_type (str): Name of the column

        Returns:
            List[str]: Array with index appended to the name
        """
        header: List[str] = []
        for count in range(self._max_entry_count):
            header.append(f"{data_type}_{count}")
        return header

    def _poll_data(self, tick: float, error_range: float) -> None:
        """Method to run a loop to poll position of each found traffic user in the connected Carla world and calculate their data in a specified time interval

        Args:
            tick (float): Time in seconds how much time should pass until the next poll starts
            error_range (float): Range from which a random error is generated that falsifies the positions
        """
        while not self._stop:
            current_time: float = round(time.time(), 3)
            time_now: datetime = datetime.now()
            for actor in self._road_users:
                location: carla.Location = actor.get_transform().location
                timestamp: float = time_now.second + round(
                    time_now.microsecond / 1000000, 3
                )
                self._hero.on_position_data(
                    actor.id,
                    timestamp,
                    mo.distorted_coordinate(location, abs(float(error_range))),
                )
            rest_time: float = round(time.time(), 3) - current_time
            rest_sleep: float = tick - rest_time
            if rest_sleep > 0:
                time.sleep(tick)

    def _classify_type(self, actor_type: str) -> int:
        """Method to classify the type of an actor encoded as an integer

        Args:
            actor_type (str): Actor type provided by the Carla world

        Returns:
            int: Encoded traffic user type
        """
        for category in VehicleTypes.categories:
            for type in VehicleTypes.types[category]:
                if type in actor_type:
                    return Constants.ROAD_USER_CODE[category]
        return Constants.ROAD_USER_CODE[EActorType.PEDESTRIAN]
