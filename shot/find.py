from send_body_ned_velocity import send_body_ned_velocity
def find(vehicle=None,l=0,side=0,f=0):
    #f表示飞行方向，f=1表示向右/向前，f=-1表示向左/向后
    #l表示正方形路径的边长
    #side表示走的是那一条边：
    #side==1->向右行进l
    #side==2->向前行进l
    #side==3->向左行进l
    #side==4->向后行进l
    if side==1:
        send_body_ned_velocity(0,f*0.1*l,0,vehicle)
    elif side==2:
        send_body_ned_velocity(-f*0.1*l,0,0,vehicle)
    # elif side==3:
    #     send_body_ned_velocity(0,-0.1,0,vehicle)
    # elif side==4:
    #     send_body_ned_velocity(-0.1,0,0,vehicle)
