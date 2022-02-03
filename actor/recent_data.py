from common import Recent, CalculatedData, MAX_STORE_SIZE
import operations as op

# from scipy import interpolate


class RecentData:
    def __init__(self, expiration_time=3):
        self._expiration_time = expiration_time
        self._timestamp = Recent(None, None)
        self._position = Recent(None, None)
        self._orientation = 0
        self._stored = {}

    def update(self, timestamp, position):
        self._store(timestamp, position)
        if (
            self._timestamp.current != None
            and (timestamp - self._timestamp.current) >= self._expiration_time
        ):
            self._timestamp.current = None

        self._timestamp.previous = self._timestamp.current
        self._timestamp.current = timestamp

        if self._timestamp.previous != None:
            self._position.previous = self._position.current
            self._position.current = position

            if self._position.current == None or self._position.previous == None:
                return None
            vector = op.get_vector(self._position.current, self._position.previous)
            return CalculatedData(
                position,
                self._get_orientation(vector),
                self._get_velocity(vector),
                None,
                None,
            )

    def _get_velocity(self, vector):
        time_difference = abs(self._timestamp.previous - self._timestamp.current)
        return op.get_velocity(vector, time_difference)

    def _get_orientation(self, vector):
        orientation = op.get_angle_to_y_axis(vector)
        if orientation != None:
            self._orientation = orientation
        return orientation if orientation != None else self._orientation

    def _store(self, timestamp, position):
        if len(self._stored) >= MAX_STORE_SIZE:
            first = list(self._stored.keys())[0]
            del self._stored[first]
        self._stored[timestamp] = position

    # Need to make sure we know in which direction the hero is headed to
    # close_hero_timestamp = self._database.get_close_data_by_timestamp(self._id, timestamp, self._tolerance)
    # close_hero_position =  self._database.get_data_by_timestamp(self._id, close_hero_timestamp).position
    # hero_distance_vector = Operations.get_vector(hero_position, close_hero_position)
    # angle_to_hero = Operations.get_angle_between_vectors(hero_distance_vector, distance_vector)
    # return Data(position, ...)

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
