from index import set_value,_init,get_value
import time 
from send_body_ned_velocity import send_body_ned_velocity
import cv2
import numpy as np
import socket
import time
import pigpio

def yolo():
    print("vedio open!")
    pi=pigpio.pi()

    servo_pin = 14
    servo_min = 1100  # 舵机最小脉冲宽度
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
    time.sleep(5)
    client_socket, client_address = server_socket.accept()
    print("地面站连接成功")

    #client_socket.setblocking(False)
    interval = 0.1  # 设置轮询间隔
    time.sleep(5)
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


        try:
             #接收数据
            coord = client_socket.recv(4096)
            coord_str = coord.decode("utf-8")
            if coord_str != '0':
                x, y, flag_servo = coord_str.split(",")
                flag_servo=int(flag_servo)
                x=int(x)
                y=int(y)
                set_value(0,flag_servo)
                set_value(2,x)
                set_value(3,y)
                F_servo=get_value(4)
                if (flag_servo == 1 or F_servo == 1) and run_servo == 0 :
                    try:
                        if flag_servo == 1:
                            print("识别到投弹")
                            time.sleep(3)
                        pi.set_servo_pulsewidth(servo_pin, servo_max)  # 最大位置
                        time.sleep(1)
                        pi.set_servo_pulsewidth(servo_pin, (servo_max+servo_min)/2)
                        run_servo = 1
                        print("舵机动了，可以继续执行")
                    except:
                         pass
            elif coord_str == '0':
                flag_servo=0
                x=0
                y=0
                set_value(0,flag_servo)
                set_value(2,x)
                set_value(3,y)
                F_servo=get_value(4)
                

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

        # 关闭连接
            client_socket.close()
            server_socket.close()

        except socket.error as e:
            # 发生其他错误，退出循循环
            print("Error receiving data:")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 关闭连接
    client_socket.close()
    server_socket.close()    
