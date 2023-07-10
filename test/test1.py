from dronekit import connect, VehicleMode
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ..takeoff.arm_and_takeoff import arm_and_takeoff
from ..scout.send_body_ned_velocity import send_body_ned_velocity
import time

#走一个 1x1 正方形后再下降1m，路线为：↑→↓←

#connect to drone 
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=True) 

arm_and_takeoff(2, vehicle) #arm_and_takeoff(aTargetAltitude, vehicle)

send_body_ned_velocity(1,0,0,1,vehicle)
print("Go forward 1m")
time.sleep(5)

send_body_ned_velocity(0,1,0,1,vehicle)
print("Go right 1m")
time.sleep(5)

send_body_ned_velocity(-1,0,0,1,vehicle)
print("Go back 1m")
time.sleep(5)

send_body_ned_velocity(0,-1,0,1,vehicle)
print("Go left 1m")
time.sleep(5)

send_body_ned_velocity(0,0,-1,1,vehicle)
print("Go down 1m")
time.sleep(5)


vehicle.mode=VehicleMode("LAND")
print(vehicle.mode)