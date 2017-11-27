# Python3
# Calculating Angle

#                                             /|
#                                            / |
#                                           /  |
#                                          /   |
# Tan x(Degree) = x/y (Opposite/Adjacent) /____|
# Inverse Tan of x/y = Angle-degrees

import math
import sys
import PiPlate_MotorDrv

print(sys.version )
motorDrvVersion = MotorDrv.version()
print("Motor Controller: {0}".format(motorDrvVersion))

addr = 0
ctl0 = MotorDrv.MotorDrv(addr)
ctl0.displayCtl()

axisMax = 32876
minSpeed = 20 # 25% of axisMax

while True:
    leftSpeed  = 100
    rightSpeed = 100

    x = float(input("x: "))
    y = float(input("y: "))
    
    angle = math.degrees(math.atan2(x,y))
    if(angle < 0):
        angle = angle + 360
    elif((abs(angle) == 0.0) or (abs(angle) == 360)):
        quad = 'Right Turn/Spin'
        ctl0.right(addr)
    elif(abs(angle) == 90.0):
        quad = 'Forward'
        ctl0.forward(addr)
    elif(abs(angle) == 180.0):
        quad = 'Left Turn/Spin'
        ctl0.left(addr)
    else: # (abs(angle) == 270):
        quad = 'Reverse'
        ctl0.reverse(addr)
    

    if((abs(angle) > 0) and (abs(angle) < 90)):
        quad = 'I - Forward Right'
        leftSpeed  = (x/abs(axisMax) * 100)
        rightSpeed = (y/abs(axisMax) * 100)
    elif((abs(angle) > 90) and (abs(angle) <180)):
        quad = 'II - Forward Left'
        leftSpeed  = (y/abs(axisMax) * 100)
        rightSpeed = (x/abs(axisMax) * 100)
    elif((abs(angle) > 180) and (abs(angle) <270)):
        quad = 'III - Reverse Left'   
        leftSpeed  = (y/abs(axisMax) * 100)
        rightSpeed = (x/abs(axisMax) * 100)
    elif((abs(angle) > 270) and (abs(angle) <360)):
        quad = 'IV - Reverse Right'  
        leftSpeed  = (x/abs(axisMax) * 100)
        rightSpeed = (y/abs(axisMax) * 100)
    else: 
        leftSpeed  = 100
        rightSpeed = 100
    
    if(x == 1 and y == 1):
        leftSpeed  = 100
        rightSpeed = 100        
        
    if(leftSpeed < minSpeed): # and (x != 0) or (y !=0): 
        leftSpeed = 20
    elif(rightSpeed < minSpeed): # and (x != 0) or (y !=0): 
        rightSpeed = 20    
        
    print('x: {0} y:{1} = {2:.2f} Degrees Speed(L/R): {3:.2f} : {4:.2f}'.format(x,y,angle,leftSpeed,rightSpeed))
    print() 
    
    

