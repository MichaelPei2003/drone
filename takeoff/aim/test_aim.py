from dronekit import connect
from arm_and_takeoff import arm_and_takeoff
from aim import aim

vehicle = connect("192.168.159.182:14550", wait_ready=False) 

#initialize PID parameter
ix = 0
iy = 0
last_error_x = 0
last_error_y = 0
flag_to_release = 0
flag_aimed = 1 #avoid getting 0 value
flag_aimed_ready = 0 #if already aimed

for i in range(400):
    bucket_x = i
    bucket_y = i / 640 * 480
    arm_and_takeoff(3, vehicle) #arm_and_takeoff(aTargetAltitude, vehicle)
    ix, iy, last_error_x, last_error_y, flag_aimed_ready = aim(bucket_x, bucket_y, ix, iy, last_error_x, last_error_y, vehicle)
