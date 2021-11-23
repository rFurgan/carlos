import time
import carla
from RoadUser import RoadUser

# TODO
# - Comments
# - Return types
# Thread implementation
# Mutex


class API:
    def __init__(self, host="127.0.0.1", port=2000):
        self.__allActors = {}
        self.__client = None
        self.__world = None
        self.__connectToWorld(host, port)

    def startPollingCoordinates(self):
        self.__pollCoordinates()
        # thread.start_new_thread()

    def stopPollingCoordinates(self):
        # Kill thread
        pass

    def getRelevantActors(self, relevantDistance=10):
        relevantActors = []
        for actor in self.__allActors:
            print(actor)
            # if actor.getDistance() <= relevantDistance:
            #     relevantActors.append(actor)
        return relevantActors

    def __connectToWorld(self, host, port):
        self.__client = carla.Client(host, port)
        self.__client.set_timeout(2.0)
        self.__world = self.__client.get_world()

    def __pollCoordinates(self):
        # while True:
        for i in range(10):
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
            time.sleep(0.5)
