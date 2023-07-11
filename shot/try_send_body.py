from send_body_ned_velocity import send_body_ned_velocity
from shot import shot
from dronekit import connect
from arm_and_takeoff import arm_and_takeoff
#connect to drone 
connection_string ='192.168.159.182:14550' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

arm_and_takeoff(2,vehicle)
while True:
    send_body_ned_velocity(-1,0,0,vehicle)
