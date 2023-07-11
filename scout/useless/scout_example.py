from dronekit import connect
from scout.useless.loiter_turns import loiter_turns
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from takeoff.arm_and_takeoff import arm_and_takeoff
 

connection_string ='192.168.31.85:14550' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

arm_and_takeoff(2,vehicle)

location=vehicle.location.global_relative_frame
loiter_turns(vehicle,location)


