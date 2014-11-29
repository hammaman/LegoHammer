# ---- CODE FOR PIWARS CHALLENGES ----
#
# Three Point Turn Challenge
#
# Purpose of the program:
# To move the robot on its own around the course, following a black line.
#
# To do this, the robot needs to:
#
#  React to a start command
#  Follow the black line (and keep doing that until the course is completed)
#
# Hardware required:
#   Raspberry Pi (any model)
#   Ryanteck motor controller board
#    ...  connected to two motors which control two wheels on the robot
#   Three line sensors (each connected to GND, 3.3V and a GPIO pin)

# Implementation:
#
#  We are assuming that the robot starts with middle sensor on black line
#    (we can check this by looking at the middle LED and checking it is not lit) 
#
#  We will use a loop to constantly monitor the line
#
#    Move forwards a little
#    Keep track of last time that each sensor last detected black
#    Check sensors:
#      If middle sensor is detecting black, loop round to start of main loop
#      If middle sensor is detecting white, then:
#          stop
#          determine which direction to turn:
#              if any sensors detecting black, turn in this direction
#              if no sensors detecting black, determine which sensor last detected black and turn in this direction
#                 and move in that direction until middle sensor detects black
#
#
#  The code is adapted from that provided at a CamJam workshop

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

# ---- SET UP THE LINE SENSORS

# Define GPIO pins to use on the Pi for the line sensors
GPIO_DETECTLFT = 25
GPIO_DETECTMID = 7
GPIO_DETECTRGH = 8

# Set pin as input
GPIO.setup(GPIO_DETECTLFT, GPIO.IN)
GPIO.setup(GPIO_DETECTMID, GPIO.IN)
GPIO.setup(GPIO_DETECTRGH, GPIO.IN)

# ---- SET UP THE MOTOR CONTROLLER BOARD

# This code also uses the Ryanteck motor controller board
# (c) Ryanteck LTD 2014

# Assign pins on the Ryanteck board
pinLeftForward = 17
pinLeftBackward = 18
pinRightForward = 22
pinRightBackward = 23

# Set up GPIO pins ready for use as outputs
GPIO.setup(pinLeftForward, GPIO.OUT)
GPIO.setup(pinLeftBackward, GPIO.OUT)
GPIO.setup(pinRightForward, GPIO.OUT)
GPIO.setup(pinRightBackward, GPIO.OUT)

# Define some functions so that we can control the motors
# and move the robot
# The functions should be self-explanatory
#

def AllStop():
    GPIO.output(pinLeftForward,0)
    GPIO.output(pinLeftBackward,0)
    GPIO.output(pinRightForward,0)
    GPIO.output(pinRightBackward,0)

def MoveForward():
    GPIO.output(pinLeftForward,1)
    GPIO.output(pinLeftBackward,0)
    GPIO.output(pinRightForward,1)
    GPIO.output(pinRightBackward,0)

def MoveLeft():
    GPIO.output(pinLeftForward,1)
    GPIO.output(pinLeftBackward,0)
    GPIO.output(pinRightForward,0)
    GPIO.output(pinRightBackward,1)
    sleep(0.01)
    AllStop()

def MoveRight():
    GPIO.output(pinLeftForward,0)
    GPIO.output(pinLeftBackward,1)
    GPIO.output(pinRightForward,1)
    GPIO.output(pinRightBackward,0)
    sleep(0.01)
    AllStop()

TIME_10_MILLISECS = 10    
    
try:

    # Check that the middle sensor is detecting black
    while GPIO.input(GPIO_DETECTMID) == 0:
        print "Not detecting black - reposition the car"
    sleep(2)
    print "Starting challenge"
    
    # Repeat the next indented block forever
    while True:

        MoveForward()
        # Monitor sensors as the car moves forward for 10 milliseconds
        current_time = time()
        while (time() < current_time + TIME_10_MILLISECS):
            #Sensormonitoring
            if GPIO.input(GPIO_DETECTLFT) == 1:
                 lasttimeleft = time()
            if GPIO.input(GPIO_DETECTRGT) == 1:
                 lasttimeright = time()            
        
        AllStop()
        
        # If the sensor is HIGH (=1), the surface is detected as black
        if GPIO.input(GPIO_DETECTMID) == 0:
            print "Not detecting a black surface"
            if GPIO.input(GPIO_DETECTLFT) == 1:
                 print "LEFT: Detecting a black surface"
                 while GPIO.input(GPIO_DETECTMID) == 0:
                     TurnLeft()
                 print "Now back on track"

            elif GPIO.input(GPIO_DETECTRGH) == 1:
                 print "RIGHT: Detecting a black surface"
                 while GPIO.input(GPIO_DETECTMID) == 0:
                     TurnRight()
                 print "Now back on track"
        
            # If not, the surface is detected as white
            else:
                 print "Detecting last reading"
                 if lasttimeleft > lasttimeright:
                     while GPIO.input(GPIO_DETECTMID) == 0:
                         TurnLeft()
                     print "Now back on track"
                 else:
                     while GPIO.input(GPIO_DETECTMID) == 0:
                         TurnRight()
                     print "Now back on track"
        
        # Wait a second, then do the same again
        time.sleep(0.1)
    
# If you press Ctrl-C, this will generate a keyboard interrupt
# and if so, clean up and stop
except KeyboardInterrupt:

    # Reset GPIO settings
    GPIO.cleanup()

# ---- END OF CODE ----
