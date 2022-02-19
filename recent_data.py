from common import Recent, MAX_STORE_SIZE
import math_operations as mo


class RecentData:
    """Class to store the most recent data and provide velocity, orientation and angular velocity

    Args:
        expiration_time (float): Time in seconds when the stored current timestamp and position is expired
    """
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
        """Returns the dictionary with the positions on the corresponding timestamps
        
        Returns:
            dict[float, Coordinate]: Dictionary with the most recent timestamps and the corresponding positions 
        """
        return self._stored

    def update(self, timestamp, position):
        """Updates the previous and current timestamp and position returning the calculated data
        
        Args:
            timestamp (float): Most recent timestamp to save
            position (Coordinate): Most recent position to save

        Returns:
            None, None, None: Insufficient data to calculate velocity, orientation and angular velocity
            float, float, float: Current velocity, orientation and angular velocity
        """
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
        """Calculates and returns the current velocity
        
        Args:
            vec (Vector): Vector of most recent covered distance

        Returns:
            float: Current velocity
        """
        self._velocity = mo.velocity(
            vec, self._recent_timestamp.previous, self._recent_timestamp.current
        )
        return self._velocity

    def _get_orientation(self, vec):
        """Calculates and returns the current orientation
        
        Args:
            vec (Vector): Vector of most recent covered distance

        Returns:
            float: Current orientation
        """
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
        """Calculates and returns the current angular velocity
        
        Returns:
            float: Current angular velocity
        """
        if self._recent_orientation.has_none() or self._recent_timestamp.has_none():
            return 0
        return mo.angular_speed(
            self._recent_orientation.previous,
            self._recent_orientation.current,
            self._recent_timestamp.previous,
            self._recent_timestamp.current,
        )

    def _store(self, timestamp, position):
        """Stores the most recent position and corresponding timestamp
        
        Args:
            timestamp (float): Timestamp of most recent detected position
            position (Coordinate): Most recent detected position

        Returns:
            float: Current position
        """
        if len(self._stored) >= MAX_STORE_SIZE:
            first = list(self._stored.keys())[0]
            del self._stored[first]
        self._stored[timestamp] = position
