from dronekit import connect, VehicleMode
import time
# 定义获取并传输位置的函数
def get_and_send_position(vehicle = None):
    while True:
        current_location = vehicle.location.global_relative_frame
        location_str = "Latitude: {0}, Longitude: {1}, Altitude: {2}".format(
            current_location.lat,
            current_location.lon,
            current_location.alt
        )
        loc = current_location
        print(location_str)
        time.sleep(1)
