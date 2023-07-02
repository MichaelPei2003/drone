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


#路线1
#↑←↓←↑←↓←↑←↓←↑

start_time = time.time()
set_value(3,start_time)
duration = 4
v_x = 1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 1
v_x = 0
v_y = -1
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = -1
v_x = -1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 1
v_x = 0
v_y = -1
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 4
v_x = 1
v_y = 0
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 1
v_x = 0
v_y = -1
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 4
v_x = -1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 1
v_x = 0
v_y = -1
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 4
v_x = 1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 1
v_x = 0
v_y = -1
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 4
v_x = -1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 1
v_x = 0
v_y = -1
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)

start_time = time.time()
set_value(3,start_time)
duration = 4
v_x = 1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
send_body_ned_velocity(v_x,v_y,0,duration)
time.sleep(5)


