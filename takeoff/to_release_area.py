import time 
from send_body_ned_velocity import send_body_ned_velocity

def to_release_area(vehicle):
    #30m
    flag1 = 0 #if bucket detected
    flag2 = 0 #double check if bucket detected
    for i in range(15):
        send_body_ned_velocity(0.8, 0, 0, vehicle)
        #leave takeoff area
    #need a lag
    send_body_ned_velocity(0.8, 0, 0, vehicle)
    print("going forward...")
    #won't auto stop if nothing detected
