def _init():
    global _global_dict
    _global_dict = {}


def set_value(key,value):
    '''定义一个全局变量'''
    _global_dict[key] = value

def get_value(key,defValue=None):
    '''定义一个全局变量，不存在则返回默认值'''
    try:
        return _global_dict[key]
    except KeyError:
        return defValue


#0,speed_x    #靠近圆筒时的x速度
#1,speed_y    #靠近圆筒时的y速度
#2,duration    #每一段巡航路线的持续时间
#3,start_time    #每一段巡航路线的开始时间
#4,v_x    #巡航的x速度
#5,v_y    #巡航的y速度
#6,cyl    #是否检测到圆筒
#7,loc    #位置
#8,vehicle    #所连接的无人机
