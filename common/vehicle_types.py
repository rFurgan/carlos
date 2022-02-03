from .enums import EVehicleType


class VehicleTypes:
    types = {
        EVehicleType.CAR: [
            "audi.a2",
            "audi.etron",
            "audi.tt",
            "bmw.grandtourer",
            "chevrolet.impala",
            "citroen.c3",
            "dodge.charger_2020",
            "dodge.charger_police",
            "dodge.charger_police_2020",
            "ford.crown",
            "ford.mustang",
            "jeep.wrangler_rubicon",
            "lincoln.mkz_2017",
            "lincoln.mkz_2020",
            "mercedes.coupe",
            "mercedes.coupe_2020",
            "mercedes.sprinter",
            "micro.microlino",
            "mini.cooper_s",
            "mini.cooper_s_2021",
            "nissan.micra",
            "nissan.patrol",
            "nissan.patrol_2021",
            "seat.leon",
            "tesla.cybertruck",
            "tesla.model3",
            "toyota.prius",
            "volkswagen.t2",
            "volkswagen.t2_2021",
        ],
        EVehicleType.BIKE: [
            "bh.crossbike",
            "diamondback.century",
            "gazelle.omafiets",
        ],
        EVehicleType.MOTORCYCLE: [
            "harley-davidson.low_rider",
            "kawasaki.ninja",
            "vespa.zx125",
            "yamaha.yzf",
        ],
        EVehicleType.TRUCK: [
            "carlamotors.carlacola",
            "carlamotors.firetruck",
            "ford.ambulance",
        ],
    }