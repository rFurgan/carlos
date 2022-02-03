from time import sleep
from carla import Client
from common import EActorType, LOCAL_PORT, LOCAL_HOST
import logging
import json
import api


# DEBUG
def change_world(map, host, port):
    try:
        client = Client(host, port)
        client.set_timeout(2.0)
        client.load_world(map)
    except RuntimeError:
        logging.error(f"Failed to connect to CARLA world {host}:{port}.")


# DEBUG
def get_a_hero(host, port):
    try:
        client = Client(host, port)
        client.set_timeout(2.0)
        world = client.get_world()
        for actor in world.get_actors():
            if EActorType.VEHICLE.value in actor.type_id:
                return actor.id
        raise
    except RuntimeError:
        logging.error(f"Failed to connect to CARLA world {host}:{port}.")
        exit()


# DEBUG
def pretty_print(json_data):
    data = json.loads(json_data)
    print(
        f"{data['id']}\nType: {data['type']}\nTimestamp: {data['timestamp']}\nVelocity: {data['data']['velocity']}\nOrientation: {data['data']['orientation']}\n----"
    )


if __name__ == "__main__":
    # change_world("Town02", LOCAL_HOST, LOCAL_PORT)
    api = Api(get_a_hero(LOCAL_HOST, LOCAL_PORT), LOCAL_HOST, LOCAL_PORT)
    api.subscribe(pretty_print)
    sleep(1000)
    del api
