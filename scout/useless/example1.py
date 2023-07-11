from threading import Thread
import time 
from dronekit import connect, VehicleMode, LocationGlobalRelative 

from send_body_ned_velocity import send_body_ned_velocity
from scout.useless import scout
from scout.useless.get_and_send_position import get_and_send_position
from scout.useless.index import set_value
from scout.useless.index import get_value

from pymavlink import mavutil 
 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyACM0' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

loc = vehicle.location.global_relative_frame
set_value(7,loc)

position_thread = Thread(target = get_and_send_position(vehicle))
position_thread.daemon = True
position_thread.start()

cir_num=0
cir=[]
cyl=0    #是否检测到圆筒，初始值为0指未检测到
set_value(6,cyl)

flag=0
start_time=time.time()
set_value(3,start_time)

#路线：↑←↓→↖←↑→
while flag != 1:
    duration=4
    set_value(2,duration)
    v_x=1
    v_y=0
    set_value(4,v_x)
    set_value(5,v_y)
    send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
    if cyl == 1 :
        scout(loc)
    time.sleep(10)

    start_time=time.time()
    set_value(3,start_time)
    duration=7
    set_value(2,duration)
    v_x = 0
    v_y = -1
    set_value(4,v_x)
    set_value(5,v_y)
    send_body_ned_velocity(0,-1,0,duration,vehicle)
    if cyl == 1 :
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    set_value(3,start_time)
    duration=4
    set_value(2,duration)
    v_x = -1
    v_y = 0
    set_value(4,v_x)
    set_value(5,v_y)
    vehicle.send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
    if cyl == 1 :
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    set_value(3,start_time)
    duration = 7
    set_value(2,duration)
    v_x = 0
    v_y = 1
    set_value(4,v_x)
    set_value(5,v_y)
    send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
    if cyl == 1 :
        scout(loc)
    time.sleep(10)
    
    start_time = time.time()
    set_value(3,start_time)
    duration = 1
    set_value(2,duration)
    v_x = 1
    v_y = 1
    set_value(4,v_x)
    set_value(5,v_y)
    send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
    if cyl == 1 :
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    set_value(3,start_time)
    duration = 5
    set_value(2,duration)
    v_x = 0
    v_y = -1
    set_value(4,v_x)
    set_value(5,v_y)
    send_body_ned_velocity(v_x,v_y,0,duration,vehicle)
    if cyl == 1 :
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    set_value(3,start_time)
    duration = 1
    set_value(2,duration)
    v_x = 1
    v_y = 0
    set_value(4,v_x)
    set_value(5,v_y)
    send_body_ned_velocity(v_x, v_y, 0, duration,vehicle)
    if cyl == 1 :
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    set_value(3,start_time)
    duration = 5
    set_value(2,duration)
    v_x = 0
    v_y = 1
    set_value(4,v_x)
    set_value(5,v_y)
    send_body_ned_velocity(v_x, v_y, 0, duration,vehicle)
    if cyl == 1 :
        scout(loc)
    time.sleep(10)
    
    flag=1

send_body_ned_velocity(5,2,0,4)
time.sleep(10)


