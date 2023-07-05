import time 
from dronekit import connect, VehicleMode, LocationGlobalRelative 

from send_body_ned_velocity import send_body_ned_velocity
from scout import scout
from get_and_send_position import get_and_send_position
from index import set_value
from index import get_value

from pymavlink import mavutil 
 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyACM0' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

set_value(8,vehicle)

cyl = 0    #是否检测到圆筒，初始值为0指未检测到

#路线2
#←↑→↑←↑→

start_time = time.time()
set_value(3,start_time)
duration = 7    #运动的持续时间
v_x = 0    #飞机在前后方向上的速度，前为正
v_y = -1    #飞机在左右方向上的速度，右为正
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
if cyl == 1 :    #检测到圆筒
    loc = get_value(7)
    scout(loc)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 1
v_x = 1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 7
v_x = 0
v_y = 1
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
if cyl == 1 :
    loc = get_value(7)
    scout(loc)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 1
v_x = 1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 7
v_x = 0
v_y = -1
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
if cyl == 1 :
    loc = get_value(7)
    scout(loc)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 1
v_x = 1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 7
v_x = 0
v_y = 1
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
if cyl == 1 :
    loc = get_value(7)
    scout(loc)
time.sleep(5)


