from dronekit import connect, VehicleMode
import math
import time

connection_string = 'udp:127.0.0.1:14550'  
vehicle = connect(connection_string, wait_ready=False)

target_coordinate = (1, 1)  # 目标坐标，即应投弹时视觉检测出的圆筒中心坐标

Kp = 0.5  #比例环节，比例控制是基于偏差进行调节的，即有差调节
Ki = 0.1  #积分环节，能对误差进行记忆，主要用于消除静差，提高系统的无差度，积分作用的强弱取决于积分时间常数Ti，Ti越大，积分作用越弱，反之则越强。
Kd = 0.2  #微分环节，能反映偏差信号的变化趋势(变化速率)，并能在偏差信号值变得太大之前，在系统中引入一个有效的早期修正信号，从而加快系统的动作速度，减小调节时间。

# 初始化误差和积分误差
error_sum = 0
last_error = 0
error_tolerance=0.01 #定义误差允许范围0.01m

def control_flight(x, y):
    global error_sum, last_error

    adjustment_angle = 1  # 每次调整的偏航角角度

    # 计算坐标差异
    dx = x - target_coordinate[0]
    dy = y - target_coordinate[1]

    # 当目标点在当前点的左侧时，dx 为负值；当目标点在当前点的右侧时，dx 为正值
    # 当目标点在当前点的后方时，dy 为负值；当目标点在当前点的前方时，dy 为正值
    # math.atan2用于计算目标点相对于当前点的方向角，反正切函数 math.atan2() 的参数顺序是 (y, x)
    # math.degrees用于将弧度值转为角度
    # 最终计算出目标航向角
    target_yaw = math.degrees(math.atan2(dy, dx))

    # 计算相对于目标航向角的偏转角度
    relative_yaw = target_yaw - vehicle.heading

    # 计算PID控制器输出
    error = math.sqrt(dx ** 2 + dy ** 2)
    error_sum += error
    error_diff = error - last_error

    
    # 计算速度调整量，到达目标点即dx=dy=0时speed=0实现悬停，后续可以改成dx和dy在一定误差内就悬停
    if error < error_tolerance:
         speed=0
    else:
         speed = Kp * error + Ki * error_sum + Kd * error_diff

    # 更新上一次的误差
    last_error = error

    # 设置速度和目标航向角度
    vehicle.airspeed = abs(speed)

    # 调整飞行方向
    if relative_yaw > adjustment_angle:
        # 目标在右侧，向右偏转
        vehicle.simple_goto(vehicle.location.global_relative_frame, vehicle.heading + adjustment_angle)
    elif relative_yaw < -adjustment_angle:
        # 目标在左侧，向左偏转
        vehicle.simple_goto(vehicle.location.global_relative_frame, vehicle.heading - adjustment_angle)
    else:
        # 目标在正前方一定误差角内，直行
        vehicle.simple_goto(vehicle.location.global_relative_frame, vehicle.heading)
   

# 循环执行飞行控制
while True:
    # 省略了接收实时坐标部分代码，这里假设从视觉接收到的坐标为(0，0)
    x = 0
    y = 0

    # 控制飞行
    control_flight(x, y)

    time.sleep(1)  # 此处为每秒执行一次循环，之后要根据摄像头帧率调整延时


vehicle.close()
