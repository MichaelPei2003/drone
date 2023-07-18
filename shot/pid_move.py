from send_body_ned_velocity import send_body_ned_velocity 
def pid_move(vehicle,target_location_x,target_location_y,integral_x,integral_y,last_error_x,last_error_y,count_in_circle_now):
    k=0.001 #控制vx和vy
    # 初始化PID控制器
    dt=0.05
    kp = 1.5  # 比例参数
    ki = 0.5  # 积分参数
    kd = 0.03  # 微分参数

    max_vx=0.4 #前后方向最大速度
    max_vy=0.4 #左右方向最大速度
    error_x = 0 
    error_y = 0
    proportional_x=0
    proportional_y=0
    derivative_x=0
    derivative_y=0

    allow_error_x=30
    allow_error_y=30

    max_vx=0.4 #前后方向最大速度
    max_vy=0.4 #左右方向最大速度
   
    #判断是否投弹部分的参数
    count_in_circle = 40
    flag_allowshot=0

    # 获取当前位置
    current_location_x=320
    current_location_y=240

    # 计算误差
    error_x = target_location_x - current_location_x
    error_y = -(target_location_y - current_location_y)

    # 计算PID控制信号
    proportional_x = error_x
    proportional_y = error_y
    integral_x += error_x * dt
    integral_y += error_y * dt
    derivative_x = (error_x - last_error_x) / dt
    derivative_y = (error_y - last_error_y) / dt
    last_error_x = error_x
    last_error_y = error_y

    vx = kp * proportional_x + ki * integral_x + kd * derivative_x
    vy = kp * proportional_y + ki * integral_y + kd * derivative_y
    velocity_vx=k*vy*0.4
    velocity_vy=0.5*k*vx
    if velocity_vx>max_vx:
        velocity_vx=max_vx
        integral_y=0
    if velocity_vy>max_vy:
        velocity_vy=max_vy
        integral_x=0
    print("x:",velocity_vx,"y:",velocity_vy,"alt:",vehicle.location.global_relative_frame.alt)
    # 发送控制信号
    if vehicle.location.global_relative_frame.alt>3.5:
        send_body_ned_velocity(velocity_vx, velocity_vy, 0.1,vehicle)
    else:
        send_body_ned_velocity(velocity_vx, velocity_vy, 0,vehicle)
        

    # 检查是否到达目标点
    if abs(error_x) < allow_error_x and abs(error_y) < allow_error_y:
        count_in_circle_now = count_in_circle_now + 1
        if count_in_circle_now >= count_in_circle:
            print("Reached target location")
            flag_allowshot=1
        if vehicle.location.global_relative_frame.alt>=1:
            send_body_ned_velocity(0,0,0.3,vehicle)
            allow_error_x=allow_error_x+5
            allow_erroe_y=allow_error_y+5
    else:
        count_in_circle_now=0
    return integral_x,integral_y,last_error_x,last_error_y,count_in_circle_now,flag_allowshot