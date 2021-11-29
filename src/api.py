from carla import Client, World
from time import perf_counter_ns
from threading import Thread, Timer
from typing import Union, List, Callable
from roaduser import RoadUser

# TODO
# - Comments


class API:
    def __init__(self, host: str = "127.0.0.1", port: int = 2000) -> None:
        try:
            self.__actors: dict[int, RoadUser] = {}
            self.__client: Union[Client, None] = None
            self.__world: Union[World, None] = None
            self.__thread: Union[Thread, None] = None
            self.__cancel_thread: bool = False
            self.__connect_to_world(host, port)
        except:
            print(f"[ERROR][{self.__init__.__name__}] Failed to instantiate class")
            raise SystemExit

    def start_polling_coordinates(self, timer: float = 0.5) -> None:
        self.__thread = self.__set_interval(self.__poll_coordinates, timer)
        self.__thread.start()

    def stop_polling_coordinates(self) -> None:
        self.__cancel_thread = True
        if self.__thread != None:
            self.__thread.cancel()
            return
        print(f"[ERROR][{self.stop_polling_coordinates.__name__}] No thread to cancel")

    def get_actors(self) -> List[RoadUser]:
        return list(self.__actors.values())

    def get_relevant_actors(self, relevant_distance=10) -> List[RoadUser]:
        relevant_actors: List[RoadUser] = []
        for id in self.__actors:
            actor: RoadUser = self.__actors[id]
            distance = actor.get_distance()
            if distance is not None and distance <= relevant_distance:
                relevant_actors.append(actor)
        return relevant_actors

    def __connect_to_world(self, host: str, port: int) -> None:
        self.__client = Client(host, port)
        self.__client.set_timeout(2.0)
        self.__world = self.__client.get_world()

    def __poll_coordinates(self, timer: float) -> None:
        self.start_polling_coordinates(timer)
        for actor in self.__world.get_actors():
            if not (actor.id in self.__actors.keys()):
                self.__actors[actor.id] = RoadUser(
                    actor.id,
                    actor.get_location(),
                    self.__world.get_actor(
                        10
                    ).get_location(),  # Should be coordinates of "us"
                    perf_counter_ns(),
                )
            else:
                self.__actors[actor.id].set_position(
                    actor.get_location(),
                    self.__world.get_actor(
                        10
                    ).get_location(),  # Should be coordinates of "us"
                    perf_counter_ns(),
                )

    def __set_interval(self, function: Callable, timer: float) -> Union[Thread, None]:
        if self.__cancel_thread:
            return None
        return Timer(timer, function, [timer])
