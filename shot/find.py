from send_body_ned_velocity import send_body_ned_velocity
def find(vehicle=None,l=0,side=0,f=0):
    #f表示飞行方向，f=1表示向右/向前，f=-1表示向左/向后
    #l表示无人机的飞行速度
    #side表示走的是水平边/竖直边：
    #side==1->向左/右行进l
    #side==2->向前/后行进l
    if side==1:
        send_body_ned_velocity(0,f*0.08*l,0,vehicle)
    elif side==2:
        send_body_ned_velocity(f*0.2*l,0,0,vehicle)

def find_move(vehicle,count_t,l,side,f):
    print("count_t=",count_t)
    if count_t%20==0:
        side=side%2+1
        print("side=",side)
        print("走了一步")
        if side==1:
            l=l+1
            print("l=",l)
            f=-f
            print("f=",f)
    if count_t==0:
        find(vehicle,4,side,f)
    else:
        find(vehicle,3*l,side,f)
    if side==1 and f==1:
        print("vehicle向右行进")
    elif side==1 and f==-1:
        print("vehicle向左行进")
    elif side==2 and f==1:
        print("vehicle向前行进")
    elif side==2 and f==-1:
        print("vehicle向后行进")
    return l,side,f
    