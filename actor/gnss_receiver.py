from datetime import datetime
from threading import Thread
from time import sleep, time
from common import VehicleTypes, EActorType, Coordinate


class GnssReceiver:
    def __init__(
        self,
        actor,
        on_data,
        sensor_tick,
    ):
        self._actor = actor
        self._on_data = on_data
        self._type = self._classify(actor.type_id)
        self._sensor_tick = sensor_tick
        self._stop = False
        self._sensor = Thread(target=self._request_gnss_data)
        self._sensor.daemon = True
        self._sensor.start()

    def stop(self):
        self._stop = True
        self._sensor.join()

    def _classify(self, actor_type):
        for category in list(VehicleTypes.types.keys()):
            for type in VehicleTypes.types[category]:
                if type in actor_type:
                    return category.value
        return EActorType.PEDESTRIAN.value

    def _request_gnss_data(self):
        while not self._stop:
            current_time = round(time(), 3)
            location = self._actor.get_transform().location
            time_now = datetime.now()
            timestamp = time_now.second + round(time_now.microsecond / 1000000, 3)
            self._on_data(
                self._actor.id,
                self._type,
                timestamp,
                Coordinate(
                    x=location.x,
                    y=location.y,
                    z=location.z,
                ),
            )
            rest_time = round(time(), 3) - current_time
            rest_sleep = self._sensor_tick - rest_time
            if rest_sleep > 0:
                sleep(self._sensor_tick)
