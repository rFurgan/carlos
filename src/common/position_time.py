from carla import Vector3D
from typing import Union


class PositionTime:
    """
    A class used to store position data of a CARLA actor with their respective timestamp

    Methods
    -------
    update(position, timestamp)
        Reassigns the position and timestamp with given values
    get_position()
        Returns the position of the actor to the given time
    get_timestamp()
        Returns the timestamp of the actor of the given position
    has_none()
        Tells if the position or timestamp is set to 'None'
    """

    def __init__(self) -> None:
        """
        Parameters
        ----------

        Returns
        -------
        None
        """
        self._position: Union[Vector3D, None] = None
        self._timestamp: Union[float, None] = None

    def update(
        self, position: Union[Vector3D, None], timestamp: Union[float, None]
    ) -> None:
        """
        Reassigns the position and timestamp with given values

        Parameters
        ----------
        position : Vector3D | None
            The new 3d coordinates of the actor at the given time
        timestamp : Vector3D | None
            The new timestamp at which the actor is at the given coordinates

        Returns
        -------
        None
        """
        self._position = position
        self._timestamp = timestamp

    def get_position(self) -> Union[Vector3D, None]:
        """
        Returns the 3d coordinates of the actor at the given time

        Returns
        -------
        float
            The 3d coordinates of the actor at the given time
        None
            Insufficient data
        """
        return self._position

    def get_timestamp(self) -> Union[float, None]:
        """
        Returns the timestamp at which the actor is at the given coordinates

        Returns
        -------
        float
            The timestamp at which the actor is at the given coordinates
        None
            Insufficient data
        """
        return self._timestamp

    def has_none(self) -> bool:
        """
        Tells if the position or timestamp is set to 'None'

        Returns
        -------
        bool
            Wheter position or timestamp is set to 'None'
        """
        return self._position == None or self._timestamp == None
