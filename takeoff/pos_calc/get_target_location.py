import math

#使用此函数格式如下: get_target_location([机身指向与目标方向的夹角，左负右正]， [距离]， vehicle)

def get_target_location(target_heading_relative, x, vehicle):
    lat = vehicle.location.global_frame.lat
    lon = vehicle.location.global_frame.lon
    heading = vehicle.heading

    heading += 4.5#magnetic declination
    
    heading += target_heading_relative

    if heading >=360:
        heading -= 360
        
    #change in lat and lon    
    dlon = x * math.sin(heading)
    dlat = x * math.cos(heading)

    target_lat = lat + dlat
    target_lon = lon + dlon
    
    return target_lat, target_lon