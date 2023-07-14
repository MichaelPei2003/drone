import time 
from dronekit import connect,VehicleMode

import sys, os
from send_body_ned_velocity import send_body_ned_velocity


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from takeoff.arm_and_takeoff import arm_and_takeoff


# 改为当前连接的pixhawk飞控的端口 
connection_string ='192.168.159.182:14550' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

arm_and_takeoff(5,vehicle)

#路线：↑←↓←↑←↓

#向前走4m
send_body_ned_velocity(1,0,0,4)
time.sleep(5)
print("go forward 4m")

#向左走2m
send_body_ned_velocity(0,-1,0,2)
time.sleep(3)
print("go left 2m")

#向后走4m
send_body_ned_velocity(-1,0,0,4)
time.sleep(5)
print("go backward 4m")

#向左走2m
send_body_ned_velocity(0,-1,0,2)
time.sleep(3)
print("go left 2m")

#向前走4m
send_body_ned_velocity(1,0,0,4)
time.sleep(5)
print("go forward 4m")

#向左走2m
send_body_ned_velocity(0,-1,0,2)
time.sleep(3)
print("go left 2m")

#向后走4m
send_body_ned_velocity(-1,0,0,4)
time.sleep(5)
print("go backward 4m")

#重新换个方向走一遍

#向前走4m
send_body_ned_velocity(1,0,0,4)
time.sleep(5)
print("go forward 4m")

#向右走2m
send_body_ned_velocity(0,1,0,2)
time.sleep(3)
print("go left 2m")

#向后走4m
send_body_ned_velocity(-1,0,0,4)
time.sleep(5)
print("go backward 4m")

#向右走2m
send_body_ned_velocity(0,1,0,2)
time.sleep(3)
print("go left 2m")

#向前走4m
send_body_ned_velocity(1,0,0,4)
time.sleep(5)
print("go forward 4m")

#向右走2m
send_body_ned_velocity(0,1,0,2)
time.sleep(3)
print("go left 2m")

#向后走4m
send_body_ned_velocity(-1,0,0,4)
time.sleep(5)
print("go backward 4m")




# #向前运动4m
# send_body_ned_velocity(1,0,0,4,vehicle)
# time.sleep(5)
# print("4m overed")

# #向左旋转90度
# send_body_angle(-90,vehicle)
# time.sleep(3)
# print("turn left 90 degree overed")

# #向前运动2m
# send_body_ned_velocity(1,0,0,2,vehicle)
# time.sleep(5)
# print("2m overed")

# #向左旋转90度
# send_body_angle(-90,vehicle)
# time.sleep(3)
# print("turn left 90 degree overed")

# #向前运动4m
# send_body_ned_velocity(1,0,0,4,vehicle)
# time.sleep(5)
# print("4m overed")

# #向右旋转90度
# send_body_angle(90,vehicle)
# time.sleep(3)
# print("turn right 90 degree overed")

# #向前运动2米
# send_body_ned_velocity(1,0,0,2,vehicle)
# time.sleep(5)
# print("2m overed")

# #向右旋转90度
# send_body_angle(90,vehicle)
# time.sleep(3)
# print("turn right 90 degree")

# #向前运动4m
# send_body_ned_velocity(1,0,0,4,vehicle)
# time.sleep(5)
# print("4m overed")

# #向左旋转90度
# send_body_angle(-90,vehicle)
# time.sleep(3)
# print("turn left 90 degree overed")

# #向前运动2m
# send_body_ned_velocity(1,0,0,2,vehicle)
# time.sleep(5)
# print("2m overed")

# #向左旋转90度
# send_body_angle(-90,vehicle)
# time.sleep(3)
# print("turn left 90 degree")

# #向前运动4m
# send_body_ned_velocity(1,0,0,4,vehicle)
# time.sleep(5)
# print("4m overed")

# #向右旋转90度
# send_body_angle(90,vehicle)
# time.sleep(3)
# print("turn right 90 degree overed")

# #向前运动2米
# send_body_ned_velocity(1,0,0,2,vehicle)
# time.sleep(5)
# print("2m overed")

# #向右旋转90度
# send_body_angle(90,vehicle)
# time.sleep(3)
# print("turn right 90 degree overed")

# #向前运动4m
# send_body_ned_velocity(1,0,0,4,vehicle)
# time.sleep(5)
# print("4m overed")

vehicle.mode = VehicleMode("RTL")
