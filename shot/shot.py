                            #from multiprocessing import connection
import time
#from dronekit import LocationGlobal, VehicleMode
from send_body_ned_velocity import send_body_ned_velocity
import cv2
import numpy as np
import socket
import time
import pigpio
def shot(vehicle):
    # 初始化PID控制器
    dt = 0.1
    kp = 0.002  # 比例参数
    ki = 0.0001  # 积分参数
    kd = 0.0001  # 微分参数
    error_x = 0
    error_y = 0
    proportional_x=0
    proportional_y=0
    integral_x = 0
    integral_y = 0
    derivative_x=0
    derivative_y=0
    last_error_x = 0
    last_error_y = 0

    pi = pigpio.pi()

    servo_pin = 14
    servo_min = 1000  # 舵机最小脉冲宽度
    servo_max = 2000  # 舵机最大脉冲宽度
    servo_mid = (servo_max - servo_min) / 2 + servo_min
    pi.set_servo_pulsewidth(servo_pin, 0)  # 停止初始位置抖动
    pi.set_servo_pulsewidth(servo_pin, servo_min)  # 最小位置

    cap = cv2.VideoCapture(0)
    # 设置编码参数
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    # 创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    print("等待地面站连接...")
    client_socket, client_address = server_socket.accept()
    print("地面站连接成功")

    #client_socket.setblocking(False)
    interval = 0.1  # 设置轮询间隔

    run_servo = 0

    while True:
        # 读取一帧图像
        ret, frame = cap.read()

        # 编码图像
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)

        # 将图像转换成字符格式
        data = np.array(imgencode)
        stringData = data.tobytes()

        # 发送图像大小
        client_socket.send(str(len(stringData)).ljust(16).encode())

        # 发送图像数据
        client_socket.send(stringData)

        # 显示图像
        #   cv2.imshow('frame', frame)

        try:
         #接收数据
            coord = client_socket.recv(4096)
            coord_str = coord.decode("utf-8")
            if coord_str != '0':
                x, y, flag_servo = coord_str.split(",")
                print("(",x,",",y,")",flag_servo)
                target_location_x = int(x)#晚点再设置吧
                target_location_y = int(y)
                if int(flag_servo) == 1 and run_servo == 0 :
                    try:
                        pi.set_servo_pulsewidth(servo_pin, servo_max)  # 最大位置
                        time.sleep(1)
                        run_servo = 1
                    except:
                        pass

            else:
                print(0)
                continue
        except BlockingIOError:
        # 如果没有新的数据到达，则等待一段时间再次尝试接收
            time.sleep(interval)
        except BrokenPipeError:
            time.sleep(interval)
        except ConnectionResetError:
            time.sleep(interval)

    

        
        # 获取当前位置
        current_location_x=320
        current_location_y=240


        # 计算误差
        error_x = -(target_location_x - current_location_x)
        error_y = -(target_location_y - current_location_y)

        # 计算PID控制信号
        proportional_x = error_x
        proportional_y = error_y
        integral_x += error_x*dt
        integral_y += error_y*dt
        derivative_x = (error_x - last_error_x)/dt
        derivative_y = (error_y - last_error_y)/dt
        last_error_x = error_x
        last_error_y = error_y

        print("vx:",vx,"vy:",vy)
        vx = kp * proportional_x + ki * integral_x + kd * derivative_x
        vy = kp * proportional_y + ki * integral_y + kd * derivative_y

        # 发送控制信号
        send_body_ned_velocity(vy, vx, 0,vehicle)

        # 检查是否到达目标点
        if abs(error_x) < 2 and abs(error_y) < 2:
            print("Reached target location")
            break
