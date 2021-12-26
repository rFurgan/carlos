from datatypes.geoposition import Geoposition
from gnss_sensor import GnssSensor
from data_calculator import DataCalculator
from datatypes.data import Data


class RoadUser:

    def __init__(self, id, actor, world, hero=None):
        self._id = id
        self._type = actor.type_id
        self._gnss_sensor = GnssSensor(actor, world, self._on_sensor_data)
        self._hero = hero
        self._data = {}
    
    def __del__(self):
        del self._gnss_sensor

    @property
    def data(self):
        return self._data

    def _on_sensor_data(self, timestamp, position):
        timestamp_before = self._closest_timestamp(True, timestamp, self._data)
        direction_vector = DataCalculator.get_vector(position, self._data[timestamp_before].position)
        if self._hero != None:
            hero_timestamp_before = self._closest_timestamp(True, timestamp, self._hero.data)
            hero_position_before = self._hero.data[hero_timestamp_before].position
            hero_timestamp_after = self._closest_timestamp(False, timestamp, self._hero.data)
            hero_position_after = self._hero.data[hero_timestamp_after].position
            hero_position = self._hero_position_at(timestamp, hero_timestamp_before, hero_position_before, hero_timestamp_after, hero_position_after)
            hero_vector = DataCalculator.get_vector(hero_position, hero_position_before)
        self._data[timestamp] = Data(
            id = self._id,
            type = self._type,
            position = position,
            orientation = DataCalculator.get_angle_to_y_axis(direction_vector),
            velocity = DataCalculator.get_velocity(direction_vector, timestamp_before, timestamp),
            distance_to_hero = 0 if self._hero == None else DataCalculator.getVectorLength(DataCalculator.get_vector(hero_position, position)),
            angle_to_hero = 0 if self._hero == None else DataCalculator.getAngleBetweenVectors(hero_vector, direction_vector)
        )

    def _closest_timestamp(self, before, timestamp, dataset):
        closest_timestamp = timestamp
        timestamps = list(dataset)
        best_diff = timestamp - timestamps[0]
        for ts in timestamps:
            diff = timestamp - ts
            if (diff < best_diff and (diff >= 0 if before else diff <= 0)):
                best_diff = diff
                closest_timestamp = timestamp
        return closest_timestamp

    def _hero_position_at(self, timestamp, hero_timestamp_before, hero_position_before, hero_timestamp_after, hero_position_after):
        return Geoposition(
            longitude=hero_position_before.longitude + (timestamp - hero_timestamp_before) * ((hero_position_after.longitude - hero_position_before.longitude) / (hero_timestamp_after - hero_timestamp_before)),
            latitude=hero_position_before.latitude + (timestamp - hero_timestamp_before) * ((hero_position_after.latitude - hero_position_before.latitude) / (hero_timestamp_after - hero_timestamp_before)),
            altitude=hero_position_before.altitude + (timestamp - hero_timestamp_before) * ((hero_position_after.altitude - hero_position_before.altitude) / (hero_timestamp_after - hero_timestamp_before)),
        )