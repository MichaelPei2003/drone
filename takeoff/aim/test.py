from dronekit import connect, VehicleMode
from send_body_ned_velocity import send_body_ned_velocity
from arm_and_takeoff import arm_and_takeoff

vehicle = connect("192.168.159.182:14550", wait_ready = False)

#arm_and_takeoff(2, vehicle)

vehicle.mode = VehicleMode("GUIDED")

while True:
    send_body_ned_velocity(-1, 0, 0, vehicle)
