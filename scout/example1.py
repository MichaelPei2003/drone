import time 
from dronekit import connect, VehicleMode, LocationGlobalRelative 

from pymavlink import mavutil 
 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyACM0' 


loc = vehicle.location.global_relative_frame

position_thread = Thread(target=get_and_send_position)
position_thread.daemon = True
position_thread.start()

cir_num=0
cir=[]

flag=0
start_time=time.time()
while flag != 1
    duration=4
    v_x=1
    v_y=0
    send_body_ned_velocity(v_x,v_y,0,duration)
    if  # 看到圆筒
        scout(loc)
    time.sleep(10)

    start_time=time.time()
    duration=7
    v_x = 0
    v_y = -1
    send_body_ned_velocity(0,-1,0,duration)
    if #看到圆筒
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    duration=4
    v_x = -1
    v_y = 0
    send_body_ned_velocity(v_x,v_y,0,duration)
    if  # 看到圆筒
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    duration = 7
    v_x = 0
    v_y = 1
    send_body_ned_velocity(v_x,v_y,0,duration)
    if  # 看到圆筒
        scout(loc)
    time.sleep(10)
    
    start_time = time.time()
    duration = 1
    v_x = 1
    v_y = 1
    send_body_ned_velocity(v_x,v_y,0,duration)
    if  # 看到圆筒
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    duration = 5
    v_x = 0
    v_y = -1
    send_body_ned_velocity(v_x,v_y,0,duration)
    if  # 看到圆筒
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    duration = 1
    v_x = 1
    v_y = 0
    send_body_ned_velocity(v_x, v_y, 0, duration)
    if  # 看到圆筒
        scout(loc)
    time.sleep(10)

    start_time = time.time()
    duration = 5
    v_x = 0
    v_y = 1
    send_body_ned_velocity(v_x, v_y, 0, duration)
    if  # 看到圆筒
        scout(loc)
    time.sleep(10)
    
    flag=1

send_body_ned_velocity(5,2,0,4)
time.sleep(10)


