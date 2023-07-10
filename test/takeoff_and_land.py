from dronekit import connect, VehicleMode
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from takeoff.arm_and_takeoff import arm_and_takeoff
import time

#connect to drone 
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

arm_and_takeoff(1, vehicle) #arm_and_takeoff(aTargetAltitude, vehicle)

for i in range(5):
    print(vehicle.mode)
    time.sleep(1)

if(vehicle.mode == "STABILIZE"):
    print("Manually taken over, exit program...")
    exit(0)

vehicle.mode = VehicleMode("LAND")

while True:
    print(vehicle.mode)
    print(vehicle.location.global_relative_frame.alt)

#Requires manual exit
