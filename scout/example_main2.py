import time 
from dronekit import connect

from send_body_ned_velocity import send_body_ned_velocity
from send_body_angle import send_body_angle

 
# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyACM0' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

#路线：↑←↓←↑←↓

#向前运动4m
send_body_ned_velocity(1,0,0,4,vehicle)
time.sleep(5)

#向左旋转90度
send_body_angle(-90,vehicle)

#向前运动2m
send_body_ned_velocity(1,0,0,2,vehicle)
time.sleep(5)

#向左旋转90度
send_body_angle(-90,vehicle)

#向前运动4m
send_body_ned_velocity(1,0,0,4,vehicle)
time.sleep(5)

#向右旋转90度
send_body_angle(90,vehicle)

#向前运动2米
send_body_ned_velocity(1,0,0,2,vehicle)
time.sleep(5)

#向右旋转90度
send_body_angle(90,vehicle)

#向前运动4m
send_body_ned_velocity(1,0,0,4,vehicle)
time.sleep(5)

#向左旋转90度
send_body_angle(-90,vehicle)

#向前运动2m
send_body_ned_velocity(1,0,0,2,vehicle)
time.sleep(5)

#向左旋转90度
send_body_angle(-90,vehicle)

#向前运动4m
send_body_ned_velocity(1,0,0,4,vehicle)
time.sleep(5)

#向右旋转90度
send_body_angle(90,vehicle)

#向前运动2米
send_body_ned_velocity(1,0,0,2,vehicle)
time.sleep(5)

#向右旋转90度
send_body_angle(90,vehicle)

#向前运动4m
send_body_ned_velocity(1,0,0,4,vehicle)
time.sleep(5)