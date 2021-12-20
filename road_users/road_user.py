from sensors.gnss_sensor import GnssSensor
from common.road_user_data import RoadUserData


class RoadUser:
    """
    A class to store data of an actor
    """

    def __init__(self, actor, world):
        """
        Args:
            `actor (Actor):`  Reference to the actor which the class represents
            `world (World):`  Reference to the world the actor is spawned in

        Returns:
            `None`
        """
        self._data = {}
        self._sensor = GnssSensor(actor, world, self.on_data)

    def get_data(self):
        """
        Creates a new dictionary with the RoadUserData over the whole runtime

        Returns:
            `dict[float, RoadUserData]`
        """
        dataset = {}
        for timestamp in self._data:
            dataset.update(self._data[timestamp].get_data())
        return dataset

    def get_latest_data(self):
        """
        Creates a new dictionary with the latest RoadUserData

        Returns:
            `dict[float, RoadUserData]`
        """
        timestamps = self._data.keys()
        if len(timestamps) == 0:
            return {}
        timestamps.sort()
        return self._data[timestamps[-1]].get_data()

    def on_data(self, timestamp, position):
        """
        Method to be called when new data from the GNSS sensor arrives. Stores the new data in a dictionary with the timestamp as key

        Args:
            `timestamp  (float):`       Timestamp on when the position data was generated
            `position   (Vector3D):`    Position data on the given timestamp generated from the sensor

        Returns:
            `None`
        """
        self._data[timestamp] = RoadUserData(self._data, timestamp, position, False)

    def get_close_data(self, timestamp):
        """
        Finds the RoadUserData closest to the given timestamp that didn't calculate the distance to the hero yet

        Args:
            `timestamp (float):` Timestamp of data the hero generated to help calculating the distance

        Returns:
            `RoadUserData` or `None`
        """
        for data_timestamp in self._data:
            if (
                abs(data_timestamp - timestamp <= 1)
                and self._data[data_timestamp].get_distance == None
            ):
                return self._data[data_timestamp]
        return None

    def on_hero_data(self, timestamp, position):
        """
        Method to be called when new data from the GNSS sensor of the hero arrives. Tries to recalculate the distance if possible

        Args:
            `timestamp  (float):`       Timestamp on when the position data of the hero was generated
            `position   (Vector3D):`    Position data on the given timestamp generated from the sensor

        Returns:
            `None`
        """
        sensor = self.get_close_data(timestamp)
        if sensor != None:
            sensor.recalculate_distance(position)
