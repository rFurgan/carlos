from API import API
import time


def main():
    api = API()
    api.startPollingCoordinates()
    time.sleep(5)
    api.stopPollingCoordinates()
    for actor in api.getRelevantActors():
        print(actor)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
