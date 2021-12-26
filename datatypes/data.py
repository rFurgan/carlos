from typing import NamedTuple
from datatypes.actor_type import EActorType
from datatypes.geoposition import Geoposition


class Data(NamedTuple):
    id: int
    type: EActorType
    position: Geoposition
    orientation: int
    velocity: int
    distanceToHero: float
    angleToHero: int