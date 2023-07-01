# 发送"返航"指令 
print("Returning to Launch") 
# 返航，只需将无人机的飞行模式切换成"RTL(Return to Launch)" 
# 无人机会自动返回home点的正上方，之后自动降落 
vehicle.mode = VehicleMode("RTL") 

# 退出之前，清除vehicle对象 