import time 
from dronekit import connect, VehicleMode, LocationGlobalRelative 

from send_body_ned_velocity import send_body_ned_velocity
from scout import scout

from pymavlink import mavutil 
 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyACM0' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 


cyl = 0    #是否检测到圆筒，初始值为0指未检测到

#路线2
#←↑→↑←↑→

start_time = time.time()
duration = 7    #运动的持续时间
v_x = 0    #飞机在前后方向上的速度，前为正
v_y = -1    #飞机在左右方向上的速度，右为正
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
if cyl == 1 :    #检测到圆筒
    scout(v_x,v_y,duration,start_time,vehicle)
time.sleep(5)

start_time = time.time()
duration = 1
v_x = 1
v_y = 0
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
time.sleep(5)

start_time = time.time()
duration = 7
v_x = 0
v_y = 1
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
if cyl == 1 :
    scout(v_x,v_y,duration,start_time,vehicle)
time.sleep(5)



