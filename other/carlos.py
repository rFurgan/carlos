# import glob
import math

# import os
# import sys
import time

# import thread
from random import randint

# try:
#     sys.path.append(
#         glob.glob(
#             "../carla/dist/carla-*%d.%d-%s.egg"
#             % (
#                 sys.version_info.major,
#                 sys.version_info.minor,
#                 "win-amd64" if os.name == "nt" else "linux-x86_64",
#             )
#         )[0]
#     )
# except IndexError:
#     pass

import carla
from carla.libcarla import Vector3D


class RoadUser:
    def __init__(self, id, position):
        self.__id = id
        self.__currentPosition = position
        self.__previousPosition = Vector3D(0, 0, 0)
        self.__orientation = 0
        self.__velocity = 0

    def getId(self):
        return self.__id

    def getCurrentPosition(self):
        return self.__currentPosition

    def getPreviousPosition(self):
        return self.__previousPosition

    def getOrientation(self):
        return self.__orientation

    def getVelocity(self):
        return self.__velocity

    def setPosition(self, position):
        self.__previousPosition = self.__currentPosition
        self.__currentPosition = self.__addCoordinateDeviation(position)
        self.__updateStats()

    def __addCoordinateDeviation(self, position, deviationStart=-10, deviationEnd=10):
        position.x = position.x + randint(deviationStart, deviationEnd)
        position.y = position.y + randint(deviationStart, deviationEnd)
        position.z = position.z + randint(deviationStart, deviationEnd)
        return position

    def __updateStats(self):
        self.__calculateOrientation()
        self.__calculateVelocity()
        self.__calculateDistance()

    def __calculateOrientation(self):
        self.__orientation = self.__vectorAngle()

    def __vectorLength(self, x, y):
        a = pow(x, 2)
        b = pow(y, 2)
        return math.sqrt(a) + math.sqrt(b)

    def __vectorAngle(self):
        vectorX = [
            self.__currentPosition.x - self.__previousPosition.x,
            self.__previousPosition.y,
        ]
        vectorY = [
            self.__currentPosition.x - self.__previousPosition.y,
            self.__currentPosition.y,
        ]
        return math.atan(
            self.__vectorLength(vectorY[0], vectorY[1]),
            self.__vectorLength(vectorX[0], vectorX[1]),
        )


class Carlos:
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
            if actor.getDistance() <= relevantDistance:
                relevantActors.append(actor)
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
                        actor.id, actor.get_location()
                    )
                else:
                    self.__allActors[actor.id].setPosition(actor.get_location())
            time.sleep(0.5)
        for actorKey in self.__allActors.keys:
            print(self.__allActors[actorKey])
