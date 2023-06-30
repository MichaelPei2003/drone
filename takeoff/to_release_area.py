import time 
from send_body_ned_velocity import send_body_ned_velocity

def to_release_area(vehicle):
    #30m
    flag1 = 0 #if bucket detected
    flag2 = 0 #double check if bucket detected
    for i in range(15):
        send_body_ned_velocity(0.8, 0, 0, 1, vehicle)
        #leave takeoff area
    for j in range(23):
        send_body_ned_velocity(0.8, 0, 0, 1, vehicle)
        print("going forward...")
        # flag1 = 
        if flag1 != 0:
            time.sleep(0.1)
            # flag2 = 
            # read detection outputs
            if flag2 != 0:
                break #release area reached
    if j == 22:
        print("计时结束时未检测到桶") 
