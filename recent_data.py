from common.datatypes import Recent, CalculatedData
from common.operations import Operations

# from scipy import interpolate


class RecentData:
    def __init__(self, expiration_time=3):
        self._expiration_time = expiration_time
        self._timestamp = Recent()
        self._position = Recent()

    def update(self, timestamp, position):
        if self._timestamp.current != None:
            # Check for data expiration
            if (timestamp - self._timestamp.current) >= self._expiration_time:
                self._timestamp.current = None

        self._timestamp.previous = self._timestamp.current
        self._timestamp.current = timestamp

        if self._timestamp.previous != None:
            self._position.previous = self._position.current
            self._position.current = position

            if self._position.current == None or self._position.previous == None:
                return
            vector = Operations.get_vector(
                self._position.current, self._position.previous
            )
            orientation = Operations.get_angle_to_y_axis(vector)
            velocity = Operations.get_velocity(
                vector, self._timestamp.previous, self._timestamp.current
            )
            return CalculatedData(position, orientation, velocity, None, None)

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
