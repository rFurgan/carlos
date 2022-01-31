from common.datatypes import Coordinate
from datetime import datetime
from threading import Thread
from time import sleep


class GnssReceiver:
    def __init__(
        self,
        actor,
        on_data,
        sensor_tick=1,
    ):
        self._actor = actor
        self._on_data = on_data
        self._sensor_tick = sensor_tick
        self._stop = False
        self._sensor = Thread(target=self._request_gnss_data)
        self._sensor.daemon = True
        self._sensor.start()

    def _request_gnss_data(self):
        location = self._actor.get_transform().location
        timestamp = datetime.now().second
        self._on_data(
            self._actor.id,
            timestamp,
            Coordinate(
                x=location.x,
                y=location.y,
                z=location.z,
            ),
        )
        sleep(self._sensor_tick)
        self._request_gnss_data()
