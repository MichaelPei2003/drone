from shot import shot
from dronekit import connect
from arm_and_takeoff import arm_and_takeoff
#connect to drone 
connection_string ='192.168.43.80:14550' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=False) 
shot(vehicle)

print("已到达指定位置，请执行下一步命令...")

