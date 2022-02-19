from api import Api
from carla import Client
import common
import logging
import json
import time


def change_world(map, host, port):
    """Method to change Carla world to the provided map

    Args:
        map (str): Map to change to
        host (str): Host adress of the Carla world
        port (int): Port adress of the Carla world
    """
    try:
        client = Client(host, port)
        client.set_timeout(2.0)
        client.load_world(map)
    except RuntimeError as error:
        logging.error(
            f"Failed to connect to CARLA world {host}:{port} due to error: {error}"
        )


if __name__ == "__main__":
    if input("Change map?") == "y":
        change_world("Town02", common.LOCAL_HOST, common.LOCAL_PORT)
        input(
            "Wait until map changed and spawn the actors. Now press any key to continue"
        )
    a = Api(common.LOCAL_HOST, common.LOCAL_PORT, 50000, 10)
    a.start(0.5)
    input("Press ENTER to end")
    # for i in range(300):
    #     time.sleep(6)
    #     a.save_csv(r"C:\Users\Pepe\Desktop", "data.csv")
    #     print(f"SAVE {i}")
    a.stop()
