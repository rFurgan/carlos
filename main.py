from api.carlos import Carlos
from time import sleep
from sys import argv


def main(argv):
    carlos = Carlos(argv)
    carlos.start()
    sleep(3)
    print(carlos.get_data())


if __name__ == "__main__":
    main(argv)
