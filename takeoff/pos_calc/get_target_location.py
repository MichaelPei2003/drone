import math
from dronekit import LocationGlobal

#使用此函数格式如下: get_target_location([机身指向与目标方向的夹角，左负右正]， [距离]， vehicle)

def get_target_location(dheading, x, vehicle):
    heading = vehicle.heading
    alt = vehicle.location.global_frame.alt + 3
    
    heading += dheading

    if heading >= 360:
        heading -= 360
        
    print("target_heading: ", heading)
    
    heading_radians = math.radians(heading)

    #change in lat and lon    
    dlon = x * math.sin(heading_radians) * 0.0000093
    dlat = x * math.cos(heading_radians) * 0.000009

    target_location = LocationGlobal(vehicle.location.global_frame.lat + dlat, vehicle.location.global_frame.lon + dlon, alt)
    
    print(target_location.lat, target_location.lon)
    
    return target_location