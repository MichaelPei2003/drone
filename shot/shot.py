#from multiprocessing import connection
import time
#from dronekit import LocationGlobal, VehicleMode
from send_body_ned_velocity import send_body_ned_velocity
import cv2
import numpy as np
import socket
import time

def shot():
    # 初始化PID控制器
    dt = 0.1
    kp = 0.2  # 比例参数
    ki = 0.1  # 积分参数
    kd = 0.5  # 微分参数
    integral = 0
    last_error = 0


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
                tx, ty, flag_servo = coord_str.split(",")
                print("(",tx,",",ty,")",flag_servo)

                # 设置目标点
                ### !!! 摄像头的坐标误差
                target_location=(tx,ty,2.5)#晚点再设置吧
            else:
                print(0)

            #print('1')
        except BlockingIOError:
        # 如果没有新的数据到达，则等待一段时间再次尝试接收
            time.sleep(interval)
        except BrokenPipeError:
            time.sleep(interval)
        except ConnectionResetError:
            time.sleep(interval)

    

        # 控制循环
        while True:
            # 获取当前位置
            lx=320
            ly=240
            current_location = (lx,ly,2.5)

            # 计算误差
            error = target_location - current_location

            # 计算PID控制信号
            proportional = error
            integral += error*dt
            derivative = (error - last_error)/dt
            last_error = error

            vx = kp * proportional.lat + ki * integral.lat + kd * derivative.lat
            vy = kp * proportional.lon + ki * integral.lon + kd * derivative.lon
            vz = kp * proportional.alt + ki * integral.alt + kd * derivative.alt

            # 发送控制信号
            send_body_ned_velocity(vx, vy, vz)

            # 检查是否到达目标点
            if error.lat < 0.001 and error.lon < 0.001 and error.alt < 0.1:
                print("Reached target location")
                break

            # 等待一段时间
            time.sleep(0.1)

