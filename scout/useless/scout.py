import time

from dronekit import connect, VehicleMode
from pymavlink import mavutil
from send_body_ned_velocity import send_body_ned_velocity
from scout.useless.control_flight import control_flight
from scout.index import set_value
from scout.index import get_value


def scout(v_x,v_y,duration,start_time,vehicle = None):
    #记录此刻的位置，并停住
    time.sleep(5)
    now_time=time.time()
    # now_loc=location
    
    #pid，运行到圆筒的正上方
    
    #此处放pid代码
    while True:
        # 省略了接收实时坐标部分代码，这里假设从视觉接收到的坐标为(0，0)
        x = 0
        y = 0

        # 控制飞行
        control_flight(x, y)
        if x <= 330 and x >= 310 :    #如果在xoy坐标系上的x坐标小于10
            break

        time.sleep(1)  # 此处为每秒执行一次循环，之后要根据摄像头帧率调整延时

    time.sleep(10)

    #下降到能看清圆筒内容的高度
    send_body_ned_velocity(0, 0, -1, 1)
    time.sleep(10)

    #回到原来的巡航路线上
    
    #依靠相对位置
    rest_time = duration-(now_time-start_time)    #计算按原来路径运动时剩余的时间
    send_body_ned_velocity(v_x,v_y,0,rest_time)    #继续按原来的路径运动
    now_time=time.time()
    cyl = get_value(6)
    if cyl == 1 :# 看到圆筒
        scout(v_x,v_y,rest_time,now_time)
