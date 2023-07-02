from arm_and_takeoff import arm_and_takeoff
from to_release_area import to_release_area
from connect import init

#connect to drone 
vehicle = init()

arm_and_takeoff(1, vehicle) #arm_and_takeoff(aTargetAltitude, vehicle)

to_release_area(vehicle) #fly straight forward at 0.8m/s for 38sec
