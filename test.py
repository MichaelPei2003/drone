from alt_hold import alt_hold
from get_target_location import get_target_location
from dronekit import connect, VehicleMode
import time
vehicle = connect("/dev/ttyACM0", wait_ready = True)

vehicle.armed = True
vehicle.mode = VehicleMode("GUIDED")

location1 = get_target_location(0, 30, vehicle)

vehicle.simple_takeoff(5)
time.sleep(5)

#vehicle.simple_goto(location1, airspeed = 1)

#time.sleep(60)

location = get_target_location(-11, 20, vehicle)

vehicle.simple_goto(location, airspeed = 1)
