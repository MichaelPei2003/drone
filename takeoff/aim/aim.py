from send_body_ned_velocity import send_body_ned_velocity

def aim(bucket_x, bucket_y, ix, iy, last_error_x, last_error_y, vehicle):
    flag = 0#flag aimed
    # PID
    dt = 0.1
    kp = 0.002  # 比例参数
    ki = 0.0002  # 积分参数
    kd = 0.002  # 微分参数
    
    self_x = 320
    self_y = 240
    
    error_y = bucket_x - self_x
    error_x = self_y - bucket_y

    px = error_x
    py = error_y
    ix += error_x * dt
    iy += error_y * dt
    dx = (error_x - last_error_x)/dt
    dy = (error_y - last_error_y)/dt
    last_error_x = error_x
    last_error_y = error_y
    vx = kp * px + ki * ix + kd * dx
    vy = kp * py + ki * iy + kd * dy
    
    if abs(error_x) >= 10:
        print("sending SPD: ", vx, ", 0")
        send_body_ned_velocity(vx, 0, 0, vehicle)
        return ix, 0, last_error_x, last_error_y, 0
    elif abs(error_y) >= 10:
        print("sending SPD: 0, ", vy)
        send_body_ned_velocity(0, vy, 0, vehicle)
        return 0, iy, last_error_x, last_error_y, 0
    elif abs(error_x) < 10 and abs(error_y) < 10:
        flag = 1
        
    return ix, iy, last_error_x, last_error_y, flag
