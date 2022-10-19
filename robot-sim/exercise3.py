from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

We start from the solution of the exercise 2
Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py exercise3.py

"""


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token(color):
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    if(color == "silver"):
        m = MARKER_TOKEN_SILVER
    elif(color == "gold"):
        m = MARKER_TOKEN_GOLD

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type == m:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	    return -1, -1
    else:
   	    return dist, rot_y


token_to_find = "silver"

while(1):
    print("Looking for a", token_to_find, "token...\n")
    dist, rot_y = find_token(token_to_find)

    if(dist == -1 or rot_y == -1):
        turn(20,0.001)

    elif(dist <= d_th):
        R.grab()
        turn(10, 4)
        drive(20, 2)
        R.release()
        drive(-20, 2)
        turn(-10, 4)

        if(token_to_find == "silver"):
            token_to_find = "gold"
        else:
            token_to_find = "silver"

    elif(rot_y <= a_th and rot_y >= -a_th):
        velocity = dist*25 #Proportional velocity to the distance
        drive(velocity,0.1)
    
    elif(rot_y > a_th or rot_y < -a_th):
        sign = a_th/abs(a_th)
        turn(sign*5, 0.001)
