from dronekit import connect 

def init():
    connection_string ='/dev/ttyACM0' #Com of current FCM connection
    print('Connectingto vehicle on: %s' % connection_string) 
    vehicle = connect(connection_string, wait_ready=False) 
    return vehicle