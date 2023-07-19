import cv2
import numpy as np
import socket
import time
import pigpio
from Pidshot import Pidshot
from dronekit import VehicleMode
from arm_and_takeoff import arm_and_takeoff
import time
from send_body_ned_velocity import send_body_ned_velocity

def shot(vehicle):
    pi = pigpio.pi()  # 连接到pigpiod守护进程

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
    arm_and_takeoff(2,vehicle)
    send_body_ned_velocity(0.4,0,0,10,vehicle)
    time.sleep(5)
    vehicle.mode = VehicleMode("RTL")
    time.sleep(3)

    vehicle.mode = VehicleMode("GUIDED")
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
                dx=int(x)
                dy=int(y)
                Pidshot(dx,dy,vehicle)
                if int(flag_servo) == 1 and run_servo == 0 :
                    try:
                        pi.set_servo_pulsewidth(servo_pin, servo_max)  # 最大位置
                        time.sleep(1)
                        run_servo = 1
                    except:
                        pass

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
        except ValueError:
            # 关舵机
            pi.set_servo_pulsewidth(servo_pin, servo_min)  # 最小位置
            time.sleep(1)
            pi.set_servo_pulsewidth(servo_pin, 0)
            pi.stop()  # 断开与pigpiod守护进程的连接

            # 关闭连接
            client_socket.close()
            server_socket.close()

        except socket.error as e:
            # 发生其他错误，退出循循环
            print("Error receiving data:")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 关舵机
    pi.set_servo_pulsewidth(servo_pin, servo_min)  # 最小位置
    pi.set_servo_pulsewidth(servo_pin, 0)  
    pi.stop()  # 断开与pigpiod守护进程的连接

    # 关闭连接
    client_socket.close()
    server_socket.close()
