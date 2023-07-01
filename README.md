## PXY ##
    - takeoff
        - arm_and_takeoff.py
        - send_body_ned_velocity.py
        - takeoff.py  # main
        - sim_takeoff.py
        - to_release_area.py
## CYT ##
    - scout
        - example1.py
        - example2.py
        - example3.py
        - get_and_send_position.py
        - scout.py
        - send_body_angle.py
        - send_body_ned_velocity.py
##  HZ ##
    - shot
        - shot.py
##  HJW ##
    - RTL
        - RTL1.py
        - RTL2.py
 ---
 ### 7.1更新 ###
 - **pxy**: 起飞、航行至投弹区代码未测试，识别坐标flag尚未定义 测试切换至master分支
 - **cyt**:侦查区代码大体框架已搭好，以三种不同的路径巡航，但send_ned_velocity()函数可能会受场地影响比较大
 - **pxy**: 起飞、航行至投弹区模拟环境测试通过，识别坐标flag尚未定义
 - **hjw**:RTL1返航直接调用飞控自带的RTL飞行模式函数，安全可靠且稳定，经过测试已加入豪华套餐
 - **hjw**:RTL2先经过返航到附近点然后根据图像反馈的xy动态调整位置，直至在接受范围内后land，还问进行模拟测试
