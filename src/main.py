from api import API
import time


def main():
    api = API()
    api.start_polling_coordinates()
    time.sleep(5)
    api.stop_polling_coordinates()
    for actor in api.get_relevant_actors():
        print(actor.get_data())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
