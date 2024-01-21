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
import weakref

# Connecting to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0) 

# We choose a blueprint for pedestrian
world = client.get_world()
blueprint_library = world.get_blueprint_library()
walker_bp = blueprint_library.filter('walker.pedestrian.0001')[0]



# create walkers
for _ in range(50):
 # create walker in random position
spawn_point = carla.Transform(carla.Location(x=random.uniform(-100, 100), y=random.uniform(-100, 100), z=1))
    walker = world.try_spawn_actor(walker_bp, spawn_point)
# If the build fails, we try again
   if walker is None:
        continue
    # We set a random desired speed and direction
   walker_control = carla.WalkerControl()
    walker_control.speed = random.uniform(4.0, 4.0)  # m/s
    walker_control.direction = carla.Vector3D(x=random.uniform(-1.0, 1.0), y=random.uniform(-1.0, 1.0), z=0.0)
    walker.apply_control(walker_control)
