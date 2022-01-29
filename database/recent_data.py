from common.datatypes import Recent, Data
from common.operations import Operations

class RecentData:

    def __init__(self, expiration_time=3):
        self._expiration_time = expiration_time
        self._timestamp = Recent()
        self._position = Recent()

    def update(self, timestamp, position):
        # Check if it's not old data if there is data
        if (self._timestamp.current == None or (self._timestamp.current != None and timestamp > self._timestamp.current)):
            # Check for data expiration
            if (timestamp - self._timestamp.current >= self._expiration_time):
                self._timestamp.current = None

            self._timestamp.previous = self._timestamp.current
            self._timestamp.current = timestamp

            if (self._timestamp.previous != None):            
                self._position.previous = self._position.current
                self._position.current = position

                vector = Operations.get_vector(self._position.current, self._position.previous)
                orientation = Operations.get_angle_to_y_axis(vector)
                velocity = Operations.get_velocity(vector, self._timestamp.previous, self._timestamp.current)

                return Data(position, orientation, velocity)
