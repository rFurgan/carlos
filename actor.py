class Actor:
    def __init__(self, id, type, max_entry_count):
        self._data = [id, type]
        self._max_entry_count = max_entry_count
        self._velocity = []
        self._orientation = []
        self._angular_speed = []
        self._distance_to_hero = []
        self._angle_to_hero = []

    def add_data(
        self, velocity, orientation, angular_speed, distance_to_hero, angle_to_hero
    ):
        if len(self._velocity) >= self._max_entry_count:
            self._velocity.pop(0)
        self._velocity.append(velocity if velocity != None else "-")

        if len(self._orientation) >= self._max_entry_count:
            self._orientation.pop(0)
        self._orientation.append(orientation if orientation != None else "-")

        if len(self._angular_speed) >= self._max_entry_count:
            self._angular_speed.pop(0)
        self._angular_speed.append(angular_speed if angular_speed != None else "-")

        if len(self._distance_to_hero) >= self._max_entry_count:
            self._distance_to_hero.pop(0)
        self._distance_to_hero.append(
            distance_to_hero if distance_to_hero != None else "-"
        )

        if len(self._angle_to_hero) >= self._max_entry_count:
            self._angle_to_hero.pop(0)
        self._angle_to_hero.append(angle_to_hero if angle_to_hero != None else "-")

    def get_data(self):
        return (
            self._data
            + self._velocity
            + self._orientation
            + self._angular_speed
            + self._distance_to_hero
            + self._angle_to_hero
        )
