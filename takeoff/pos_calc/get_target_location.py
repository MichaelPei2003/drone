import math
from dronekit import LocationGlobal

def get_earth_radius(lat):
    # 根据WGS84椭球体模型计算地球半径
    a = 6378137.0  # 赤道半径
    b = 6356752.314245  # 极半径
    e = math.sqrt(1 - (b/a)**2)
    sin_lat = math.sin(math.radians(lat))
    R = a * (1 - e**2) / (1 - e**2 * sin_lat**2)**1.5
    return R

#使用此函数格式如下: get_target_location([机身指向与目标方向的夹角，左负右正]， [距离]， vehicle)

def get_target_location(dheading, x, vehicle):
    heading = vehicle.heading
    alt = vehicle.location.global_frame.alt + 3
    
    heading += dheading

    if heading >= 360:
        heading -= 360
        
    print("target_heading: ", heading)
    
    heading_radians = math.radians(heading)
    
    true_earth_radius = get_earth_radius(vehicle.location.global_frame.lat)

    #change in lat and lon    
    dlon = x * math.sin(heading_radians) * 0.0000093
    dlat = x * math.cos(heading_radians) * 0.000009

    
    print("dlat: ", dlat, "dlon: ", dlon)

    target_location = LocationGlobal(vehicle.location.global_frame.lat + dlat, vehicle.location.global_frame.lon + dlon, alt)
    
    print("target lat: ", target_location.lat, "target lon: ", target_location.lon)
    
    return target_location
