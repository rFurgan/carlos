from recent_data import RecentData
from common.datatypes import Coordinate

# TODO Hero
# TODO -> When new data from other actors comes in, we need to check if data exists for that timestamp and inter-/extrapolate if necessary


class Hero:
    def __init__(self, id):
        self._id = id
        self._recent_data = {}

    def on_position_data(self, id, timestamp, position):
        if id not in self._recent_data:
            self._recent_data[id] = RecentData()
        temp = self._recent_data[id].update(timestamp, position)
        if temp != None and temp.velocity != None and temp.orientation != None:
            print(f"ID: {id} - Velocity: {round(temp.velocity)}")
        # TODO What to do with this data?
        # TODO -> Either make it subscribable or send it via Socket (?)
        # TODO Only check for more data if they're relevant (not hero) - checking distance afterwards, so we need to check that inside and stop
