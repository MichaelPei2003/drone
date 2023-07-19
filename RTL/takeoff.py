from dronekit import connect, VehicleMode
from get_target_location import get_target_location
import time
from pymavlink import mavutil

def takeoff(vehicle):
    vehicle = connect("/dev/ttyACM0", wait_ready = True)

    default_heading = vehicle.heading

    print("current location: lat: ", vehicle.location.global_frame.lat, "lon: ", vehicle.location.global_frame.lon)

    target_location = get_target_location(0, 30, vehicle)

    print("Arming motors...")
    vehicle.mode = VehicleMode("GUIDED")
    print("Vehicle mode: GUIDED")
    vehicle.armed = True
    print("Vehicle armed")

    #if not armed do following loop
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")

    print("Taking off")
    vehicle.simple_takeoff(3)
    time.sleep(2)

    print("Going to right, 2m")

    print("target location:", target_location.lat, ", ", target_location.lon, ", ", target_location.alt)

    vehicle.simple_goto(target_location, airspeed = 1.5)
    time.sleep(30)

    print(vehicle.heading)

    print("turning back")

    vehicle.message_factory.command_long_send(
    0, 0,  # target_system, target_component
    mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
    0,  # confirmation
    default_heading,  # param1 (目标偏航角)
    0, 0, 0, 0, 0,0  # param2, param3, param4, param5, param6
    )
