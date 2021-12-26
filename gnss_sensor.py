from datatypes.geoposition import Geoposition


class GnssSensor:

    def __init__(
        self,
        actor,
        world,
        on_data,
        update_timer=1.0,
        factor=100000
    ):
        self._actor = actor
        self._on_data = on_data
        self._update_timer = update_timer
        self._ref_timestamp = 0
        self._factor = factor

        self._sensor = world.spawn_actor(
            world.get_blueprint_library().find("sensor.other.gnss"),
            self._actor.get_transform(),
            self._actor,
        )
        self._sensor.listen(lambda event: self._on_gnss_event(event))

    def __del__(self):
        self._sensor.destroy()

    def get_actor_id(self):
        return self._actor.id

    def _on_gnss_event(self, event):
        if event.timestamp - self._ref_timestamp >= self._update_timer:
            self._on_data(
                round(event.timestamp, 1),
                Geoposition(
                    longitude = event.longitude * self._factor,
                    latitude = event.latitude * self._factor,
                    altitdue = event.altitude * self._factor,
                ),
            )
            self._ref_timestamp = event.timestamp
