import logging
import sys
import time
import csv
import math_operations as mo
import pathlib
from hero import Hero
from actor import Actor
from carla import Client
from common import EActorType, Coordinate, VehicleTypes, ROAD_USER_CODE
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
    """
    def __init__(self, host, port, relevance_radius, max_entry_count):
        self._actors = {}
        self._road_users = []
        self._subscribers = []
        self._stop = False
        self._thread = None
        self._hero = None
        self._relevance_radius = relevance_radius
        self._max_entry_count = max_entry_count
        self._header_written = False
        try:
            client = Client(host, port)
            client.set_timeout(2.0)
            world = client.get_world()
        except RuntimeError as error:
            logging.error(f"Something went wrong connecting: {error.message}")
            sys.exit(1)
        for actor in world.get_actors():
            if (
                EActorType.VEHICLE.value in actor.type_id
                or EActorType.PEDESTRIAN.value in actor.type_id
            ):
                if self._hero == None and mo.vector_length(actor.get_velocity()) > 0:
                    self._hero = Hero(actor.id, self._actors, self._subscribers, self._relevance_radius)
                self._road_users.append(actor)
                self._actors[actor.id] = Actor(
                    actor.id, self._classify_type(actor.type_id), self._max_entry_count
                )

    def start(self, tick):
        """Method to start a thread to poll and calulate the data of all present actors in the connected Carla world

        Args:
            tick (float): Time in seconds how often the position of the actors is to be polled
        """
        if self._hero == None:
            logging.error("No Hero initialized or found")
            sys.exit(1)
        self._thread = Thread(target=self._poll_data, args=[tick])
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        """Method to stop the polling of positions and calculation of data by killing the thread and main loop"""
        self._stop = True
        if self._thread != None:
            self._thread.join()

    def save_csv(self, path, filename):
        """Method to save collected data into a .csv file on the given path with the given filename

        Note:
            If the path doesn't work, try adding r before the string. E.g. r"C:\users\someUser\Desktop"
            The filename should include .csv at the end

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

    def subscribe(self, callback):
        """Method to add callback function to which the calculated data will be forwarded to in runtime

        Args:
            callback (function): Callback function with one argument holding the data in JSON format
        """
        self._subscribers.append(callback)

    def unsubscribe(self, callback):
        """Method to remove callback function to which the calculated data is forwarded to in runtime

        Args:
            callback (function): Callback function that should be removed
        """
        for index in range(len(self._subscribers)):
            if self._subscribers[index] == callback:
                self._subscribers.pop(index)
                break

    def _header(self):
        """Creates a header line for the created CSV file

        Returns:
            Array[str]: An array holding all headers for the created CSV file
        """
        header = ["ID", "type"]
        header += self._data_header("velocity")
        header += self._data_header("orientation")
        header += self._data_header("angular_speed")
        header += self._data_header("distance_to_hero")
        header += self._data_header("angle_to_hero")
        return header

    def _data_header(self, data_type):
        """Creates multiple headers for each column 

        Args:
            data_type (str): Name of the column

        Returns:
            Array[str]: Array with index appended to the name 
        """
        header = []
        for count in range(self._max_entry_count):
            header.append(f"{data_type}_{count}")
        return header

    def _poll_data(self, tick):
        """Method to run a loop to poll position of each found traffic user in the connected Carla world and calculate their data in a specified time interval

        Args:
            tick (float): Time in seconds how much time should pass until the next poll starts
        """
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
        """Method to classify the type of an actor encoded as an integer

        Args:
            actor_type (str): Actor type provided by the Carla world

        Returns:
            int: Encoded traffic user type
        """
        for category in list(VehicleTypes.types.keys()):
            for type in VehicleTypes.types[category]:
                if type in actor_type:
                    return ROAD_USER_CODE[category]
        return ROAD_USER_CODE[EActorType.PEDESTRIAN]
