from math import degrees, sqrt
from numpy import arccos

# TODO Check if docstring needs the properties in the class description


class RoadUserData:
    """
    A class to calculate and hold the generated data for a RoadUser
    """

    def __init__(self, data_reference, timestamp, position, is_hero):
        """
        Args:
            `data_reference  (dict[float, RoadUserData):`   Reference to dictionary of data to fetch previous data
            `timestamp       (float):`                      Timestamp of the provided positional data
            `position        (Vector3D):`                   Position data at the specified timestamp
            `is_hero         (bool):`                       Flag to define if data is of the hero

        Returns:
            `None`
        """
        self._timestamp = timestamp
        self._position = position
        self._is_hero = is_hero
        self._prev_data = self._get_prev_data(data_reference)
        self._orientation = self._calc_orientation()
        self._velocity = self._calc_velocity()
        self._distance = 0.0 if is_hero else None

    @property
    def get_timestamp(self):
        """`float:` Timestamp of the provided positional data of the RoadUser"""
        return self._timestamp

    @property
    def get_position(self):
        """`Vector3D:` Position at the specified timestamp of the RoadUser"""
        return self._position

    @property
    def get_distance(self):
        """`float or None:` Distance from the RoadUser to the hero in Meters"""
        return self._distance

    @property
    def get_orientation(self):
        """`int:` Orientation describing the angle between the y-axis and the RoadUser in degrees"""
        return self._orientation

    @property
    def get_velocity(self):
        """`int:` Speed of the RoadUser in km/h"""
        return self._velocity

    def get_data(self):
        """`dict[float, dict[str, int or float]]:` Returns the data as a dictionary with the timestamp as key"""
        return {
            self._timestamp: {
                "orientation": self._orientation,
                "distance": self._distance,
                "velocity": self._velocity,
            }
        }

    def recalculate_distance(self, hero_position, accuracy=4):
        """
        Calculates the distance to the hero afterwards when the data didn't suffice at the initialization

        Args:
            `hero_position (Vector3D):` Position of the hero in the most recent incoming data
            `accuracy (int, optional):`       Describes how many digits after the dot to be preserved. Defaults to 4

        Returns:
            `None`
        """
        x = hero_position.x - self._position.x
        y = hero_position.y - self._position.y
        z = hero_position.z - self._position.z
        self._distance = round(sqrt((x * x) + (y * y) + (z * z)), accuracy)

    def _get_prev_data(self, data_reference):
        """
        RoadUserData containing the data around one second before

        Args:
            `data_reference (dict[float, RoadUserData):` Data of the previous position with one second difference

        Returns:
            `None` or `RoadUserData`
        """
        for timestamp in data_reference:
            if self._timestamp - timestamp <= 1:
                return data_reference[timestamp]
        return None

    def _calc_orientation(self):
        """
        Calculates and gives the angle between the y-axis and the RoadUser in degrees

        Returns:
            `int`
        """
        return int(
            degrees(
                arccos(
                    self._position.y
                    / sqrt(self._position.x ** 2 + self._position.y ** 2)
                )
            )
        )

    def _calc_velocity(self):
        """
        Calculates and gives the velocity at the given timestamp

        Returns:
            `int` or `None`
        """
        if self._prev_data == None:
            return None
        return int(
            (
                self._calc_distance(self._prev_data.get_position)
                / (self._timestamp - self._prev_data.get_timestamp)
            )
            * 3.6
        )

    def _calc_distance(
        self,
        prev_position,
        accuracy=4,
    ):
        """
        Calculates and gives the distance between the current position and the given other position

        Args:
            `prev_position (Vector3D):`   Reference point to calculate the distance between the current position
            `accuracy (int, optional):`         Describes how many digits after the dot to be preserved. Defaults to 4

        Returns:
            `float`
        """
        x = self._position.x - prev_position.x
        y = self._position.y - prev_position.y
        z = self._position.z - prev_position.z
        return round(sqrt((x * x) + (y * y) + (z * z)), accuracy)
