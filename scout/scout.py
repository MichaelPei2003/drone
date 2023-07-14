import time 
from dronekit import connect,VehicleMode

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from takeoff.send_body_ned_velocity import send_body_ned_velocity
# from send_body_ned_velocity import send_body_ned_velocity
from index import set_value


def scout(v_x,v_y,vehicle=None):
    send_body_ned_velocity(v_x/2,v_y/2,1,vehicle)
    break_time=time.time()
    set_value(1,break_time)