from datatypes import CalculatedData, Data

class Hero:
    def __init__(self, id, tolerance):
        self._id = id
        self._tolerance = tolerance
        # self._database = Database()
        self._subscription_callbacks = []

    def on_position_data(self, id, timestamp, position):
        # TODO
        for callback in self._subscription_callbacks:
            # TODO ----------------------------------------------v--v--v--v
            callback(Data(id, timestamp,CalculatedData(position, 0, 0, 0, 0)))

    def subscribe(self, callback):
        self._subscription_callbacks.append(callback)