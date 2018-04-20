# !/usr/bin/python3
# Calculating Angle
#
#                                             /|
#                                            / |
#                                           /  |
#                                          /   |
# Tan x(Degree) = x/y (Opposite/Adjacent) /____|
# Inverse Tan of x/y = Angle-degrees
#
# NOTE: This was tested using an XBox USB wireless controller.
#
# Upate March 2018 - Added HC-SR04 Sonic sensor module. In this case, 
#     we are looking to determne if an opbject is within 10cm/4 inches 
#    'in front' or forward of us. If so, initate a stop or alternate 
#     manuver. 
#
#==========================================================================

import math
import sys
import MotorDrv
import pygame
from time import sleep
import piplates.MOTORplate as MOTOR          #import the MOTORplate module
#import SR04                                  # RPi HC-SR04 multi-threaded 
# import SR04_pigpio as SR04                 # The pigpio library verson requires the
                                             #  pigiod deamon to be running. 
print("New SR04 module loaded...")

def PygameHandler(events):
# Read pygame events for axis and button entries
	global y
	global x
	
	for event in events:
		if event.type == joystick.JOYAXISMOTION:
			y = float(joystick.get_axis(0))
			x = float(joystick.get_axis(1))
	
	return

# Function to set all drives off
def MotorOff():
    #print("Stopping Motor")
    MOTOR.dcSTOP(ctl,FL)
    MOTOR.dcSTOP(ctl,FR)
    MOTOR.dcSTOP(ctl,RL)
    MOTOR.dcSTOP(ctl,RR)
        
    status = "stopped"
    return status

def resetCtl(ctl):
	MOTOR.clrLED(ctl)
	sleep(1)
	MOTOR.RESET(ctl)
	return

def initMotor(FLdir,FRdir,RLdir,RRdir):
	#print("Setting: ",rotation)
	MOTOR.dcCONFIG(ctl,FL,FLdir,0.0,0.0)
	MOTOR.dcCONFIG(ctl,FR,FRdir,0.0,0.0)
	MOTOR.dcCONFIG(ctl,RL,RLdir,0.0,0.0)
	MOTOR.dcCONFIG(ctl,RR,RRdir,0.0,0.0)
	
	MOTOR.dcSTART(ctl,FL)
	MOTOR.dcSTART(ctl,FR)
	MOTOR.dcSTART(ctl,RL)
	MOTOR.dcSTART(ctl,RR)
	
	if   (FLdir == FRdir == RLdir == RRdir  == "cw") : 
		status = "forward"
		return
	elif (FLdir == FRdir == RLdir == RRdir  == "ccw"): 
		status = "reverse" 
		return
	elif (FLdir == RLdir == "cw"  and FRdir == RRdir == "ccw"):
		status = "left"
	elif (FLdir == RLdir == "ccw" and FRdir == RRdir == "cw"):
		status = "right"
	else:
		 status = 'something not right'
	
	return status 

def fwd(FLspeed,FRspeed,RLspeed,RRspeed):
	# print("Forward motion called. CTL: ",ctl)
	status = initMotor('cw','cw','cw','cw')
	MOTOR.dcSTART(ctl, FL)
	MOTOR.dcSTART(ctl, FR)
	MOTOR.dcSTART(ctl, RL)
	MOTOR.dcSTART(ctl, RR)
	
	status = "forward"
	return status

def reverse(FLspeed,FRspeed,RLspeed,RRspeed):
	#print("Reverse motion called. CTL: ")
	status = initMotor('ccw','ccw','ccw','ccw')
	MOTOR.dcSTART(ctl, FL)
	MOTOR.dcSTART(ctl, FR)
	MOTOR.dcSTART(ctl, RL)
	MOTOR.dcSTART(ctl, RR)
	
	status = "reverse"
	return status

def left(FLspeed,FRspeed,RLspeed,RRspeed):
	status = initMotor('ccw','cw','ccw','cw')
	MOTOR.dcSTART(ctl,FL)
	MOTOR.dcSTART(ctl,FR)
	MOTOR.dcSTART(ctl,RL)
	MOTOR.dcSTART(ctl,RR)
	
	status = 'left'
	return status

def right(FLspeed,FRspeed,RLspeed,RRspeed):
	status = initMotor('cw','ccw','cw','ccw')
	MOTOR.dcSTART(ctl,FL)
	MOTOR.dcSTART(ctl,FR)
	MOTOR.dcSTART(ctl,RL)
	MOTOR.dcSTART(ctl,RR)
	
	status = 'right'
	return status

def motorSpeed(FLspeed,FRspeed,RLspeed,RRspeed):
	MOTOR.dcSPEED(ctl,FL,FLspeed)
	MOTOR.dcSPEED(ctl,FR,FRspeed)
	MOTOR.dcSPEED(ctl,RL,RLspeed)
	MOTOR.dcSPEED(ctl,RR,RRspeed)

def fwdObstruction(distance):
	inches = distance * 0.39370078740158         # calculate inches
	feet = inches / 12                           # calculate feet
	print("Panic, we are {0:0,.2f} inches from an object".format(inches))
	status = MotorOff()                          # kill motors
	sleep(2)                                     # pause for 2 seconds
	Speed = 20
	status = reverse(Speed,Speed,Speed,Speed)
	motorSpeed(Speed,Speed,Speed,Speed)
	sleep(2)
	status = MotorOff()
	status = 'obstruction'
	print("WOW...that was close...\n") 
	return status

def chkDist(status):
	distance = SR04.getDist()
	if (distance < 15)  and (status != 'obstruction'):
		if status != 'obstruction' and (status != 'stopped'): 
			status = fwdObstruction(distance)
			return status
		else:
			#print("Status is: {0}".format(status))
			status != 'stopped'
			sleep(2)
			return status
	return status

def main():
	
	#=======================================================================
	#	Initialize Variables, processes, threads
	#=======================================================================
	
	#   Initialize multi-threaded HC-SR04 sonic sensor
	# DistThread = SR04.ChkDist(1,"ChkDist-1")
	# DistThread.start()
	
	# Define Motors
	global FL
	global FR
	global RL
	global RR	
	global status
		
	FL = 1				# Define Motor 1 = Front Left   - FL
	FR = 2  			# Define Motor 2 = Fright Right - FR
	RL = 3  			# Defome Motor 3 = Rear Left    - RL
	RR = 4  			# Define Motor 4 = Rear Right   - RR
	
	#Initalized the Xbox controller via the pygame module
	pygame.init()
	
	joystick = pygame.joystick.Joystick(0)
	joystick.init()
	print("JS Initialized: ",joystick.get_init())  # Return 1 or True if Successful
	print(joystick.get_name())
	
	#PiPlate Motor controller
	motorDrvVersion = MotorDrv.version()
	print("Motor Controller: {0}".format(motorDrvVersion))
	
	motor = MOTOR
	global ctl
	ctl = 1
	resetCtl(ctl)
	status = initMotor('ccw','ccw','ccw','ccw')
	for i in range(10):
		MOTOR.clrLED(ctl)
		sleep(.0625)
		MOTOR.setLED(ctl)
		sleep(.0625)
	print("Reset and initalize controller {0} and motors".format(ctl))
	
	axisMax = 1
	minSpeed = 5
	obstruction = 20 
	
	
	#=======================================================================
	# Main Logic Loop Start 
	#=======================================================================
	#            Forward
	#         (-179 / 179)
	#              180
	#               |
	#               |
	#Left   270 ----+------ 90  Right
	#      (-90)    |
	#               |
	#            360 / 0
	#           (-1 / 1)
	#            Reverse		
	#=======================================================================
	
	while True:
		leftSpeed  = 100
		rightSpeed = 100
		#sleep(.25)
	
		#status = chkDist(status)
	
		for event in pygame.event.get():
			if event.type == pygame.JOYBUTTONDOWN:
				B = joystick.get_button(1)
				if (B == 1):
					print("Button B:",B)
					status = MotorOff()
				
				A = joystick.get_button(0)
				if (A == 1):
					print("Button A:",A)
					# exit()
					pass
					
			if event.type == pygame.JOYAXISMOTION:
				y = joystick.get_axis(1)
				x = joystick.get_axis(0) 
				speed = joystick.get_axis(2)
			    
				angle = math.degrees(math.atan2(x,y))
				#status = chkDist(status)	
			
		#===========================================================================================
		# Determining drive direction is based on the calculated angle of the joystick's
		# x and y offset from each other.
		# NOTE: depending on the direction, forward, forward right, forward left, 
		#       left, right, reverse left, reverse right, the speed of the left or 
		#       right axels are adjusted by the x and y values. Right and left
		#       axels speeds are determined by the x OR y offset values from its axis.
		# 
		# Up/down or forward/reverse speed is determined by the veritical Y axis.
		# Left/Right speed is determined by the horizontal X axis. 
		#
		# ==========================================================================================
	
				if(angle < 0):
					angle = angle  + 360
	
				yAxis = abs((y/axisMax * 100))
				xAxis = abs((x/axisMax * 100))
				
				# Hard Forward
				if(angle ==  180):
					leftSpeed  = yAxis
					rightSpeed = yAxis
					if status != 'forward':
						status = MotorOff()
						status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					status = "forward"
	
				# Forward Right Turning Angle 
				if(angle >= 135 and angle < 180 and angle != 180):
					leftSpeed  = yAxis
					rightSpeed = yAxis+(xAxis/2)
					if status != 'forward':
						status = MotorOff()
						status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)

				# Forward Right Turning Angle 
				if(angle > 90 and angle < 135 and angle != 90):
					leftSpeed  = xAxis
					rightSpeed = yAxis+(xAxis/2) if (yAxis+(xAxis/2))  > 10 else 20
					if status != 'forward':
						status = MotorOff()
						status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)


				# Forward Left Turning Angle 
				if(angle > 180 and angle < 226 and angle != 180):
					leftSpeed  = yAxis-(xAxis/2) 
					rightSpeed = yAxis
					if status != 'forward':
						status = MotorOff()
						status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)

				# Forward Left Turning Angle 
				if(angle >= 226 and angle < 270):
					leftSpeed  = yAxis-(xAxis/2) if (yAxis-(xAxis/2))  > 10 else 20
					rightSpeed = xAxis
					if status != 'forward':
						status = MotorOff()
						status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
	
				#Hard Left
				if(angle == 270):
					leftSpeed  = xAxis
					rightSpeed = xAxis				
					if status != 'left':
						status = MotorOff()
						status = left(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					status = "left"

				# Reverse Right Turning Angle 
				if(angle > 270 and angle <= 315):
					leftSpeed  = yAxis
					rightSpeed = xAxis-(yAxis/2) if (xAxis-(yAxis/2))  > 10 else 20
					if status != 'reverse':
						status = MotorOff()
						status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					status = "reverse"

				# Reverse Right Turning Angle 
				if(angle > 315 and angle <= 360):
					leftSpeed  = yAxis
					rightSpeed = xAxis # -(yAxis/2) if (xAxis-(yAxis/2))  > 10 else 20
					if status != 'reverse':
						status = MotorOff()
						status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					status = "reverse"
	
				# Hard Reverse
				if(angle == 0 ):
					leftSpeed  = yAxis
					rightSpeed = yAxis
					if status != 'reverse':
						status = MotorOff()
						status = reverse(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					status = "reverse"

				# Reverse Left Turning Angle 
				if(angle > 0 and angle <= 45):
					leftSpeed  = xAxis
					rightSpeed = yAxis-(xAxis/2) if (yAxis-(xAxis/2))  > 10 else 20
					if status != 'reverse':
						status = MotorOff()
						status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					status = "reverse"
					
				# Reverse Left Turning Angle 
				if(angle > 45 and angle < 90):
					leftSpeed  = xAxis
					rightSpeed = yAxis #-(xAxis/2) if (yAxis-(xAxis/2))  > 10 else 20
					if status != 'reverse':
						status = MotorOff()
						status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					status = "reverse"
		
				#Hard Right Turn
				if(angle == 90.0):
					leftSpeed  = xAxis
					rightSpeed = xAxis
					if status != 'right':
						status = MotorOff()					
						status = right(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
					status = "right"
			
				if xAxis <=1 and yAxis <= 1 and status != 'stopped':
					status = MotorOff()
				
				print('x: {0:>6.3f} y:{1:>6.3f} = {2:.0f} Degrees Speed(L/R): {3:.2f} : {4:.2f} Status: {5}'.format(abs(x)*100,abs(y)*100,angle,leftSpeed,rightSpeed,status))		
			
	return

if __name__ == '__main__':
    main()
	#print("BREAK DOWN, Something went wrong")	
