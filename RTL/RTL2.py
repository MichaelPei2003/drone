from ast import Delete
from pickle import TRUE
from re import L
from ssl import VERIFY_X509_PARTIAL_CHAIN
import time
from winreg import DeleteKeyEx 
from dronekit import connect, VehicleMode, LocationGlobalRelative 

from pymavlink import mavutil 
msg = vehicle.message_factory.command_long_encode(
    RTL_ALT = 0;#返航高度，0时以当前高度
    RTL_ALT_FINAL = 220;#以厘米为单位，即返回高度为1米
    RTL_LOIT_TIME = 60000;#悬停10秒
)
vehicle.send_mavlink(msg)#发送指令

time.sleep(1)
#读取H的xy坐标
Lx=str.split(',',2)[0]
Ly=str.split(',',2)[1]
while True:
    if Lx<=42
        addx=42-Lx
        send_body_ned_velocity(addx*0.01,0,0,0)
        time.sleep(1)
    elif Lx>=98
        delx=Lx-98
        send_body_ned_velocity(delx*-0.01,0,0,0)
        time.sleep(1)
    if Ly<=25
        addy=25-Ly
        send_body_ned_velocity(0,addy*0.01,0,0)
        time.sleep(1)
    elif Ly>=81
        dely=Ly-98
        send_body_ned_velocity(0,dely*-0.01,0,0)
        time.sleep(1)
    if (Lx<98&Lx>42&Ly<81&Ly>25)
        vehicle.mode = VehicleMode("LAND")
        break

     
    