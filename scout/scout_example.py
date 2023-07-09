import time 
from dronekit import connect, VehicleMode, LocationGlobalRelative 

from send_body_ned_velocity import send_body_ned_velocity
from loiter_turns import loiter_turns

from pymavlink import mavutil 
 
connection_string ='/dev/ttyACM0' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

location=vehicle.location.global_relative_frame
loiter_turns(vehicle,location)
