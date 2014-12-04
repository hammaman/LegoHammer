# ---- CODE FOR PIWARS CHALLENGES ----
#
# Three Point Turn Challenge
#
# Purpose of this Python (version 2) program:
# To move the robot on its own around the course.
#
# To do this, the robot needs to:
#
#  Move forwards for 150cm
#  Turn left 90 degrees
#  Move forwards for 70cm
#  Turn left 180 degrees
#  Move forwards for 140cm
#  Turn left 180 degrees
#  Move forwards for 70cm
#  Turn left 90 degrees
#  Move forwards for 150cm (back to start)
#
#  (These measurements are derived from the course specification)
#
# Hardware required:
#   Raspberry Pi (any model)
#   Ryanteck motor controller board
#    ...  connected to two motors which control two wheels on the robot
#
# You will also need to connect to the Pi remotely to run this code
# as the robot will start moving as soon as this code is run
# and you don't want it connected to things if this happens!
#
# We have added a Wifi USB dongle to the Pi
# and connected the Pi to a Wifi network
# We have enabled SSH in the advanced menu of raspi-config
# (please refer to raspberrypi.org for fuller instructions) 
# and connected using a Windows laptop running Putty
# Once logged in, the command to run this code is:
#    sudo python 4_Three_point_turn.py
# (assuming the code is stored in the current directory)

# Implementation:
#
#  Initially, we intended to use a sensor to detect the
#  direction that the robot was facing.  This would then keep it
#  on track as it did the challenge.
#
#  However, we had difficulties with the magnetometer to send direction
#  and we found the Lego motors to be very well matched, so that the robot
#  moved in a reasonably straight line. So the need to get the magnetometer
#  to work was reduced, and we just decided to use an approach to move
#  the motors in a predefined way and hope that the robot's course was
#  close to that required 
#
#  So the code does not involve any detection of position
#
#  Instead, we are relying on a measurement of the time
#  it takes to move 1 meter:
#      TIME_TO_COVER_1M in milliseconds
#
#  and the time it takes to rotate 360 degrees
#      TIME_TO_ROTATE_360DEG in milliseconds
#
#  These are determined by timing the robot and entering the values below
#  We recognise that this depends on the surface that the robot is on
#  but this cannot be factored in before the event!

TIME_TO_COVER_1M = 5.8
TIME_TO_ROTATE_360DEG = 3.5

# ---- START OF PYTHON CODE ----

# Import required Python libraries

# Import the time module so that we can make our program wait
# for a length of time
import time

# Import the GPIO module so that we can control the GPIO pins
# and refer to it as GPIO for the rest of the code
import RPi.GPIO as GPIO

# Use physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# This code also uses the Ryanteck motor controller board
# (c) Ryanteck LTD 2014

# Assign pins on the Ryanteck board

pinLeftForward = 18
pinLeftBackward = 17
pinRightForward = 23
pinRightBackward = 22

# Set up GPIO pins ready for use as outputs
GPIO.setup(pinLeftForward, GPIO.OUT)
GPIO.setup(pinLeftBackward, GPIO.OUT)
GPIO.setup(pinRightForward, GPIO.OUT)
GPIO.setup(pinRightBackward, GPIO.OUT)

# Define some functions so that we can control the motors
# and move the robot
# The functions should be self-explanatory
#
# NOTE: once the function has been called, the robot will continue
#       to do the action until another function call is made
#       So to move forward for a certain time, we can call the MoveForward
#       function and then ask the Pi to wait for a certain time

def MoveForward():
    GPIO.output(pinLeftForward,1)
    GPIO.output(pinLeftBackward,0)
    GPIO.output(pinRightForward,1)
    GPIO.output(pinRightBackward,0)

def Reverse():
    GPIO.output(pinLeftForward,0)
    GPIO.output(pinLeftBackward,1)
    GPIO.output(pinRightForward,0)
    GPIO.output(pinRightBackward,1)

def AllStop():
    GPIO.output(pinLeftForward,0)
    GPIO.output(pinLeftBackward,0)
    GPIO.output(pinRightForward,0)
    GPIO.output(pinRightBackward,0)

def MoveLeft():
    GPIO.output(pinLeftForward,1)
    GPIO.output(pinLeftBackward,0)
    GPIO.output(pinRightForward,0)
    GPIO.output(pinRightBackward,1)

def MoveRight():
    GPIO.output(pinLeftForward,0)
    GPIO.output(pinLeftBackward,1)
    GPIO.output(pinRightForward,1)
    GPIO.output(pinRightBackward,0)

# The following function stops the robot and waits for a second
# and is used between steps
def Pause():
    AllStop()
    time.sleep(0.5)
    
# To recap, the robot needs to do the following things
#
#  React to a start command
#
#  Move forwards for 150cm
#  Turn left 90 degrees
#  Move forwards for 70cm
#  Turn left 180 degrees
#  Move forwards for 140cm
#  Turn left 180 degrees
#  Move forwards for 70cm
#  Turn left 90 degrees
#  Move forwards for 150cm (back to start)
#
#  The python code to do this is as follows:

#  We "try" the code in case it is cancelled by Ctrl-C
#  and if it is cancelled by Ctrl-C, there is cleanup of the GPIO pins
#  which stops the robot continuing what it was doing

try:

    time.sleep(1)
    print "Starting challenge"


    #  Move forwards for 150cm
    print "Moving forwards 150cm"
    MoveForward()
    time.sleep(TIME_TO_COVER_1M * 150 / 100)

    Pause()

    #  Turn left 90 degrees
    print "Turning left 90 degrees"
    MoveLeft()
    time.sleep(TIME_TO_ROTATE_360DEG * 90 / 360)

    Pause()

    #  Move forwards for 70cm
    print "Moving forwards 70cm"
    MoveForward()
    time.sleep(TIME_TO_COVER_1M * 70 / 100)

    Pause()

    #  Turn left 180 degrees
    print "Turn left 180 degrees"
    MoveLeft()
    time.sleep(TIME_TO_ROTATE_360DEG * 180 / 360)

    Pause()

    #  Move forwards for 140cm
    print "Move forward 140cm"
    MoveForward()
    time.sleep(TIME_TO_COVER_1M * 140 / 100)

    Pause()

    #  Turn left 180 degrees
    print "Turn left 180 degrees"
    MoveLeft()
    time.sleep(TIME_TO_ROTATE_360DEG * 180 / 360)

    Pause()

    #  Move forwards for 70cm
    print "Move forward 70cm"
    MoveForward()
    time.sleep(TIME_TO_COVER_1M * 70 / 100)

    Pause()

    #  Turn left 90 degrees
    print "Turn left 90 degrees"
    MoveLeft()
    time.sleep(TIME_TO_ROTATE_360DEG * 90 / 360)

    Pause()

    #  Move forwards for 150cm (back to start)
    print "Moving forward 150cm back to start"
    MoveForward()
    time.sleep(TIME_TO_COVER_1M * 150 / 100)

    #  We've finished the challenge!
    AllStop()
    print "Challenge completed!"

# Clean up if Ctrl-C is pressed
except KeyboardInterrupt:

    #Reset GPIO settings
    GPIO.cleanup()

# ---- END OF CODE ----

