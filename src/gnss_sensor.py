from typing import Callable, Union
from carla import World, Actor, Vector3D, Sensor, GNSSMeasurement
import weakref

"""
This class is highly influenced by the class `GnssSensor` from
https://github.com/carla-simulator/carla/blob/master/PythonAPI/examples/manual_control.py:893
with slight changes
"""


class GnssSensor:
    """
    A class to attach a GNSS sensor to a CARLA actor

    A class attaches a GNSS sensor to a CARLA actor tracking its movement asynchronically calling the callback function with the timestamp and positional data

    Methods
    -------
    get_actor_id()
        Returns the id of the actor the sensor is attached to
    _on_gnss_event()
        Method to be called when new data from the sensor arrives
    """

    def __init__(
        self,
        actor: Actor,
        world: World,
        update: Callable[[Vector3D, float], None],
        update_timer: float = 1.0,
    ) -> None:
        """
        Parameters
        ----------
        _actor : Actor
            CARLA Actor to which the sensor will be attached to
        _update : Callable
            External method to update the newly arrived data
        _update_timer : float
            Interval timer in seconds how often the data should be updated
        _ref_timestamp : flaot | None
            Timestamp reference to keep track of the previous timestamp
        _sensor : Sensor
            Reference to the created GNSS sensor

        Returns
        -------
        None
        """
        self._actor: Actor = actor
        self._update: Callable = update
        self._update_timer: float = update_timer
        self._ref_timestamp: Union[float, None] = None
        self._sensor: Sensor = world.spawn_actor(
            world.get_blueprint_library().find("sensor.other.gnss"),
            self._actor.get_transform(),
            attach_to=self._actor,
        )
        weak_self = weakref.ref(self)
        self._sensor.listen(lambda event: GnssSensor._on_gnss_event(weak_self, event))

    def __del__(self) -> None:
        """
        Parameters
        ----------

        Returns
        -------
        None
        """
        self._sensor.destroy()

    def get_actor_id(self) -> int:
        """
        Returns the id of the CARLA actor to which the GNSS sensor is attached to

        Parameters
        ----------

        Returns
        -------
        int
            CARLA actor id to which the GNSS sensor is attached to
        """
        return self._actor_id

    @staticmethod
    def _on_gnss_event(weak_self: weakref, event: GNSSMeasurement) -> None:
        """
        Method to be called when new GNSS sensor data arrives

        Checks the timestamp and updates the data with the referenced external method if the defined update interval is reached

        Parameters
        ----------
        weak_self : weakref
            Weak reference to the object itself
        event: GNSSMeasurement
            GNSS data including timestamp, frame, latitude, longitude, altitude and transform

        Returns
        -------
        None
        """
        self = weak_self()
        if not self:
            return
        if self._ref_timestamp == None:
            self._ref_timestamp = event.timestamp
        else:
            diff = event.timestamp - self._ref_timestamp
            if diff >= self._update_timer:
                self._update(
                    Vector3D(event.latitude, event.longitude, event.altitude),
                    event.timestamp,
                )
                self._ref_timestamp = event.timestamp
