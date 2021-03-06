# ---- CODE FOR PIWARS CHALLENGES ----
#
# Three Point Turn Challenge
#
# Purpose of this Python (version 2) program:
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
#    sudo python 1_Line_Sensors_challenge.py
# (assuming the code is stored in the current directory)

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
GPIO_DETECTMID = 8
GPIO_DETECTRGT = 7

# Set pin as input
GPIO.setup(GPIO_DETECTLFT, GPIO.IN)
GPIO.setup(GPIO_DETECTMID, GPIO.IN)
GPIO.setup(GPIO_DETECTRGT, GPIO.IN)

# ---- SET UP THE MOTOR CONTROLLER BOARD

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

def TurnLeft():
    GPIO.output(pinLeftForward,1)
    GPIO.output(pinLeftBackward,0)
    GPIO.output(pinRightForward,0)
    GPIO.output(pinRightBackward,1)
    time.sleep(0.01)
    AllStop()

def TurnRight():
    GPIO.output(pinLeftForward,0)
    GPIO.output(pinLeftBackward,1)
    GPIO.output(pinRightForward,1)
    GPIO.output(pinRightBackward,0)
    time.sleep(0.01)
    AllStop()

TIME_10_MILLISECS = 0.01    
    
try:

    # Check that the middle sensor is detecting black
    while GPIO.input(GPIO_DETECTMID) == 0:
        print "Not detecting black - reposition the car"
    time.sleep(2)
    print "Starting challenge"
    
    # Repeat the next indented block forever
    while True:

        MoveForward()
        print "Moving forward"

        # Monitor sensors as the car moves forward for 10 milliseconds
        current_time = time.time()
        while (time.time() < current_time + TIME_10_MILLISECS):
            #Sensormonitoring
            if GPIO.input(GPIO_DETECTLFT) == 1:
                 lasttimeleft = time.time()
            if GPIO.input(GPIO_DETECTRGT) == 1:
                 lasttimeright = time.time()            
        
        AllStop()
        
        # If the sensor is HIGH (=1), the surface is detected as black
        if GPIO.input(GPIO_DETECTMID) == 0:
            print "Not detecting a black surface"
            if GPIO.input(GPIO_DETECTLFT) == 1:
                 print "LEFT: Detecting a black surface"
                 while GPIO.input(GPIO_DETECTMID) == 0:
                     TurnLeft()
                 print "Now back on track"

            elif GPIO.input(GPIO_DETECTRGT) == 1:
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
