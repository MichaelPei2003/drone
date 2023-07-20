from index import set_value
import time 
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from send_body_ned_velocity import send_body_ned_velocity

def scout(vehicle):
    fscout=0
    set_value(0,fscout)
    send_body_ned_velocity(0.4,0,0,10,vehicle)
    time.sleep(5)
    print("first path")

    send_body_ned_velocity(-0.4,0.3,0,10,vehicle)
    time.sleep(5)
    print("second path")

    send_body_ned_velocity(0.4,0,0,10,vehicle)
    time.sleep(5)
    print("third path")

    send_body_ned_velocity(-0.4,0.3,0,10,vehicle)
    time.sleep(5)
    print("forth path")

    send_body_ned_velocity(0.4,0,0,10,vehicle)
    time.sleep(5)
    print("fifth path")

    send_body_ned_velocity(-0.2,-0.3,0,20,vehicle)
    time.sleep(5)
    print("sixth path")

    print("end scouting .")
    fscout=1
    set_value(0,fscout)
    '''定义一个全局变量'''
    
    
