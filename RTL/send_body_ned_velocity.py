from pymavlink import mavutil
import time

def send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration=0,vehicle = None):

    if vehicle == None:
        print("Vehicle info unknown, please take over controls.")

    msg = vehicle.message_factory.set_position_target_local_ned_encode(

        0,       # time_boot_ms (not used)

        0, 0,    # target system, target component

        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.

        0b0000111111000111, # type_mask

        0, 0, 0, # x, y, z positions (not used)

        velocity_x, velocity_y, velocity_z, # m/s

        0, 0, 0, # x, y, z acceleration

        0, 0)

        vehicle.send_mavlink(msg)
