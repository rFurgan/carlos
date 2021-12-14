from api import Api
from time import sleep
from json import loads, dumps


def main():
    api = Api()
    api.start()
    sleep(3)
    api.stop()
    # data = api.get_data(10)  # Get all data of actor 10
    # data = api.get_recent_data(10)  # Get most recent data of actor 10
    data = api.get_data()  # Get all data of all actors
    # data = api.get_recent_data()  # Get most recent data of all actors
    print(dumps(loads(data), indent=4))
    del api


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
