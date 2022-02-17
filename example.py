from api import Api
from carla import Client
import common
import logging
import json
import time


def change_world(map, host, port):
    try:
        client = Client(host, port)
        client.set_timeout(2.0)
        client.load_world(map)
    except RuntimeError as error:
        logging.error(
            f"Failed to connect to CARLA world {host}:{port} due to error: {error}"
        )


def pretty_print(json_data):
    data = json.loads(json_data)
    print(
        f"ID: {data['id']}\nO: {data['data']['orientation']}\nV: {data['data']['velocity']}\nD: {data['data']['distance_to_hero']}\nA: {data['data']['angle_to_hero']}\n-------"
    )


if __name__ == "__main__":
    if input("Change map?") == "y":
        change_world("Town02", common.LOCAL_HOST, common.LOCAL_PORT)
        input(
            "Wait until map changed and spawn the actors. Now press any key to continue"
        )
    a = Api(common.LOCAL_HOST, common.LOCAL_PORT)
    # input("Press ENTER to end")
    a.start(0.5)
    for i in range(300):
        time.sleep(6)
        a.save_csv()
        print(f"SAVE {i}")
    a.stop()
