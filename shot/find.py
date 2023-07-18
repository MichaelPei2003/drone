from send_body_ned_velocity import send_body_ned_velocity
def find(vehicle=None,l=0,side=0,f=0):
    #f表示飞行方向，f=1表示向右/向前，f=-1表示向左/向后
    #l表示无人机的飞行速度
    #side表示走的是水平边/竖直边：
    #side==1->向左/右行进l
    #side==2->向前/后行进l
    if side==1:
        send_body_ned_velocity(0,f*0.1*l,0,vehicle)
    elif side==2:
        send_body_ned_velocity(f*0.2*l,0,0,vehicle)
