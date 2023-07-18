from pymavlink import mavutil
from dronekit import connect
from arm_and_takeoff import arm_and_takeoff
from send_body_ned_velocity import send_body_ned_velocity

vehicle = connect("/dev/ttyACM0", wait_ready = True)

arm_and_takeoff(3, vehicle)

while True:
    send_body_ned_velocity(0.8, 0, 0, vehicle)