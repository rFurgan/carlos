import time
import carla
import threading
from roaduser import RoadUser

# TODO
# - Comments


class API:
    def __init__(self, host="127.0.0.1", port=2000) -> None:
        try:
            self.__actors = {}
            self.__client = None
            self.__world = None
            self.__thread = None
            self.__connect_to_world(host, port)
        except:
            print(f"[ERROR][{self.__init__.__name__}] Failed to instantiate class")
            raise SystemExit

    def start_polling_coordinates(self, interval_timer=0.5) -> None:
        self.__thread = self.__set_interval(self.__poll_coordinates, interval_timer)
        self.__thread.start()

    def stop_polling_coordinates(self) -> None:
        if self.__thread != None:
            self.__thread.cancel()
            return
        print(f"[ERROR][{self.stop_polling_coordinates.__name__}] No thread to cancel")

    def get_relevant_actors(self, relevant_distance=10) -> list:
        relevant_actors = []
        for id in self.__actors:
            actor = self.__actors[id]
            if actor.get_distance() <= relevant_distance:
                relevant_actors.append(actor)
        return relevant_actors

    def __connect_to_world(self, host, port) -> None:
        self.__client = carla.Client(host, port)
        self.__client.set_timeout(2.0)
        self.__world = self.__client.get_world()

    def __poll_coordinates(self) -> None:
        for actor in self.__world.get_actors():
            if not (actor.id in self.__actors.keys()):
                self.__actors[actor.id] = RoadUser(
                    actor.id,
                    actor.get_location(),
                    actor.get_location(),  # Should be coordinates of "us"
                    time.perf_counter_ns(),
                )
            else:
                self.__actors[actor.id].set_position(
                    actor.get_location(),
                    actor.get_location(),  # Should be coordinates of "us"
                    time.perf_counter_ns(),
                )

    # author: stamat
    # https://gist.github.com/stamat/5371218
    def __set_interval(self, function, seconds):
        def function_wrapper():
            self.__set_interval(function, seconds)
            function()

        return threading.Timer(seconds, function_wrapper)
