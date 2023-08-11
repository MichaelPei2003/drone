from pymavlink import mavutil 

def set_heading(vehicle, target_heading): 
    vehicle.message_factory.command_long_send(
                        0,
                        0,  # target_system, target_component
                        mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
                        0,  # confirmation
                        target_heading,  # param1 (目标偏航角)
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,  # param2, param3, param4, param5, param6
     )
