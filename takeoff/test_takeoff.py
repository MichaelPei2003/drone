from dronekit import connect
from arm_and_takeoff import arm_and_takeoff
from to_release_area import to_release_area

#connect to drone 
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

arm_and_takeoff(1, vehicle) #arm_and_takeoff(aTargetAltitude, vehicle)

vehicle.mode = ("RTL")