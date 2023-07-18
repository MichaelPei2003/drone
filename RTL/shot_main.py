from shotH import shot
from dronekit import connect, VehicleMode
from arm_and_takeoff import arm_and_takeoff
import time
from send_body_ned_velocity import send_body_ned_velocity

#connect to drone 
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect (connection_string, wait_ready=True) 

arm_and_takeoff(2,vehicle)
send_body_ned_velocity(0.4,0,0,10,vehicle)
time.sleep(5)
vehicle.mode = VehicleMode("RTL")
time.sleep(2)
shot(vehicle)

print("已完成投弹，执行下一步侦查指令...")

