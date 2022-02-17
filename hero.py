from recent_data import RecentData
from scipy import interpolate
from common import Coordinate
import math_operations as mo
import logging


class Hero:
    def __init__(self, hero_id, actors):
        self._hero_id = hero_id
        self._actors = actors
        self._recent_data = {}
        self._relevance_radius = 100

    def on_position_data(self, id, timestamp, position):
        if id not in self._recent_data:
            self._recent_data[id] = RecentData(3)
        velocity, orientation, angular_speed = self._recent_data[id].update(
            timestamp, position
        )
        if id != self._hero_id:
            distance_to_hero, angle_to_hero = self._hero_dependent_data(id, timestamp)
        else:
            distance_to_hero, angle_to_hero = None, None
        try:
            self._actors[id].add_data(
                velocity, orientation, angular_speed, distance_to_hero, angle_to_hero
            )
        except KeyError:
            logging.warn(f"Failed to add data for actor {id}")

    def _hero_dependent_data(self, id, timestamp):
        position_other = self._predict_position(id, timestamp)
        position_hero_now, position_hero_before = self._predict_positions(
            self._hero_id, timestamp - 0.5, timestamp
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
        if not (id in self._recent_data):
            return None
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
        vec = mo.vector(position_hero, position_other)
        return mo.vector_length(vec)

    def _get_angle_to_hero(
        self,
        position_hero_before,
        position_hero_now,
        position_other,
    ):
        vector_hero = mo.vector(position_hero_now, position_hero_before)
        vector_hero_other = mo.vector(position_other, position_hero_before)
        return mo.angle_between_vectors(vector_hero, vector_hero_other)
