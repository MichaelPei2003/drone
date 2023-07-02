import time 
from dronekit import connect, VehicleMode, LocationGlobalRelative 

from send_body_ned_velocity import send_body_ned_velocity
from scout import scout

from pymavlink import mavutil 
 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyACM0' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 


#路线2
send_body_ned_velocity(0,-1,0,7)
time.sleep(5)

send_body_ned_velocity(1,0,0,1)
time.sleep(5)

send_body_ned_velocity(0,1,0,7)
time.sleep(5)

send_body_ned_velocity(1,0,0,1)
time.sleep(5)

send_body_ned_velocity(0,-1,0,7)
time.sleep(5)

send_body_ned_velocity(1,0,0,1)
time.sleep(5)

send_body_ned_velocity(0,1,0,7)
time.sleep(5)

send_body_ned_velocity(1,0,0,1)
time.sleep(5)
