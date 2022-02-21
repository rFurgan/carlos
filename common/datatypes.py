class Vector:
    """Class to represent a 3D vector

    Args:
        x (float): x component of vector
        y (float): y component of vector
        z (float): z component of vector
    """
    def __init__(self, x: float, y: float, z: float) -> None:
        self._x: float = x
        self._y: float = y
        self._z: float = z

    @property
    def x(self) -> float:
        """
        Returns:
            float: x component of vector"""
        return self._x

    @property
    def y(self) -> float:
        """
        Returns:
            float: y component of vector"""
        return self._y

    @property
    def z(self) -> float:
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
    def __init__(self, x: float, y: float, z: float):
        self._x: float = x
        self._y: float = y
        self._z: float = z

    @property
    def x(self) -> float:
        """
        Returns:
            float: x component of coordinate"""
        return self._x

    @property
    def y(self) -> float:
        """
        Returns:
            float: y component of coordinate"""
        return self._y

    @property
    def z(self) -> float:
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
    def __init__(self, previous: any, current: any) -> None:
        self._previous: any = previous
        self._current: any = current

    @property
    def previous(self) -> any:
        """
        Returns:
            any: Previously stored data"""
        return self._previous

    @property
    def current(self) -> any:
        """
        Returns:
            any: Most recently stored data"""
        return self._current

    @previous.setter
    def previous(self, previous: any) -> None:
        """
        Args:
            previous (any): Value to set previous"""
        self._previous = previous

    @current.setter
    def current(self, current: any) -> None:
        """
        Args:
            current (any): Value to set current"""
        self._current = current

    def has_none(self) -> bool:
        """Check if either previous or current is set to None
        
        Returns:
            bool: True if one of the attributes set to None, False otherwise
        """
        return self._current == None or self._previous == None
