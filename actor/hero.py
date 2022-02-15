from .recent_data import RecentData
from scipy import interpolate
from common import Coordinate, Operations
import json


class Hero:
    def __init__(self, id, relevance_radius, subscribers, cursor, database):
        self._id = id
        self._relevance_radius = relevance_radius
        self._subscribers = subscribers
        self._cursor = cursor
        self._database = database
        self._recent_data = {}
        self._stop = False
        self._type = None

    def on_position_data(self, id, type, timestamp, position):
        if id not in self._recent_data:
            self._recent_data[id] = RecentData()
        orientation, velocity = self._recent_data[id].update(timestamp, position)
        distance_to_hero, angle_to_hero = None, None
        if id != self._id:
            distance_to_hero, angle_to_hero = self._hero_dependent_data(id, timestamp)
        if distance_to_hero != None and distance_to_hero >= self._relevance_radius:
            return
        # self._cursor.execute(
        #     f"INSERT INTO actor_{id} VALUES({timestamp}, {orientation if orientation != None else 'NULL'}, {velocity if velocity != None else 'NULL'}, {distance_to_hero if distance_to_hero != None else 'NULL'}, {angle_to_hero if angle_to_hero != None else 'NULL'})"
        # )
        # self._database.commit()
        for subscriber in self._subscribers:
            subscriber(
                json.dumps(
                    {
                        "id": id,
                        "type": type,
                        "timestamp": timestamp,
                        "data": {
                            "orientation": orientation,
                            "velocity": velocity,
                            "distance_to_hero": distance_to_hero,
                            "angle_to_hero": angle_to_hero,
                        },
                    }
                )
            )

    def _hero_dependent_data(self, id, timestamp):
        position_other = self._predict_position(id, timestamp)
        position_hero_now, position_hero_before = self._predict_positions(
            self._id, timestamp - 0.5, timestamp
        )
        if (
            position_hero_before == None and position_hero_now == None
        ) or position_other == None:
            return None, None
        if position_hero_before == None and position_hero_now != None:
            return self._get_distance_to_hero(position_hero_now, position_other), None
        return (
            self._get_distance_to_hero(position_hero_now, position_other),
            self._get_angle_to_hero(
                position_hero_before, position_hero_now, position_other
            ),
        )

    def _predict_position(self, id, timestamp):
        stored_data = self._recent_data[id].stored
        timestamps = sorted(stored_data, reverse=True)
        if len(timestamps) <= 1:
            return None
        x = []
        y = []
        z = []
        for ts in timestamps:
            data = stored_data[ts]
            x.append(data.x)
            y.append(data.y)
            z.append(data.z)
        polation = (
            "extrapolate"
            if timestamp < timestamps[0] or timestamp > timestamps[-1]
            else "interpolate"
        )
        polate_x = interpolate.interp1d(timestamps, x, fill_value=polation)
        polate_y = interpolate.interp1d(timestamps, y, fill_value=polation)
        polate_z = interpolate.interp1d(timestamps, z, fill_value=polation)

        return Coordinate(polate_x(timestamp), polate_y(timestamp), polate_z(timestamp))

    def _predict_positions(self, id, timestamp_before, timestamp_now):
        stored_data = self._recent_data[id].stored
        timestamps = sorted(stored_data, reverse=True)
        if len(timestamps) <= 1:
            return None, None
        x = []
        y = []
        z = []
        for ts in timestamps:
            data = stored_data[ts]
            x.append(data.x)
            y.append(data.y)
            z.append(data.z)

        polation_before = (
            "extrapolate"
            if timestamp_before < timestamps[0] or timestamp_before > timestamps[-1]
            else "interpolate"
        )
        polate_x_before = interpolate.interp1d(
            timestamps, x, fill_value=polation_before
        )
        polate_y_before = interpolate.interp1d(
            timestamps, y, fill_value=polation_before
        )
        polate_z_before = interpolate.interp1d(
            timestamps, z, fill_value=polation_before
        )

        polation_now = (
            "extrapolate"
            if timestamp_now < timestamps[0] or timestamp_now > timestamps[-1]
            else "interpolate"
        )
        polate_x_now = interpolate.interp1d(timestamps, x, fill_value=polation_now)
        polate_y_now = interpolate.interp1d(timestamps, y, fill_value=polation_now)
        polate_z_now = interpolate.interp1d(timestamps, z, fill_value=polation_now)

        position_x_now = polate_x_now(timestamp_now)
        position_y_now = polate_y_now(timestamp_now)
        position_z_now = polate_z_now(timestamp_now)

        position_x_before = polate_x_before(timestamp_before)
        position_y_before = polate_y_before(timestamp_before)
        position_z_before = polate_z_before(timestamp_before)

        if position_x_now == position_x_before and position_y_now == position_y_before:
            return (
                Coordinate(
                    position_x_now,
                    position_y_now,
                    position_z_now,
                ),
                None,
            )

        return (
            Coordinate(
                position_x_now,
                position_y_now,
                position_z_now,
            ),
            Coordinate(
                position_x_before,
                position_y_before,
                position_z_before,
            ),
        )

    def _get_distance_to_hero(self, position_hero, position_other):
        vector = vector(position_hero, position_other)
        return Operations.vector_length(vector)

    def _get_angle_to_hero(
        self,
        position_hero_before,
        position_hero_now,
        position_other,
    ):
        vector_hero = Operations.vector(position_hero_now, position_hero_before)
        vector_hero_other = Operations.vector(position_other, position_hero_before)
        return Operations.angle_between_vectors(vector_hero, vector_hero_other)
