from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time

# 改为当前连接的pixhawk飞控的端口 
connection_string ='/dev/ttyACM0' 
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

msg = vehicle.message_factory.command_long_encode(
    RTL_ALT = 0,#返航高度，0时以当前高度
    RTL_ALT_FINAL = 220,#以厘米为单位，即返回高度为1米
    RTL_LOIT_TIME = 60000#悬停10秒
)
vehicle.send_mavlink(msg)#发送指令

time.sleep(30)