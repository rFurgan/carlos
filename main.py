from time import sleep
from api import Api

if __name__ == "__main__":
    api = Api()
    api.start(36)
    api.subscribe(lambda data: print(f"ID:{data.id}\nTimestamp: {data.timestamp}\nPosition: {data.position}\n----------------"))
    sleep(5)
    del api
