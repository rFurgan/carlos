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

    def has_none(self):
        return self._current == None or self._previous == None
