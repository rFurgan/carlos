from carla import Vector3D
from typing import Union, Dict
from random import randint
from numpy import arccos
from math import degrees, sqrt
from common.position_time import PositionTime

# TODO Add distance to HERO


class RoadUser:
    """
    A class to keep track of actors in the connected CARLA world

    A class to keep track of actors by saving the timestamps along with the position (modified with a specific deviation) from which the orientation, velocity and distance to "us"/the "hero" is calculated

    Methods
    -------
    get_id()
        Returns the id of actor for which the instance is created for
    get_data()
        Returns all the data collected over the runtime of the program
    get_recent_data()
        Returns the most recent data collected
    update(position, timestamp)
        Updates the positional and timestamp data and then creates a new entry in the database with the newly calculated data
    _add_deviation(postion, deviation=0)
        Adds a random amount of deviation to the coordinates of the position
    _calculate_velocity()
        Calculates and returns the velocity from the most recent data
    _calculate_travelled_distance()
        Calculates and returns the travelled distance from the most recent data
    _calculate_distance()
        Calculates and returns the distance from the actor to "us"/the "hero" from the most recent data
    _calculate_orientation()
        Calculates and returns the orientation from the y-axis defined in the world in degree from the most recent data
    """

    def __init__(self, id: int) -> None:
        """
        Parameters
        ----------
        id : int
            Id of the actor for which the instance is created for

        Returns
        -------
        None
        """
        self._id: int = id
        self._data: Dict[float, Dict[str, Union[float, None]]] = {}
        self._current: PositionTime = PositionTime()
        self._previous: PositionTime = PositionTime()

    def get_id(self) -> int:
        """
        Returns the id of actor for which the instance is created for

        Parameters
        ----------

        Returns
        -------
        int
            The id of the actor for which the instance is created for
        """
        return self._id

    def get_data(self) -> Dict[float, Dict[str, Union[float, None]]]:
        """
        Returns all the data collected over the runtime of the program

        Parameters
        ----------

        Returns
        -------
        Dict[float, Dict[str, Union[float, None]]]
            Data in a dictionary with the key being the timestamp and the corresponding data is dictionary with velocity, distance and orientation as values
        """
        return self._data

    def get_recent_data(self) -> Dict[int, Dict[str, Union[float, None]]]:
        """
        Returns the most recent data collected

        Parameters
        ----------

        Returns
        -------
        Dict[int, Dict[str, Union[float, None]]]
            The most recent data collected over the runtime of the program as a dictionary
        """
        timestamp = list(self._data)[-1]
        return {timestamp: self._data[timestamp]}

    def update(self, position: Vector3D, timestamp: float) -> None:
        """
        Updates the positional and timestamp data and then creates a new entry in the database with the newly calculated data

        Parameters
        ----------
        position : Vector3D
            The new 3d coordinates of the actor at the given timestamp of the newest update period
        timestamp : float
            The new timestamp of the newest update period

        Returns
        -------
        None
        """
        self._previous.update(self._current._position, self._current._timestamp)
        self._current.update(self._add_deviation(position), timestamp)
        self._data[timestamp] = {
            "orientation": self._calculate_orientation(),
            "velocity": self._calculate_velocity(),
            "distance": self._calculate_distance(),
        }

    def _add_deviation(self, position: Vector3D, deviation: int = 0) -> Vector3D:
        """
        Adds a random amount of deviation to the coordinates of the position

        Parameters
        ----------
        position : Vector3D
            The 3d coordinates to be falsified with a specific deviation
        deviation : int, optional
            The range from which a random number will be generated to falsify the position

        Returns
        -------
        Vector3D
            New position with deviation added to the coordinates
        """
        position.x = position.x + randint(-deviation, deviation)
        position.y = position.y + randint(-deviation, deviation)
        position.z = position.z + randint(-deviation, deviation)
        return position

    def _calculate_velocity(self) -> Union[float, None]:
        """
        Calculates and returns the velocity from the most recent data

        Parameters
        ----------

        Returns
        -------
        float
            Velocity of the actor with the newly arrived data
        None
            Insufficient data
        """
        if self._current.has_none() or self._previous.has_none():
            return None
        current_timestamp = self._current.get_timestamp()
        previous_timestamp = self._previous.get_timestamp()
        return (
            self._calculate_travelled_distance()
            / (current_timestamp - previous_timestamp)
        ) * 3.6

    def _calculate_travelled_distance(self) -> Union[float, None]:
        """
        Calculates and returns the travelled distance from the most recent data

        Parameters
        ----------

        Returns
        -------
        float
            Travelled distance of the actor with the newly arrived data
        None
            Insufficient data
        """
        if self._current.has_none() or self._previous.has_none():
            return None
        current_position = self._current.get_position()
        previous_position = self._previous.get_position()
        x = current_position.x - previous_position.x
        y = current_position.y - previous_position.y
        z = current_position.z - previous_position.z
        return sqrt((x * x) + (y * y) + (z * z))

    # TODO Distance to HERO
    def _calculate_distance(self) -> Union[float, None]:
        """
        Calculates and returns the distance from the actor to "us"/the "hero" from the most recent data

        Parameters
        ----------

        Returns
        -------
        float
            Distance of the actor from "us"/the "hero" with the newly arrived data
        None
            Insufficient data
        """
        if self._current.has_none():
            return None
        # current_position = self._current.get_position()
        # x = <hero_position>.x - current_position.x
        # y = <hero_position>.y - current_position.y
        # z = <hero_position>.z - current_position.z
        # return sqrt((x * x) + (y * y) + (z * z))

    def _calculate_orientation(self) -> Union[float, None]:
        """
        Calculates and returns the orientation from the y-axis defined in the world in degree from the most recent data

        Parameters
        ----------

        Returns
        -------
        float
            Orientation from the y-axis defined in the world in degree with the newly arrived data
        None
            Insufficient data
        """
        if self._current.has_none():
            return None
        current_position = self._current.get_position()
        return degrees(
            arccos(
                current_position.y
                / sqrt(current_position.x ** 2 + current_position.y ** 2)
            )
        )
