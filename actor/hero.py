from .recent_data import RecentData
import json


class Hero:
    def __init__(self, id, subscribers):
        self._id = id
        self._recent_data = {}
        self._subscribers = subscribers

    def on_position_data(self, id, type, timestamp, position):
        if id not in self._recent_data:
            self._recent_data[id] = RecentData()
        calculated = self._recent_data[id].update(timestamp, position)
        self._notify_subscribers(
            json.dumps(
                {
                    "id": id,
                    "type": type,
                    "timestamp": timestamp,
                    "data": {
                        "orientation": calculated.orientation
                        if calculated != None
                        else None,
                        "velocity": calculated.velocity if calculated != None else None,
                        "distance_to_hero": None,
                        "angle_to_hero": None,
                    },
                }
            )
        )
        # TODO When new data from other actors comes in, we need to check if data exists for that timestamp and inter-/extrapolate if necessary
        # TODO Write into database
        # TODO Write position additionally - it's removed from the notification
        # TODO Only check for more data if they're relevant (not hero) - checking distance afterwards, so we need to check that inside and stop

    def _notify_subscribers(self, data):
        for subscriber in self._subscribers:
            subscriber(data)
