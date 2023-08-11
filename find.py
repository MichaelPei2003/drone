from send_body_ned_velocity_notime import send_body_ned_velocity_notime
import math
import numpy as np
def find(vehicle=None,l=0,side=0,f=0):
    #f表示飞行方向，f=1表示向右/向前，f=-1表示向左/向后
    #l表示正方形路径的边长
    #side表示走的是那一条边：
    if side==1:
        if vehicle._rngfnd_distance>4.2:
            send_body_ned_velocity_notime(0, f*0.1*l, 0.02,vehicle)
        elif vehicle._rngfnd_distance<3.6:
            send_body_ned_velocity_notime(0, f*0.1*l, -0.02,vehicle)
        else:
            send_body_ned_velocity_notime(0, f*0.1*l, 0,vehicle)

    elif side==2:
        if vehicle._rngfnd_distance>4.2:
            send_body_ned_velocity_notime(f*0.1*l, 0, 0.02,vehicle)
        elif vehicle._rngfnd_distance<3.6:
            send_body_ned_velocity_notime(f*0.1*l, 0, -0.02,vehicle)
        else:
            send_body_ned_velocity_notime(f*0.1*l, 0, 0,vehicle)

    # elif side==3:
    #     send_body_ned_velocity(0,-0.1,0,vehicle)
    # elif side==4:
    #     send_body_ned_velocity(-0.1,0,0,vehicle)


#######以下是pid_move函数所需的类
"""
Cix类:用于存储ix
   属性zero:保留zero个数值
   属性figet:当前数组下标
"""
class Cix:
    def __init__(self,zero,figet):
        self.ix=np.zeros(zero)
        self.figet=figet
    def getix(self,figet,zero):
        return self.ix[figet%zero]
    def setix(self,ix,zero):
        self.ix[self.getfiget()%zero]=ix
    def getfiget(self):
        return int(self.figet)
    def setfiget(self):
        self.figet=self.figet+1

"""
Ciy类:用于存储iy
    属性zero:保留zero个数值
    属性figet:当前数组下标
"""
class Ciy:
    def __init__(self,zero,figet):
        self.iy=np.zeros(zero)
        self.figet=figet
    def getiy(self,figet,zero):
        return self.iy[figet%zero]
    def setiy(self,iy,zero):
        self.iy[self.getfiget()%zero]=iy
    def getfiget(self):
        return int(self.figet)
    def setfiget(self):
        self.figet=self.figet+1

"""
Clx类:用于存储last_error_x
    属性lx:存储last_error_x
"""
class Clx:
    def __init__(self):
        #赋初值零
        self.lx=0
    def getlx(self):
        return self.lx
    def setlx(self,lx):
        self.lx=lx

"""
Cly类:用于存储last_error_y
    属性ly:存储last_error_y
"""
class Cly:
    def __init__(self):
        #赋初值零
        self.ly=0
    def getly(self):
        return self.ly
    def setly(self,ly):
        self.ly=ly

########
zero=20
figet=0
#########cix和ciy的初始化
cix=Cix(zero,figet)
ciy=Ciy(zero,figet)
#########
#########clx和cly的初始化
clx=Clx()
cly=Cly()
#########
def pid_move(vehicle,target_location_x,target_location_y):
   
    k=0.002#控制vx和vy
    # 初始化PID控制器
    dt=0.5
    kp = 0.41  # 比例参数0.5/0.48
    ki = 0.06  # 积分参数0.1
    kd = 0.22  # 微分参数0.18
    max_vx=0.4 #前后方向最大速度
    max_vy=0.4 #左右方向最大速度
    error_x = 0 
    error_y = 0
    proportional_x=0
    proportional_y=0
    integral_x=0
    integral_y=0
    derivative_x=0
    derivative_y=0

    # 获取当前位置
    current_location_x=300
    current_location_y=220

    # 计算误差
    error_x = target_location_x - current_location_x
    error_y = -(target_location_y - current_location_y)
    #########此处用于存储数组ix和iy第figet%zero位置的值
    cix.setix(error_x*dt/5,zero)
    ciy.setiy(error_y*dt/5,zero)
    print("输出")
    print("setix=",error_x*dt/5)
    print("setiy=",error_y*dt/5)
    print("输出结束")
    #########figet值＋1
    cix.setfiget()
    ciy.setfiget()

    # 计算PID控制信号 
    proportional_x = error_x
    proportional_y = error_y
    print("下面开始打印每次的ix和iy的累加值")
    for i in range(zero):
    #    print("ix[",i,"]=",cix.getix(i,zero))
    #    print("iy[",i,"]=",ciy.getiy(i,zero))
        integral_x +=cix.getix(i,zero)
        integral_y +=ciy.getiy(i,zero)
    derivative_x = (error_x - clx.getlx()) / dt
    derivative_y = (error_y - cly.getly()) / dt
    clx.setlx(error_x)
    cly.setly(error_y)

    vx = kp * proportional_x + ki * integral_x + kd * derivative_x
    vy = kp * proportional_y + ki * integral_y + kd * derivative_y
    velocity_vx=k*vy
    velocity_vy=k*vx
    if velocity_vx>max_vx:
        integral_x=0
        velocity_vx=max_vx
    if velocity_vy>max_vy:
        velocity_vy=max_vy
        integral_y=0
    print("x:",velocity_vx,"y:",velocity_vy,"alt:",vehicle.location.global_relative_frame.alt)
    print("px:",kp*proportional_y,"ix:",ki * integral_y,"dx:",kd * derivative_y)
    print("py:",kp*proportional_x,"iy:",ki * integral_x,"dy:",kd * derivative_x)
    # 发送控制信号
    if abs(target_location_x-current_location_x)<50 and abs(target_location_y-current_location_y)<50:
        integral_x=0
        integral_y=0
    if vehicle._rngfnd_distance>4.5:
        send_body_ned_velocity_notime(velocity_vx, velocity_vy, 0.05,vehicle)
    elif vehicle._rngfnd_distance<3.6:
        send_body_ned_velocity_notime(velocity_vx, velocity_vy, -0.05,vehicle)
    else:
       send_body_ned_velocity_notime(velocity_vx, velocity_vy, 0,vehicle)
