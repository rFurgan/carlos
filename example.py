import carla
import common
import logging
from api import Api


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
    except RuntimeError as error:
        logging.error(
            f"Failed to connect to CARLA world {host}:{port} due to error: {error.message}"
        )


if __name__ == "__main__":
    if input("Change map?") == "y":
        change_world("Town02", common.LOCAL_HOST, common.LOCAL_PORT)
        input(
            "Wait until map changed and spawn the actors. Now press any key to continue"
        )
    a: Api = Api(common.LOCAL_HOST, common.LOCAL_PORT, 50000, 10)
    a.start(0.5)
    input("Press ENTER to end")
    a.save_csv(r"C:\Users\Pepe\Desktop", "data.csv")
    a.stop()
