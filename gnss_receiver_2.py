from common.datatypes import Geoposition
import carla


class GnssReceiver:
    def __init__(
        self,
        actor,
        world,
        on_data,
        sensor_tick=0,
        noise_alt_bias=0,
        noise_alt_stddev=0,
        noise_lat_bias=0,
        noise_lat_stddev=0,
        noise_lon_bias=0,
        noise_lon_stddev=0,
        noise_seed=0,
    ):
        self._actor = actor
        self._on_data = on_data

        gnss_bp = world.get_blueprint_library().find("sensor.other.gnss")
        gnss_bp.set_attribute("sensor_tick", str(sensor_tick))
        gnss_bp.set_attribute("noise_alt_bias", str(noise_alt_bias))
        gnss_bp.set_attribute("noise_alt_stddev", str(noise_alt_stddev))
        gnss_bp.set_attribute("noise_lat_bias", str(noise_lat_bias))
        gnss_bp.set_attribute("noise_lat_stddev", str(noise_lat_stddev))
        gnss_bp.set_attribute("noise_lon_bias", str(noise_lon_bias))
        gnss_bp.set_attribute("noise_lon_stddev", str(noise_lon_stddev))
        gnss_bp.set_attribute("noise_seed", str(noise_seed))

        self._sensor = world.spawn_actor(
            gnss_bp,
            # self._actor.get_transform(),
            carla.Transform(carla.Location(0, 0, 0)),
            self._actor,
        )
        self._sensor.listen(lambda event: self._on_gnss_event(event))

    def __del__(self):
        self._sensor.destroy()

    def _on_gnss_event(self, event):
        t = self._actor.get_transform()
        # print(
        #     f"{event.longitude} {event.latitude} {event.altitude}\n{t.location.x} {t.location.y} {t.location.z}"
        # )
        print(
            f"{event.longitude} {event.latitude} {event.altitude}\n{t.location.x} {t.location.y} {t.location.z}"
        )
        self._on_data(
            self._actor,  # TODO
            event.timestamp,
            Geoposition(
                longitude=event.longitude,
                latitude=event.latitude,
                altitude=event.altitude,
            ),
        )
