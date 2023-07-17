from dronekit import connect, VehicleMode
from arm import arm
from get_target_location import get_target_location
import time
from pymavlink import mavutil

vehicle = connect("192.168.143.160:14550", wait_ready = False)

default_heading = vehicle.heading

print("current location: lat: ", vehicle.location.global_frame.lat, "lon: ", vehicle.location.global_frame.lon)

target_location = get_target_location(0, 30, vehicle)

arm(vehicle)

vehicle.mode = VehicleMode("GUIDED")

print("Taking off")
vehicle.simple_takeoff(3)
time.sleep(10)

print("Going to right, 2m")

print("target location:", target_location.lat, ", ", target_location.lon, ", ", target_location.alt)

vehicle.simple_goto(target_location, airspeed = 0.8)

time.sleep(38)

print(vehicle.heading)

print("turning back")

vehicle.message_factory.command_long_send(
0, 0,  # target_system, target_component
mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
0,  # confirmation
default_heading,  # param1 (目标偏航角)
0, 0, 0, 0, 0,0  # param2, param3, param4, param5, param6
)

time.sleep(10)

print("test ended, RTL")

vehicle.mode = VehicleMode("RTL")
