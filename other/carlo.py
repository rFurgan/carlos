#!/usr/bin/env python

"""
Imports etc.
"""
import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import random
import time

def main():
    actor_list = []

    try:
        client = carla.Client('127.0.0.1', 2000)
        client.set_timeout(2.0)

        world = client.get_world()

        # blueprints = world.get_blueprint_library().filter('vehicle.*')
        blueprints = world.get_blueprint_library().filter('walker.*')

        # bp = random.choice(blueprints.filter('vehicle'))
        bp = random.choice(blueprints.filter('walker'))
        ai = world.get_blueprint_library().find('controller.ai.walker')

        spawn_points = world.get_map().get_spawn_points()
        random.shuffle(spawn_points)
        transform = random.choice(spawn_points)
        ###
        transform.location.x = 26.382587
        transform.location.y = -57.401386
        transform.location.z = 5.600000
        ###
        print("Location to spawn: {}".format(transform.location))

        vehicle = world.spawn_actor(ai, transform, bp)
        # vehicle = world.spawn_actor(transform, bp)
        
        time.sleep(0.5)
        # print("Vehicle spawn to: {}".format(vehicle.get_location()))

        actor_list.append(vehicle)
        # print('created %s' % vehicle.type_id)

        print('spawned %d vehicles, press Ctrl+C to exit.' % len(actor_list))

        while True:
            world.wait_for_tick()
            time.sleep(0.1)

    finally:


        print('destroying actors')
        for actor in actor_list:
            actor.destroy()
        print('done.')


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
