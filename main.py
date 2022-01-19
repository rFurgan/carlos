from api import Api
from time import sleep

if __name__ == "__main__":
    a = Api()
    a.start(24)
    sleep(5)
    del a
