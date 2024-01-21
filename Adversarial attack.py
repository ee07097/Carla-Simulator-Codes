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
import math
import random 
import time 
import numpy as np
import cv2
import matplotlib.pyplot as plt


# Connecting to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0) 

# We choose a blueprint for pedestrian
world = client.get_world()
blueprint_library = world.get_blueprint_library()
walker_bp = blueprint_library.filter('walker.pedestrian.0001')[0]



# Creating vehicles
vehicle_bp = bp_lib.find('vehicle.audi.a2') 
vehicle = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))
vehicle.set_autopilot(True)

# Move camera behind vehicle
spectator = world.get_spectator() 
transform = carla.Transform(vehicle.get_transform().transform(carla.Location(x=-4,z=2.5)),vehicle.get_transform().rotation) 
spectator.set_transform(transform)



# Find desired camera position
camera_bp = bp_lib.find('sensor.camera.rgb') 
camera_init_trans = carla.Transform(carla.Location(z=2)) 
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)
time.sleep(0.2) # Αλλαγής κάμερας
spectator.set_transform(camera.get_transform())
camera.destroy()



# Playback camera
camera_init_trans = carla.Transform(carla.Location(z=2))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)


# The callback stores the sensor data for reuse
def camera_callback(image, data_dict):
# Convert image to numpy array
img = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4)
# Add Gaussian noise
mean = 0
var = 0.5
sigma = var**0.5
gauss = np.random.normal(mean,sigma,(image.height, image.width, 4))
gauss = gauss.reshape(image.height, image.width, 4)
img = img + gauss



# Save a noisy image
data_dict['image'] = img
filename = f"captured_images/{time.time()}.png"
# Get camera dimensions                     
image_w = camera_bp.get_attribute("image_size_x").as_int()
image_h = camera_bp.get_attribute("image_size_y").as_int()
camera_data = {'image': np.zeros((image_h, image_w, 4))}
# Start recording
camera.listen(lambda image: camera_callback(image, camera_data))
# window OpenCV
cv2.namedWindow('RGB Camera', cv2.WINDOW_AUTOSIZE)
cv2.imshow('RGB Camera', camera_data['image'])
cv2.waitKey(1)

# Game loop
while True:
# save image
cv2.imwrite(filename, camera_data['image'])
# Get the current control of the autopilot
control = vehicle.get_control()
# Adding noise to control
control.throttle += np.random.normal(0, 0.1)
control.steer += np.random.normal(0, 0.1)
# Application of noise in the vehicle
vehicle.apply_control(control)
# Imshow renders sensor data to display
cv2.imshow('RGB Camera', camera_data['image'])


  

# Exit if user types 'q'
if cv2.waitKey(1) == ord('q'):
break
# exit OpenCV 
cv2.destroyAllWindows()
cv2.stop()
