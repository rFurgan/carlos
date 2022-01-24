from datatypes import Geoposition


class GnssReceiver:
    def __init__(self, actor, world, on_data):
        self._actor = actor
        self._on_data = on_data
        self._sensor = world.spawn_actor(
            world.get_blueprint_library().find("sensor.other.gnss"),
            self._actor.get_transform(),
            self._actor,
        )
        self._sensor.listen(lambda event: self._on_gnss_event(event))

    def __del__(self):
        self._sensor.destroy()

    def _on_gnss_event(self, event):
        self._on_data(
            self._actor.id,
            event.timestamp,
            Geoposition(
                longitude=event.longitude,
                latitude=event.latitude,
                altitude=event.altitude,
            ),
        )
