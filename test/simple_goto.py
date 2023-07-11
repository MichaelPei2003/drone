from dronekit import connect, VehicleMode
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ..takeoff.arm_and_takeoff import arm_and_takeoff
import time

#connect to drone 
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

vehicle.simple_goto(vehicle.location.global_relative_frame.lat+0.00001, vehicle.location.global_relative_frame.lon+0.00001, 3)
