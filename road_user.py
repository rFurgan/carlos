from datatypes import Geoposition, Data, HeroData
from gnss_sensor import GnssSensor
from data_calculator import DataCalculator
from scipy import interpolate


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
        direction_vector = None
        timestamp_before = self._closest_timestamp(timestamp, self._data)
        if timestamp_before != None:
            direction_vector = DataCalculator.get_vector(
                position, self._data[timestamp_before].position
            )
        hero_data = self._hero_data(timestamp, position, direction_vector)
        self._data[timestamp] = Data(
            self._id,
            self._type,
            position,
            DataCalculator.get_angle_to_y_axis(direction_vector)
            if timestamp_before != None
            else None,
            DataCalculator.get_velocity(direction_vector, timestamp_before, timestamp)
            if timestamp_before != None
            else None,
            0 if self._hero == None else hero_data.distance_to_hero,
            0 if self._hero == None else hero_data.angle_to_hero,
        )

    def _hero_data(self, timestamp, position, direction_vector):
        if self._hero != None:
            hero_timestamp_before = self._closest_timestamp(timestamp, self._hero.data)
            if hero_timestamp_before != None:
                hero_position_before = self._hero.data[hero_timestamp_before].position
                hero_position_at = self._hero_position_at(timestamp)
                if (hero_position_at != None):
                    hero_vector = DataCalculator.get_vector(
                        hero_position_at, hero_position_before
                    )
                    return HeroData(
                        DataCalculator.get_vector_length(
                            DataCalculator.get_vector(hero_position_at, position)
                        ),
                        None
                        if direction_vector == None
                        else DataCalculator.getAngleBetweenVectors(
                            hero_vector, direction_vector
                        ),
                    )
        return HeroData(distance_to_hero=None, angle_to_hero=None)

    def _closest_timestamp(self, timestamp, dataset):
        closest_timestamp = None
        timestamps = list(dataset)
        if len(timestamps) > 0:
            best_diff = timestamp - timestamps[0]
            for ts in timestamps:
                diff = timestamp - ts
                if diff < best_diff and (diff > 0):
                    best_diff = diff
                    closest_timestamp = ts
        return closest_timestamp

    def _hero_position_at(self, timestamp):
        longitudes = []
        latitudes = []
        altitudes = []
        timestamps = sorted(list(self._hero.data))
        if (len(timestamps) == 0):
            return None
        for ts in timestamps:
            position = self._hero.data[ts].position
            longitudes.append(position.longitude)
            latitudes.append(position.latitude)
            altitudes.append(position.altitude)
        polation = "extrapolate" if timestamp < timestamps[0] or timestamp > timestamps[-1] else "interpolate"
        polate_longitude = interpolate.interp1d(
            timestamps, longitudes, fill_value=polation
        )
        polate_latitude = interpolate.interp1d(
            timestamps, latitudes, fill_value=polation
        )
        polate_altitude = interpolate.interp1d(
            timestamps, altitudes, fill_value=polation
        )
        return Geoposition(
            polate_longitude(timestamp),
            polate_latitude(timestamp),
            polate_altitude(timestamp),
        )
