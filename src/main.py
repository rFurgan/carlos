from api import Api
from time import sleep


def main():
    api = Api()
    api.start()
    sleep(1.2)
    api.stop()
    print(api.get_data())
    del api


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
