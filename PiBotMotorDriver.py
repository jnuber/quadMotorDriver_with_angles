# #!/usr/bin/python3
# Calculating Angle
#
#                                             /|
#                                            / |
#                                           /  |
#                                          /   |
# Tan x(Degree) = x/y (Opposite/Adjacent) /____|
# Inverse Tan of x/y = Angle-degrees

import math
import sys
import MotorDrv
import pygame
from time import sleep

"""
Read pygame events for axis and button entries
"""
def PygameHandler(events):
	global y
	global x
	
	for event in events:
		if event.type == joystick.JOYAXISMOTION:
			y = float(joystick.get_axis(0))
			x = float(joystick.get_axis(1))
	


"""
Initalized the Xbox controller via the pygame module
"""
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print("JS Initialized: ",joystick.get_init())  # Return 1 or True if Successful
print(joystick.get_name())


"""
PiPlate Motor controller
"""
motorDrvVersion = MotorDrv.version()
print("Motor Controller: {0}".format(motorDrvVersion))

addr = 0
ctl0 = MotorDrv.MotorDrv(addr)
ctl0.displayCtl()

axisMax = 1
minSpeed = 20 # 20% of axisMax


while True:
	sleep(.25)
	leftSpeed  = 100
	rightSpeed = 100
    
	for event in pygame.event.get():
		y = joystick.get_axis(1)
		x = joystick.get_axis(0)
		speed = joystick.get_axis(2)
		# print("x: {0:>6.3f}  y: {1:>6.3f}".format(x,y))
		B = joystick.get_button(1)
		if (B == 1):
			print("Button B:",B)

		angle = math.degrees(math.atan2(x,y))
		
		if(angle < 0):
			angle = angle + 360
		elif((abs(angle) == 0.0) or (abs(angle) == 360)):
			quad = 'Revese'
			ctl0.reverse(addr)
		elif(abs(angle) == 90.0):
			quad = 'Left Turn/Spin'
			ctl0.left(addr)
		elif(abs(angle) == 180.0):
			quad = 'Forward'
			ctl0.forward(addr)
		else: # (abs(angle) == 270):
			quad = 'Right Turn/Spin'
			ctl0.right(addr)
	

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

		if(x == 0 and y == 0):
			leftSpeed  = 0.0
			rightSpeed = 0.0
			ctl0.stop(addr)   
		"""
		if(leftSpeed < abs(minSpeed)): # and (x != 0) or (y !=0): 
			leftSpeed = minSpeed
		if(rightSpeed < abs(minSpeed)): # and (x != 0) or (y !=0): 
			rightSpeed = minSpeed    
		"""
		
		print('x: {0:>6.3f} y:{1:>6.3f} = {2:.0f} Degrees Speed(L/R): {3:.2f} : {4:.2f}  Speed:{5:.2f}'.format(x,y,angle,abs(leftSpeed),abs(rightSpeed),speed))
    
    

