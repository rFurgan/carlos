class Vector:
    """Class to represent a 3D vector

    Args:
        x (float): x component of vector
        y (float): y component of vector
        z (float): z component of vector
    """
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        """
        Returns:
            float: x component of vector"""
        return self._x

    @property
    def y(self):
        """
        Returns:
            float: y component of vector"""
        return self._y

    @property
    def z(self):
        """
        Returns:
            float: z component of vector"""
        return self._z


class Coordinate:
    """Class to represent a 3D coordinate

    Args:
        x (float): x component of coordinate
        y (float): y component of coordinate
        z (float): z component of coordinate
    """
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        """
        Returns:
            float: x component of coordinate"""
        return self._x

    @property
    def y(self):
        """
        Returns:
            float: y component of coordinate"""
        return self._y

    @property
    def z(self):
        """
        Returns:
            float: z component of coordinate"""
        return self._z


class Recent:
    """Class to represent previous and current data

    Args:
        previous (any): Previous data
        previous (any): Most recent data
    """
    def __init__(self, previous, current):
        self._previous = previous
        self._current = current

    @property
    def previous(self):
        """
        Returns:
            float: Previously stored data"""
        return self._previous

    @property
    def current(self):
        """
        Returns:
            float: Most recently stored data"""
        return self._current

    @previous.setter
    def previous(self, previous):
        """
        Args:
            previous (any): Value to set previous"""
        self._previous = previous

    @current.setter
    def current(self, current):
        """
        Args:
            current (any): Value to set current"""
        self._current = current

    def has_none(self):
        """Check if either previous or current is set to None
        
        Returns:
            bool: True if one of the attributes set to None, False otherwise
        """
        return self._current == None or self._previous == None
