import time 
from dronekit import connect,VehicleMode

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from takeoff.send_body_ned_velocity import send_body_ned_velocity
# from send_body_ned_velocity import send_body_ned_velocity


def scout(v_x,v_y):
    send_body_ned_velocity(v_x/2,v_y/2,1,vehicle=None)
    break_time=time.time()
    return  break_time