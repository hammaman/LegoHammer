# ---- CODE FOR PIWARS CHALLENGES ----
#
# Proximity challenge
#
# Purpose of the program:
# To move the robot towards a wall, and for it to stop before it reaches it.
#
# To do this, the robot needs to:
#
#  React to a start command (running this program)
#  Move forward
#  Stop when gets close to the wall
#
# Hardware required:
#   Raspberry Pi (any model)
#   Ryanteck motor controller board
#    ...  connected to two motors which control two wheels on the robot
#   Ultrasonic sensor

# Implementation:
#
#  We are assuming that the robot starts pointing at the wall
#  and so we can just set it moving forward 
#
#  We will use a loop to constantly monitor the distance
#  and take the average of three measurements to the wall
#  When this falls below a certain amount, the STOP_DISTANCE,
#  we will stop the robot
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
# NOTE: all the functions move the robot slightly and then stop the robot

def MoveForward():
    GPIO.output(pinLeftForward,1)
    GPIO.output(pinLeftBackward,0)
    GPIO.output(pinRightForward,1)
    GPIO.output(pinRightBackward,0)


def AllStop():
    GPIO.output(pinLeftForward,0)
    GPIO.output(pinLeftBackward,0)
    GPIO.output(pinRightForward,0)
    GPIO.output(pinRightBackward,0)

# Define GPIO pins for the ultrasonic sensor
GPIO_TRIGGER = 17
GPIO_ECHO = 18

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Set the stop distance in cm
STOP_DISTANCE = 15

# Set up variables to record the distance
current_distance = 1000
last_distance = 1000
prev_distance = 1000
rolling_average = 1000

try:

    # Set up the sensor
    GPIO.output(GPIO_TRIGGER, False)
        
    # Allow module to settle
    time.sleep(0.5)

    #Move forward
    MoveForward()

    # Repeat until the average distance is below our trigger point to stop
    while (rolling_average > STOP_DISTANCE):
        # Set trigger to False
        
        # Send 10ms pulse to trigger
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        
        start = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()
            
        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()
            
        # Calculate pulse length
        elapsed = stop - start
        
        # Distance pulse travelled in that time is
        # time multiplied by the speed of sound
        # which is 34326 cm/s
        # but distance is there and back,
        # so distance to object is distance travelled divided by 2
        
        distance = elapsed * 34326.0 / 2.0
        
        #Calculate the rolling average
        prev_distance = last_distance
        last_distance = current_distance
        current_distance = distance
        
        rolling_average = (prev_distance + last_distance + current_distance) / 3

    #This code happens when the STOP_DISTANCE is reached
    AllStop()
    print "Stopped"
        
# If you press Ctrl-C, this will generate a keyboard interrupt
# and if so, clean up and stop
except KeyboardInterrupt:

    # Reset GPIO settings
    GPIO.cleanup()

