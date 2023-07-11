from dronekit import connect
from send_body_ned_velocity import send_body_ned_velocity
from arm_and_takeoff import arm_and_takeoff

import time

vehicle = connect('192.168.159.182:14550', wait_ready=False)

arm_and_takeoff(1, vehicle)

for x in range(5):
    send_body_ned_velocity(0, 1, 0, vehicle)
    time.sleep(1)
