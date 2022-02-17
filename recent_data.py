from common import Recent, MAX_STORE_SIZE
import math_operations as mo


class RecentData:
    def __init__(self, expiration_time):
        self._expiration_time = expiration_time
        self._recent_timestamp = Recent(None, None)
        self._recent_position = Recent(None, None)
        self._recent_orientation = Recent(None, None)
        self._orientation = None
        self._velocity = 0
        self._stored = {}

    @property
    def stored(self):
        return self._stored

    def update(self, timestamp, position):
        self._store(timestamp, position)
        if (
            self._recent_timestamp.current != None
            and (timestamp - self._recent_timestamp.current) > self._expiration_time
        ):
            self._recent_timestamp.current = None

        self._recent_timestamp.previous = self._recent_timestamp.current
        self._recent_timestamp.current = timestamp

        if self._recent_timestamp.previous != None:
            self._recent_position.previous = self._recent_position.current
            self._recent_position.current = position

            if self._recent_position.has_none():
                return None, None, None
            vec = mo.vector(
                self._recent_position.current, self._recent_position.previous
            )
            return (
                self._get_velocity(vec),
                self._get_orientation(vec),
                self._get_angular_velocity(),
            )
        return None, None, None

    def _get_velocity(self, vec):
        self._velocity = mo.velocity(
            vec, self._recent_timestamp.previous, self._recent_timestamp.current
        )
        return self._velocity

    def _get_orientation(self, vec):
        orientation = mo.angle_to_y_axis(vec)
        self._recent_orientation.previous = self._recent_orientation.current
        self._recent_orientation.current = orientation
        if orientation != None and self._velocity > 0:
            self._orientation = orientation
        return (
            orientation
            if orientation != None and self._velocity > 0
            else self._orientation
        )

    def _get_angular_velocity(self):
        if self._recent_orientation.has_none() or self._recent_timestamp.has_none():
            return 0
        return mo.angular_speed(
            self._recent_orientation.previous,
            self._recent_orientation.current,
            self._recent_timestamp.previous,
            self._recent_timestamp.current,
        )

    def _store(self, timestamp, position):
        if len(self._stored) >= MAX_STORE_SIZE:
            first = list(self._stored.keys())[0]
            del self._stored[first]
        self._stored[timestamp] = position
