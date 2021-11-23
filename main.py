from API import API


def main():
    api = API()
    api.startPollingCoordinates()
    for actor in api.getRelevantActors():
        print(actor)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
