from send_body_ned_velocity import send_body_ned_velocity
from dronekit import VehicleMode

def Pidshot(x,y,vehicle):
    # PID参数
    Kp = 1.0  # 比例系数
    Ki = 0.1  # 积分系数
    Kd = 0.01  # 微分系数
    target_X = 70  # 目标X轴坐标
    current_X = 0  # 当前X轴坐标
    target_Y = 53  # 目标Y轴坐标
    current_Y = 0  # 当前Y轴坐标
    error_priorX = 0  # 上一次误差
    integralX = 0  # 积分
    derivativeX = 0  # 微分
    error_priorY = 0  # 上一次误差
    integralY = 0  # 积分
    derivativeY = 0  # 微分
    current_X=x/640*140 # 测量当前X坐标
    current_Y=y/480*105 # 测量当前Y坐标
    if (current_X<=68 or current_X>=72):
        # 计算误差
        errorX = target_X - current_X
        # 计算积分
        integralX = integralX + errorX
        # 计算微分
        derivativeX = errorX - error_priorX
        # 计算控制量
        controlX = Kp * errorX + Ki * integralX + Kd * derivativeX
        # 更新上一次误差
        error_priorX = errorX
        # 应用控制量到无人机
        send_body_ned_velocity(0,controlX*0.1,0,vehicle)
        # 测量当前X坐标
        current_X=x/640*140 

    if (current_Y<=50 or current_Y>=55):
        # 计算误差
        errorY = target_Y - current_Y
        # 计算积分
        integralY = integralY + errorY
        # 计算微分
        derivativeY = errorY - error_priorY 
        # 计算控制量
        controlY = Kp * errorY + Ki * integralY + Kd * derivativeY
        # 更新上一次误差
        error_priorY = errorY
        # 应用控制量到无人机
        send_body_ned_velocity(controlY*0.1,0,0,vehicle)
        # 测量当前Y坐标
        current_Y=y/480*105    

    if (current_X>=68 and current_X<=72 and current_Y>=50 and current_Y<=55):
        #if reach the range of xy,change mode to "LAND"
        print("reach the range")
        vehicle.VehicleMode("LAND")
