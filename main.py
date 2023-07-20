import cv2
import numpy as np
import socket
import time
import pigpio
from find import find
from dronekit import connect, VehicleMode
import time
from RTL import PidRTL
from scout import scout
from send_body_ned_velocity import send_body_ned_velocity
from send_body_ned_velocity_notime import send_body_ned_velocity_notime
from threading import Thread
from index import _init,get_value
from get_target_location import get_target_location
from pymavlink import mavutil


#connect to drone 
connection_string ='/dev/ttyACM0' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect (connection_string, wait_ready=True) 

_init
k=0.001#控制vx和vy
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
integral_x = 0
integral_y = 0
derivative_x=0
derivative_y=0
last_error_x = 0
last_error_y = 0

allow_error_x=30
allow_error_y=30
count_in_circle = 40
count_in_circle_now = 0
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

#connect to transfer
print("等待地面站连接...")
client_socket, client_address = server_socket.accept()
print("地面站连接成功")

print("get the first vedio")
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

#get scout area start
scout_start = get_target_location(-2, 57, vehicle)



#takeoff and leave tekeoff area
default_heading = vehicle.heading
print("current location: lat: ", vehicle.location.global_frame.lat, "lon: ", vehicle.location.global_frame.lon)
target_location = get_target_location(0, 30, vehicle)
print("Arming motors...")
vehicle.mode = VehicleMode("GUIDED")
print("Vehicle mode: GUIDED")
vehicle.armed = True
print("Vehicle armed")
#if not armed do following loop
while not vehicle.armed:
    print("Waiting for arming...")
    time.sleep(1)
vehicle.mode = VehicleMode("GUIDED")
print("Taking off")
vehicle.simple_takeoff(3.5)
time.sleep(4)
print("target location:", target_location.lat, ", ", target_location.lon, ", ", target_location.alt)
vehicle.simple_goto(target_location, airspeed = 1)
time.sleep(27)
time_start = time.time()

#side,l用于find
"""
l控制无人机飞行的速度
f和side共同控制无人机飞行的方向
"""
side=1
l=2
f=1
count_t = 0 #计算经过几轮while循环


#client_socket.setblocking(False)
interval = 0.1  # 设置轮询间隔

run_servo = 0
#flag
f_takeoff = 0
frtl=0
fshot=0
fscout=0
fstep=0
f_goto_scout = 0
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
            #识别到后重置find中的side和l
            side=1
            l=0
            f=1

            if f_takeoff == 0:
                vehicle.commands.upload()
                print(vehicle.heading)
                print("turning back")
                vehicle.message_factory.command_long_send(
                0, 0,  # target_system, target_component
                mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
                0,  # confirmation
                default_heading,  # param1 (目标偏航角)
                0, 0, 0, 0, 0,0  # param2, param3, param4, param5, param6
                )
                f_takeoff = 1

            if fshot==0:
                target_location_x = int(x)#图传返回的圆筒坐标，是目标点的坐标
                target_location_y = int(y)
            if int(flag_servo) == 1 and run_servo == 0 :
                try:
                    pi.set_servo_pulsewidth(servo_pin, servo_max)  # 最大位置
                    # time.sleep(1)
                    run_servo = 1
                except:
                    pass

        elif coord_str == '0' and f_takeoff == 0 and time.time() - time_start <= 7:
            continue
        elif coord_str == '0' and f_takeoff == 0 and time.time() - time.start > 7:
            f_takeoff = 1

        elif coord_str == '0' and fshot==0:
            print("count_t=",count_t)
            if count_t%20==0:
                side=side%2+1
                print("side=",side)
                print("走了一步")
                if side==1:
                    l=l+1
                    print("l=",l)
                    f=-f
                    print("f=",f)
            if count_t==0:
                find(vehicle,4,side,f)
            else:
                find(vehicle,3*l,side,f)
            if side==1 and f==1:
                print("vehicle向右行进")
            elif side==1 and f==-1:
                print("vehicle向左行进")
            elif side==2 and f==1:
                print("vehicle向前行进")
            elif side==2 and f==-1:
                print("vehicle向后行进")
            if count_t>360:
                print("无法找到目标，放弃，直接投弹")
                try:
                    pi.set_servo_pulsewidth(servo_pin, servo_max)  # 最大位置
                    time.sleep(1)
                    run_servo = 1
                    print("投弹完成，请继续执行")
                    fshot=1
                    break
                except:
                    pass
            count_t=count_t+1
            continue
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
    if fshot==0 and coord_str != '0':    
        # 获取当前位置
        print("shot open!")
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
            send_body_ned_velocity_notime(velocity_vx, velocity_vy, 0.1,vehicle)
        else:
            send_body_ned_velocity_notime(velocity_vx, velocity_vy, 0,vehicle)
            

        # 检查是否到达目标点
        if abs(error_x) < allow_error_x and abs(error_y) < allow_error_y:
            count_in_circle_now = count_in_circle_now + 1
            if count_in_circle_now >= count_in_circle:
                print("Reached target location")
                pi.set_servo_pulsewidth(servo_pin, servo_max)  # 最大位置
                # time.sleep(1)
                run_servo = 1
                print("投弹完成，请继续执行")
                fshot=1
                #wait to move
                break
            if vehicle.location.global_relative_frame.alt>=2:
                send_body_ned_velocity_notime(0,0,0.1,vehicle)
                allow_error_x=allow_error_x+10
                allow_erroe_y=allow_error_y+10
                kp=kp*0.8
                ki=ki*0.8
                kd=kd*0.8
        else:
            count_in_circle_now=0

#from shot area to scout area
vehicle.simple_goto(scout_start, airspeed = 1.5)
time.sleep(17)
print("go to scout")
vehicle.message_factory.command_long_send(
0, 0,  # target_system, target_component
mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
0,  # confirmation
default_heading,  # param1 (目标偏航角)
0, 0, 0, 0, 0,0  # param2, param3, param4, param5, param6
)
time.sleep(2)
print("move over")

#model scout
print("scout open!")
daemon_thread = Thread(target=scout,args=(vehicle,))
daemon_thread.daemon = True  # 设置线程为守护线程
# 启动守护线程
daemon_thread.start()
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
    
    fscout=get_value(0)
    if fscout==1:
        break

#model RTL      
print("RTL open!")
vehicle.mode = VehicleMode("RTL")
time.sleep(20)
vehicle.mode = VehicleMode("GUIDED")

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
            PidRTL(dx,dy,vehicle)
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
