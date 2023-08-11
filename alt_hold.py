from send_body_ned_velocity_notime import send_body_ned_velocity_notime

def alt_hold(target_alt, vehicle):
    while vehicle._rngfnd_distance < target_alt-0.2:
        print("Increasing alt, current alt:", vehicle._rngfnd_distance)
        send_body_ned_velocity_notime(0, 0, -0.5, vehicle)
    
    while vehicle._rngfnd_distance > target_alt+0.1:
        print("Decreasing alt, current alt: ", vehicle._rngfnd_distance)
        send_body_ned_velocity_notime(0, 0, 0.3, vehicle)
    send_body_ned_velocity_notime(0,0,0,vehicle)
