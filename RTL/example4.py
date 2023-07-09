import time 
from dronekit import connect, VehicleMode, LocationGlobalRelative 

from command_long_send import simple_gomin
from scout import scout
from scout.useless.get_and_send_position import get_and_send_position
from scout.useless.index import set_value
from scout.useless.index import get_value

from pymavlink import mavutil 
 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyACM0' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 


start_time = time.time()
set_value(3,start_time)
duration = 4
v_x = 1
v_y = 0
set_value(2,duration)
set_value(4,v_x)
set_value(5,v_y)
simple_gomin(v_x,v_y,0,vehicle)
time.sleep(5)