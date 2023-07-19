from shotH import shot
from dronekit import connect, VehicleMode
from arm_and_takeoff import arm_and_takeoff
import time
from send_body_ned_velocity import send_body_ned_velocity

#connect to drone 
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect (connection_string, wait_ready=True) 


shot(vehicle)

print("已完成投弹，执行下一步侦查指令...")

