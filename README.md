# quadMotorDriver_with_angles
Reseach Credits due: https://pythonhosted.org/triangula/sixaxis.html

Program to drive Raspberry Pi3 controlled 4 wheel chassi rover. Motors controlled by PiPlater Motor controller and XBox wireless
controller via Pygame library. Reading a USB wireless XBox controller's left axis number 0,1, determined the joystick's angle from when pressed. 

Then used the the x/y value's offset from center to adjust left/right wheel speeds. Full forward, Reverse, hard left and right wheels are throttled at 100%. Other directions such as forward left/right, reverse left/right, one side will overdrive the other. For example, turning left, right side wheels will over drive left side and visa versa. NOTE that depending direction, x/y value are not always assigned to the same chassi wheels's drive side. 

 
 Calculating Angle                           /|
                                            / |
                                           /  |
                                          /   |
 Tan x(Degree) = x/y (Opposite/Adjacent) /____|
 Inverse Tan of x/y = Angle-degrees

===========================================================================================
 Determining drive direction is based on the calculated angle of the joystick's
 x and y offset from each other.
 NOTE: depending on the direction, forward, forward right, forward left, 
       left, right, reverse left, reverse right, the speed of the left or 
       right axels are adjusted by the x and y values. Right and left
       axels speeds are determined by the x OR y offset values from its axis.
 
 Up/down or forward/reverse speed is determined by the veritical Y axis.
 Left/Right speed is determined by the horizontal X axis. 

 ==========================================================================================
	
