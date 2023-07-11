from send_body_ned_velocity import send_body_ned_velocity
from send_body_angle import send_body_angle
from dronekit import connect
from arm_and_takeoff import arm_and_takeoff
#connect to drone 
connection_string ='192.168.130.182:14550' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

arm_and_takeoff(2,vehicle)
send_body_angle(60,vehicle)