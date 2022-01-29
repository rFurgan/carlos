from time import sleep
from api import Api
from carla import Client
from common.datatypes import EActorType

# TODO delete
# DEBUG
def change_world(host="127.0.0.1", port=2000):
    try:
        client = Client(host, port)
        client.set_timeout(2.0)
        client.load_world("Town01")
    except RuntimeError:
        print(f"[ERROR] Failed to connect to CARLA world ${host}:${port}.")
        exit()

# TODO delete
# DEBUG
def get_a_hero(host="127.0.0.1", port=2000):
    try:
        client = Client(host, port)
        client.set_timeout(2.0)
        world = client.get_world()
        for actor in world.get_actors():
            if EActorType.VEHICLE.value in actor.type_id:
                return actor.id
        raise
    except RuntimeError:
        print(f"[ERROR] Failed to connect to CARLA world ${host}:${port}.")
        exit()


if __name__ == "__main__":
    # change_world()
    api = Api(get_a_hero())
    sleep(10)
    del api
