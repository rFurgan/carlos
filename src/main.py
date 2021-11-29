from api import API
from time import sleep


def main():
    api = API()
    api.start_polling_coordinates()
    sleep(5)
    api.stop_polling_coordinates()
    for actor in api.get_actors():
        print(actor.get_data())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
