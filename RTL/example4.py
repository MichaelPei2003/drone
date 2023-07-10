import cv2
import numpy as np
import socket
import time
from dronekit import connect

from PidControl import PidControl
import sys
sys.path.append("takeoff")
from takeoff.arm_and_takeoff import arm_and_takeoff
from takeoff.send_body_ned_velocity import send_body_ned_velocity

#connect to drone 
#for simulation use:
#connection_string ='192.168.43.169:14550' #RPI's IP, port is always 14550
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 

pi = pigpio.pi()  # 连接到pigpiod守护进程


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

run_servo = 0   #  the flag to servo

#takeoff and leave takeoff area
arm_and_takeoff(1, vehicle) #arm_and_takeoff(aTargetAltitude, vehicle)
for i in range(10):
    send_body_ned_velocity(0.8, 0, 0, vehicle)
    time.sleep(1)

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
    
    flag_to_release = int(stringData)
    
    #如果没用检测到任何东西则直飞
    #如果一直未检测到目标飞行器不会自动停止！！！
    if flag_to_release == 0:
        send_body_ned_velocity(0.8, 0, 0, vehicle)#(vx, vy, vz, vehicle)，单位m/s

    # 显示图像
 #   cv2.imshow('frame', frame)

    try:
         #接收数据
        coord = client_socket.recv(4096)
        coord_str = coord.decode("utf-8")
        if coord_str != '0':
            x, y, flag_servo = coord_str.split(",")
            print("(",x,",",y,")",flag_servo)
            PidControl(x,y,vehicle)

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
        pi.stop()  # 断开与pigpiod守护进程的连接

        # 关闭连接
        client_socket.close()
        server_socket.close()

    except socket.error as e:
        # 发生其他错误，退出循循环
        print("Error receiving data:")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
pi.stop()  # 断开与pigpiod守护进程的连接


# 关闭连接
client_socket.close()
server_socket.close()
