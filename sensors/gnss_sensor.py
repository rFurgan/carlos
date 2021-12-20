from carla import Vector3D

"""
This class is influenced by the class 'GnssSensor' from
https://github.com/carla-simulator/carla/blob/master/PythonAPI/examples/manual_control.py:893
with slight changes
"""


class GnssSensor:
    """
    A class to generate and attach an GNSS sensor to the defined actor
    """

    def __init__(
        self,
        actor,
        world,
        on_data,
        update_timer=1.0,
    ):
        """
        Args:
            `actor          (Actor):`     Actor to which the GNSS sensor will be attached to
            `world          (World):`     World in which the actor is and the sensor will be spawned
            `on_data        (Callable):`        Method to be called when sensor data arrives
            `update_timer   (float, optional):` Time interval how often actual sensor data should be forwarded

        Returns:
            `None`
        """
        self._on_data = on_data
        self._update_timer = update_timer
        self._ref_timestamp = 0
        self._sensor = world.spawn_actor(
            world.get_blueprint_library().find("sensor.other.gnss"),
            actor.get_transform(),
            attach_to=actor,
        )
        self._sensor.listen(lambda event: self._on_gnss_event(event))

    def __del__(self):
        """
        Returns:
            `None`
        """
        self._sensor.destroy()

    def _on_gnss_event(self, event):
        """
        Method to be called when new sensor data arrives. Prepares and forwards the data to the attached RoadUser class of the corresponding actor

        Args:
            `event (GNSSMeasurement):` Sensor data containing a timestamp, latitude, longitude and altitude data

        Returns:
            `None`
        """
        factor = 100000
        if event.timestamp - self._ref_timestamp >= self._update_timer:
            self._on_data(
                round(event.timestamp, 1),
                Vector3D(
                    event.latitude * factor,
                    event.longitude * factor,
                    event.altitude * factor,
                ),
            )
            self._ref_timestamp = event.timestamp
