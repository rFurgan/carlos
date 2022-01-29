from database.recent_data import RecentData
from common.datatypes import Data, ETimestampType, Geoposition
from common.operations import Operations
from scipy import interpolate

# TODO Hero
# TODO -> When new data from other actors comes in, we need to check if data exists for that timestamp and inter-/extrapolate if necessary

class Hero:
    def __init__(self, id):
        self._id = id
        self._recent_data = {}

    def on_position_data(self, id, timestamp, position):
        timestamp = int(timestamp)
        position = self._position_in_meter(position)

        if self._recent_data[id] == None:
            self._recent_data[id] = RecentData()
        # TODO What to do with this data?
        # TODO Check if it's "None"
        self._recent_data[id].update(timestamp, position)

        # TODO Only check for more data if they're relevant (not hero) - checking distance afterwards, so we need to check that inside and stop


    def _position_in_meter(self, position):
        factor = 100000
        return Geoposition(
            position.longitude * factor,
            position.latitude * factor,
            position.altitude * factor,
        )

    #     # Need to make sure we know in which direction the hero is headed to
    #     # close_hero_timestamp = self._database.get_close_data_by_timestamp(self._id, timestamp, self._tolerance)
    #     # close_hero_position =  self._database.get_data_by_timestamp(self._id, close_hero_timestamp).position
    #     # hero_distance_vector = Operations.get_vector(hero_position, close_hero_position)
    #     # angle_to_hero = Operations.get_angle_between_vectors(hero_distance_vector, distance_vector)
    #     # return Data(position, ...)

    # def _hero_position_at(self, timestamp):
    #     longitudes = []
    #     latitudes = []
    #     altitudes = []
    #     data = self._database.get_data_by_id(self._id)
    #     if data == None:
    #         return
    #     timestamps = list(data.keys())
    #     timestamps.sort()
    #     if len(timestamps) == 0:
    #         return None
    #     for ts in timestamps:
    #         position = data[ts].position
    #         longitudes.append(position.longitude)
    #         latitudes.append(position.latitude)
    #         altitudes.append(position.altitude)
    #     polation = (
    #         "extrapolate"
    #         if timestamp < timestamps[0] or timestamp > timestamps[-1]
    #         else "interpolate"
    #     )
    #     polate_longitude = interpolate.interp1d(
    #         timestamps, longitudes, fill_value=polation
    #     )
    #     polate_latitude = interpolate.interp1d(
    #         timestamps, latitudes, fill_value=polation
    #     )
    #     polate_altitude = interpolate.interp1d(
    #         timestamps, altitudes, fill_value=polation
    #     )
    #     return Geoposition(
    #         polate_longitude(timestamp),
    #         polate_latitude(timestamp),
    #         polate_altitude(timestamp),
    #     )
