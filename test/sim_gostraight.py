from dronekit import connect, VehicleMode
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ..takeoff.arm_and_takeoff import arm_and_takeoff
import time
import math
from pymavlink import mavutil

#connect to drone 
connection_string ='192.168.43.169:14550' #Com of current FCM connection
print('Connectingto vehicle on: %s' % connection_string) 
vehicle = connect(connection_string, wait_ready=True) 

def goStraight(vehicle,x,y,z):
    if x is not None or y is not None:
        tx = float(x)
        ty = float(y)
        tz = float(z)
        if (math.isnan(x) or math.isinf(x)) or (math.isnan(y) or math.isinf(y)) or (math.isnan(z) or math.isinf(z)):
            raise ValueError("Altitude was NaN or Infinity. Please provide a real number")
        vehicle._master.mav.command_long_send(0, 0, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF_LOCAL,
                                               0, 0, 0, 0, 0, tx, ty, tz)

goStraight(vehicle,5,5,5)
print("完成")
time.sleep(5)
print("程序结束")