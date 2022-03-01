import json
import carla
import logging
import time
import sys
from api import Api

LOCAL_HOST: str = "127.0.0.1"
LOCAL_PORT: int = 2000
RELEVANCE_RADIUS: int = 50000
MAX_ENTRY_COUNT: int = 10


def change_world(map: str, host: str, port: int) -> None:
    """Method to change Carla world to the provided map

    Args:
        map (str): Map to change to
        host (str): Host adress of the Carla world
        port (int): Port adress of the Carla world
    """
    try:
        client: carla.Client = carla.Client(host, port)
        client.set_timeout(2.0)
        client.load_world(map)
    except RuntimeError as err:
        logging.error(
            f"Failed to connect to CARLA world {host}:{port} due to error: {err}"
        )


def pretty_print(jd):
    print(json.loads(jd))


if __name__ == "__main__":
    # if input("Change map?") == "y":
    #     change_world("Town03", LOCAL_HOST, LOCAL_PORT)
    #     input(
    #         "Wait until map changed and spawn the actors. Now press any key to continue"
    #     )

    a: Api = Api(LOCAL_HOST, LOCAL_PORT, RELEVANCE_RADIUS, MAX_ENTRY_COUNT)
    if len(sys.argv) > 1:
        error_range = sys.argv[1]
        a.start(0.5, error_range)
        for _ in range(600):
            a.save_csv(r"C:\Users\daydr\Desktop", f"Map_03_{error_range}m_error.csv")
            time.sleep(8)
        a.stop()
