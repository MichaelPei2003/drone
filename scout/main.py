from transfer_scout import transfer
import time 
from dronekit import connect,VehicleMode

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from takeoff.arm_and_takeoff import arm_and_takeoff

from threading import Thread

from send_body_ned_velocity import send_body_ned_velocity

# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyACM0' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=True) 

daemon_thread = Thread(target=transfer)
daemon_thread.daemon = True  # 设置线程为守护线程

# 启动守护线程
daemon_thread.start()

arm_and_takeoff(5,vehicle)

send_body_ned_velocity(0.4,0,0,10,vehicle)
time.sleep(5)
print("first path")

send_body_ned_velocity(-0.4,-0.3,0,10,vehicle)
time.sleep(5)
print("second path")

send_body_ned_velocity(0.4,0,0,10,vehicle)
time.sleep(5)
print("third path")

send_body_ned_velocity(-0.4,-0.3,0,10,vehicle)
time.sleep(5)
print("forth path")

send_body_ned_velocity(0.4,0,0,10,vehicle)
time.sleep(5)
print("fifth path")

send_body_ned_velocity(-0.2,-0.3,0,20,vehicle)
time.sleep(5)
print("sixth path")

# send_body_ned_velocity(-1,0.75,0,4,vehicle)
# time.sleep(5)
# print("sixth path")

# send_body_ned_velocity(0,1,0,0,3,vehicle)
# time.sleep(5)
# print("seventh path")

# send_body_ned_velocity(1,0.75,0,4,vehicle)
# time.sleep(5)
# print("eighth path")

# send_body_ned_velocity(0,-1,0,3,vehicle)
# time.sleep(5)
# print("nineth path")

print("end scouting .")

vehicle.mode = VehicleMode("RTL")