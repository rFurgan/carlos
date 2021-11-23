import time
import carla
import threading
from RoadUser import RoadUser

# TODO
# - Comments


class API:
    def __init__(self, host="127.0.0.1", port=2000) -> None:
        self.__allActors = {}
        self.__client = None
        self.__world = None
        self.__thread = self.__set_interval(self.__pollCoordinates, 0.5)
        self.__connectToWorld(host, port)

    def startPollingCoordinates(self) -> None:
        self.__thread.start()

    def stopPollingCoordinates(self) -> None:
        self.__thread.cancel()

    def getRelevantActors(self, relevantDistance=10) -> list:
        relevantActors = []
        for id in self.__allActors:
            actor = self.__allActors[id]
            if actor.getDistance() <= relevantDistance:
                relevantActors.append(actor)
        return relevantActors

    def __connectToWorld(self, host, port) -> None:
        self.__client = carla.Client(host, port)
        self.__client.set_timeout(2.0)
        self.__world = self.__client.get_world()

    def __pollCoordinates(self) -> None:
        for actor in self.__world.get_actors():
            if not (actor.id in self.__allActors.keys()):
                self.__allActors[actor.id] = RoadUser(
                    actor.id,
                    actor.get_location(),
                    actor.get_location(),
                    time.perf_counter_ns(),
                )
            else:
                self.__allActors[actor.id].setPosition(
                    actor.get_location(),
                    actor.get_location(),
                    time.perf_counter_ns(),
                )

    # author: stamat
    # https://gist.github.com/stamat/5371218
    def __set_interval(self, function, seconds):
        def function_wrapper():
            self.__set_interval(function, seconds)
            function()

        return threading.Timer(seconds, function_wrapper)
