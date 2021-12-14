from carla import Client, World
from typing import Union, List, Dict
from gnss_sensor import GnssSensor
from common.logger import Logger, LogType
from road_user import RoadUser
from json import dumps


class Api:
    """
    A class to communicate with the host CARLA world

    A class to keep track of all actors in the connected CARLA world by attaching sensors and creating a local database of all detected actors.

    Methods
    -------
    start()
        Connects to the host CARLA world and makes preparations to keep track of all detected actors
    stop()
        Stops tracking all detected actors
    get_data(id=None)
        Returns data of all detected actors in JSON format
    _connect_to_world(host, port)
        Connects to CARLA world with given ip address and port number
    _prepare_actors()
        Detects all actors in the connected CARLA world and makes preparations to keep track of them
    _destroy_gnss_sensors()
        Detaches and deletes all GNSS sensors
    _destroy_road_users()
        Deletes all data of actors being kept track of
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 2000) -> None:
        """
        Parameters
        ----------
        host : str, optional
            The ip address of the host world
        port : int, optional
            The port number from which to connect to the host world

        Returns
        -------
        None
        """
        self._host: str = host
        self._port: int = port
        self._gnss_sensors: Dict[int, GnssSensor] = {}
        self._road_users: Dict[int, RoadUser] = {}
        self._client: Union[Client, None] = None
        self._world: Union[World, None] = None
        self._logger: Logger = Logger(Api.__name__)

    def __del__(self) -> None:
        """
        Parameters
        ----------

        Returns
        -------
        None
        """
        self._logger.log(LogType.INFO, "Quitting")
        self._destroy_gnss_sensors()
        self._destroy_road_users()

    def start(self) -> None:
        """
        Connects to the host CARLA world and makes preparations to keep track of all detected actors

        Parameters
        ----------

        Returns
        -------
        None
        """
        self._logger.log(LogType.INFO, "Starting")
        self._connect_to_world(self._host, self._port)
        self._prepare_actors()

    def stop(self) -> None:
        """
        Stops tracking all detected actors

        Parameters
        ----------

        Returns
        -------
        None
        """
        self._logger.log(LogType.INFO, "Stopping")
        self._destroy_gnss_sensors()

    def get_data(self, id: int = None) -> str:
        """
        Returns data of all detected actors in JSON format

        Returns either the data of all detected actors for the whole timespan the program ran or by providing an id it returns all the data only from the actor of the given id
        Example of the format:
        {
            "1": {
                "1005.4651102274656": {
                    "orientation": 20.823125854342642,
                    "velocity": 34.124251258543421,
                    "distance": 10.534968201994212
                },
                "1006.4651102274656": {
                    "orientation": 20.823125854342642,
                    "velocity": 35.324251258849532,
                    "distance": 11.684032985021244
                },
            },
            "2": {
                "1005.4651102274656": {
                    "orientation": 13.23908235091124,
                    "velocity": 34.234523634234256,
                    "distance": 15.234523634234256
                },
                "1006.4651102274656": {
                    "orientation": 13.23908235091124,
                    "velocity": 34.234523634234256,
                    "distance": 17.236536234234256
                },
            }
        }

        Paramters
        ---------
        id : int
            Option to only get data of the actor with the given id (default is None)

        Returns
        -------
        str
            Data of the actor(s) in JSON format (see example above)
        """
        if id == None:
            dataset = {}
            for road_user in self._road_users:
                dataset[road_user] = self._road_users[road_user].get_data()
            return dumps(dataset)
        return dumps(self._road_users[id].get_data())

    def get_recent_data(self, id: int = None) -> str:
        """
        Returns most recent data of all detected actors in JSON format

        Returns either the most recent data of all detected actors or by providing an id it returns the most recent data only from the actor of the given id
        Example of the format:
        {
            "1": {
                "1005.4651102274656": {
                    "orientation": 20.823125854342642,
                    "velocity": 34.124251258543421,
                    "distance": 10.534968201994212
                },
            },
            "2": {
                "1005.4651102274656": {
                    "orientation": 13.23908235091124,
                    "velocity": 34.234523634234256,
                    "distance": 15.234523634234256
                },
            }
        }

        Paramters
        ---------
        id : int
            Option to only get data of the actor with the given id (default is None)

        Returns
        -------
        str
            Most recent data of the actor(s) in JSON format (see example above)
        """
        if id == None:
            dataset = {}
            for road_user in self._road_users:
                dataset[road_user] = self._road_users[road_user].get_recent_data()
            return dumps(dataset)
        return dumps(self._road_users[id].get_recent_data())

    def _connect_to_world(self, host: str, port: int) -> None:
        """
        Connects to CARLA world with given ip address and port number

        Parameters
        ----------
        host : str, optional
            The ip address of the host world
        port : int, optional
            The port number from which to connect to the host world

        Raises
        ------
        SystemExit
            If the connection to the host world failed

        Returns
        -------
        None
        """
        self._logger.log(LogType.INFO, "Connecting to host world")
        try:
            if self._client == None:
                self._client = Client(host, port)
                self._client.set_timeout(2.0)
            if self._world == None:
                self._world = self._client.get_world()
        except:
            self._logger.log(LogType.ERROR, "Failed to connect to host world")
            raise SystemExit

    def _prepare_actors(self) -> None:
        """
        Detects all actors in the connected CARLA world and makes preparations to keep track of them

        Parameters
        ----------

        Raises
        ------
        SystemExit
            If not connected to the host world

        Returns
        -------
        None
        """
        self._logger.log(LogType.INFO, "Preparing actors")
        if self._world == None:
            self._logger.log(
                LogType.ERROR,
                "Failed to prepare actors",
            )
            raise SystemExit
        road_user_ids: List[int] = list(self._road_users.keys())
        gnss_sensor_ids: List[int] = list(self._gnss_sensors.keys())
        for actor in self._world.get_actors():
            if actor.id not in road_user_ids:
                self._road_users[actor.id] = RoadUser(actor.id)
            if actor.id not in gnss_sensor_ids:
                self._gnss_sensors[actor.id] = GnssSensor(
                    actor, self._world, self._road_users[actor.id].update
                )

    def _destroy_gnss_sensors(self) -> None:
        """
        Detaches and deletes all GNSS sensors

        Parameters
        ----------

        Returns
        -------
        None
        """
        self._logger.log(LogType.INFO, "Destroying GNSS sensors")
        for sensor_id in list(self._gnss_sensors):
            del self._gnss_sensors[sensor_id]

    def _destroy_road_users(self) -> None:
        """
        Deletes all data of actors being kept track of

        Parameters
        ----------

        Returns
        -------
        None
        """
        self._logger.log(LogType.INFO, "Destroying RoadUser instances")
        for road_user_id in list(self._road_users):
            del self._road_users[road_user_id]
