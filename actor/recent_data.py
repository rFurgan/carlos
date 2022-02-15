from common import Recent, MAX_STORE_SIZE, velocity, angle_to_y_axis, vector


class RecentData:
    def __init__(self, expiration_time=3):
        self._expiration_time = expiration_time
        self._timestamp = Recent(None, None)
        self._position = Recent(None, None)
        self._orientation = 0
        self._stored = {}

    @property
    def stored(self):
        return self._stored

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
                return None, None
            vec = vector(self._position.current, self._position.previous)
            return self._get_orientation(vec), self._get_velocity(vec)
        return None, None

    def _get_velocity(self, vec):
        time_difference = abs(self._timestamp.previous - self._timestamp.current)
        return velocity(vec, time_difference)

    def _get_orientation(self, vec):
        orientation = angle_to_y_axis(vec)
        if orientation != None:
            self._orientation = orientation
        return orientation if orientation != None else self._orientation

    def _store(self, timestamp, position):
        if len(self._stored) >= MAX_STORE_SIZE:
            first = list(self._stored.keys())[0]
            del self._stored[first]
        self._stored[timestamp] = position
