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
 ---
 ### 7.1更新 ###
 - **pxy**: 起飞、航行至投弹区代码未测试，识别坐标flag尚未定义 测试切换至master分支
 - **cyt**:侦查区代码大体框架已搭好，以三种不同的路径巡航，但send_ned_velocity()函数可能会受场地影响比较大
 - **pxy**: 起飞、航行至投弹区模拟环境测试通过，识别坐标flag尚未定义
