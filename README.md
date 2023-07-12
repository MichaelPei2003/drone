## PXY ##
    - takeoff
        - .old
            - to_release_area.py
        - __init__.py
        - arm_and_ned_velocity.py
        - mav_cmd_test.py
        - send_body_ned_velocity.py
        - sim_move.py
        - sim_takeoff.py
        - takeoff.py 
## CYT ##
    - scout
        - control_flight.py
        - example_main.py
        - send_body_ned_velocity.py
        - send_body_angle.py
##  HZ ##
    - shot
        - shot.py
        - sim_shot_main.py
        - shot_main.py
        - send_body_ned_velocity.py
        - arm_and_takeoff.py
##  HJW ##
    - RTL
        - RTL1.py
        - PidControl.py
        - RTLremake.py
        - command_long_send.py
        - example4.py
        - Pidshot.py
        - shot_main.py
        - arm_and_takeoff.py
        - shot.py
        - send_body_ned_velocity.py
        - 主函数shot_main,调用arm_and_takeoff,然后调用shot，shot里再调用Pidshot，Pidshot调用send_body_ned_velocity,还需要改pid和send_body_ned_velocity
 ---
 ### 备忘 ###
 - 当前使用的飞控固件版本为arducopter 3.2.1
 - dronekit使用NED坐标系，z轴正方向指向地面，写参数时需要注意
 - https://mavlink.io/en/messages/common.html (#73, #75, #76)

 ### 7.1更新 ###
 - **pxy**: 起飞、航行至投弹区代码未测试，识别坐标flag尚未定义 测试切换至master分支
 - **cyt**:侦查区代码大体框架已搭好，以三种不同的路径巡航，但send_ned_velocity()函数可能会受场地影响比较大
 - **pxy**: 起飞、航行至投弹区模拟环境测试通过，识别坐标flag尚未定义
 - **hjw**:RTL1返航直接调用飞控自带的RTL飞行模式函数，安全可靠且稳定，经过测试已加入豪华套餐
 - **hjw**:RTL2先经过返航到附近点然后根据图像反馈的xy动态调整位置，直至在接受范围内后land，还未进行模拟测试
 ### 7.2更新 ###
 - **cyt**:改掉了很多很多语法错误，import了很多文件和函数，引用调用了一些全局变量
 - **pxy**:试了怪东西，但是怪东西炸了所以什么都没有变
 - **hjw**:RTL3在RTL2的基础上加入了PID参数控制，补全了pxy最喜欢的调用函数，暂时没有报错，不过必要的P,I,D参数显然还得再试验进行调参
 ### 7.3更新 ###
 - **cyt**:确定了侦查到圆筒时飞机的飞行逻辑，在向左飞时，如果有看见圆筒，则往最左边圆筒偏移，在向右飞时，如果有看见圆筒，则往最右边圆筒偏移，都只在左右方向上移动，运行路径为：←↑→↑←↑→
 ### 7.5更新 ###
 - **pxy**:
    - 修改了前往投弹区控制逻辑
    - 新增test_takeoff.py用于实机飞行测试
    - 废弃了to_release_area.py，原有takeoff.py文件中均删除相应内容
    - 根目录下test_transfer.py整合了原有takeoff.py的内容
    - 新增了__init__.py用于调用子文件夹中的模块
 - **cyt**：
    - 把运动路径改为了：←↑→
    - 改变了调用参数的方法
    - 删除了一些实际没有用到的变量
    - 把一些没用的文件放到了useless文件夹下
 - **hjw**：
    - 把三个函数拆开成三段代码
    - 废弃了没有用的RTL2,鉴定为RTL1和RTL3也可以退役了
    - 修改了一下调用和time.sleep
### 7.6更新 ###
- **pxy**:
    - GUIDE、LOITER、LAND、ALTHOLD模式实机测试:
        - 上述模式功能正常
        - 正常使用LOITER模式需要油门摇杆置于非最低位置，但解锁要求油门摇杆置于最低
        - 手动接管切换至STABILIZE模式后会被后续程序模式切换命令覆盖，每次进行程序模式切换前建议检测是否处于STABILIZE模式以免影响人工介入
    - RTL模式有待测试
    - 注:若程序无法切换模式，是由于pymavlink版本过新导致，请运行sudo pip uninstall pymavlink，然后pip install pymavlink==2.4.8
- **hz**:
    - 拆封了函数，将函数放在shot.py文件中。增加dt，保证实时性
- **cyt**:
    - 加了test1.py代码，理论上能运动一个1x1m的正方形，路径为：↑→↓←，再向下运动1m，但是飞机测试的时候根本不动（恼），但在仿真里能跑起来，可能是飞机缺少了什么装备。正在寻求解决方法...
    - 加了global_frame.py,global_relative_frame.py,local_frame.py,来打印不同参考系下的位置
### 7.7更新 ###
- **pxy**:
    - GPS定位有约50cm的误差，需要纳入考虑
    - 手切RTL返航点准确，需在RTL返回返航点后切换至LAND实现自动落地
- **hjw**:
    - 调整RTL标准参数之后，做到返航高度5米，滞留10秒，降落速度30cm/s，误差现在在80cm左右，目标20cm左右
- **hz**:
    -https://stackoverflow.com/questions/76063407/problems-installing-pymavlink-2-4-8
### 7.9更新 ###
- **hjw**:
    - 修正了新的控制函数，更正了Pid坐标设置参数，设置了新的测试代码example4.py
### 7.10更新 ###
- **cyt**：
    - 试了一下让飞机在空中固定点绕圈的代码，但是看了一下文档发现只能在固定翼上运行，所以还是打算用正常直线的巡航路线来遍历整个场地，多遍历几遍
- **pxy**:
    - send_body_ned_velocity功能模块有修改，参照takeoff文件夹里的就好
- **hjw**:
    - 识别和移动经过测试已经能进行数据响应了，但仍然存在移动的方向误差，显然需要改移动和PID参数
- **hz**:
    - sim_shot_main.py解决了图传阻塞的问题，飞机速度方向vx和vy的方向和图传返回坐标x和y的方向关系有待确定，
    - send_body_ned_velocity.py中vy的呈现方式有问题，准备弃用
### 7.11更新 ###
- **pxy**:
    - 现有send_body_ned_velocity模块只能控制直行，往其它方向移动均不可控转圈
    - MAV_CMD_NAV_ATTITUDE_TIME尝试了一下但是模拟中飞机没用动作，有待研究
- **cyt**：
    - 因为发现了send_body_ned_velocity只能控制飞机向前运动，所以scout部分选择先用send_body_angle来改变飞机的朝向，再控制飞机向前进
    - 增加了不一样的巡航路径：↑←↓←↑←↓，并在每执行一步后都print完成的命令，在仿真上跑了一下两个实例，有时候send_body_angle的函数并不能让飞机转角度（不知道为什么），而且有时候在仿真中转了角度后再向前走，飞机走的飘飘的（跟喝多了一样），不知道在实际的飞机上是不是也会这样（沉思）
- **pxy**:
    - send_body_ned_velocity中，type_mask最左侧两个1改成0则x，y坐标移动均为平移
### 7.12更新 ###
- **cyt**：
    - 把实现路径的方式改回了全部使用send_body_ned_velocity，路径为：←↑→，然后反过来重新走一遍原来的路径：←↓→，并在仿真中跑了之后可以成功按预想的轨迹运动（好耶！），到时候再在真机上测试
