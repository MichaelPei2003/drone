
from pymavlink import mavutil
import time
def send_body_angle(angle,duration=0,vehicle = None):
    if vehicle == None:
        print("Vehicle info unknown, please take over controls.")
    # 设置目标位置，向左转90度
    target_yaw = vehicle.heading + angle  # 目标偏航角为当前偏航角加输入的角度

    # 发送控制指令
    msg = vehicle.message_factory.command_long_encode(
    0, 0,  # target_system, target_component
    mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
    0,  # confirmation
    target_yaw,  # param1 (目标偏航角)
    0, 0, 0, 0, 0,0  # param2, param3, param4, param5, param6
    )
    for x in range(0,duration):

        vehicle.send_mavlink(msg)

        time.sleep(1)
