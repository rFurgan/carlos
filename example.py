from api import Api
from carla import Client
import common as c
import logging
import json

from common.constants import LOCAL_HOST, LOCAL_PORT

# DEBUG
def change_world(map, host, port):
    try:
        client = Client(host, port)
        client.set_timeout(2.0)
        client.load_world(map)
    except RuntimeError as error:
        logging.error(
            f"Failed to connect to CARLA world {host}:{port} due to error: {error}"
        )


# DEBUG
def get_a_hero_id(host, port):
    try:
        client = Client(host, port)
        client.set_timeout(2.0)
        world = client.get_world()
        for actor in world.get_actors():
            if c.EActorType.VEHICLE.value in actor.type_id:
                return actor.id
        raise RuntimeError("No actors found to assign hero")
    except RuntimeError as error:
        logging.error(
            f"Failed to connect to CARLA world {host}:{port} due to error: {error}"
        )
        exit()


# DEBUG
def pretty_print(json_data):
    data = json.loads(json_data)
    print(
        f"ID: {data['id']}\nO: {data['data']['orientation']}\nV: {data['data']['velocity']}\nD: {data['data']['distance_to_hero']}\nA: {data['data']['angle_to_hero']}\n-------"
    )


if __name__ == "__main__":
    api = Api()
    # change_world("Town02", LOCAL_HOST, LOCAL_PORT)
    # input("Continue?")
    api.start(
        hero_id=get_a_hero_id(c.LOCAL_HOST, c.LOCAL_PORT),
        sim_host=LOCAL_HOST,
        sim_port=c.LOCAL_PORT,
        db_user=c.DB_USER,
        db_password=c.DB_PASSWORD,
        db_host=c.DB_HOST,
        db_port=c.DB_PORT,
        db_override=True,
    )
    api.subscribe(pretty_print)
    input("Press any key to end")
    del api
