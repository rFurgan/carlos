class Vector:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

class Coordinate:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

class CalculatedData:

    def __init__(self, position, orientation, velocity, distance_to_hero, angle_to_hero):
        self._position = position
        self._orientation = orientation
        self._velocity = velocity
        self._distance_to_hero = distance_to_hero
        self._angle_to_hero = angle_to_hero

    @property
    def position(self):
        return self._position

    @property
    def orientation(self):
        return self._orientation

    @property
    def velocity(self):
        return self._velocity

    @property
    def distance_to_hero(self):
        return self._distance_to_hero

    @property
    def angle_to_hero(self):
        return self._angle_to_hero

class Data:
    def __init__(self, id, type, timestamp, data):
        self._id = id
        self._type = type
        self._timestamp = timestamp
        self._data = data

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def data(self):
        return self._data

class Recent:
    def __init__(self, previous, current):
        self._previous = previous
        self._current = current

    @property
    def previous(self):
        return self._previous

    @property
    def current(self):
        return self._current

    @previous.setter
    def previous(self, previous):
        self._previous = previous

    @current.setter
    def current(self, current):
        self._current = current


# # TODO Check
# class HeroData(NamedTuple):
#     distance_to_hero: float
#     angle_to_hero: int


# # TODO Check
# class CloseTimestamp(NamedTuple):
#     timestamp: float
#     type: ETimestampType
