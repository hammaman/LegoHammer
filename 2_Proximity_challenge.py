# ---- CODE FOR PIWARS CHALLENGES ----
#
# Proximity challenge
#
# Purpose of this Python (version 2) program:
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
#    sudo python 2_Proximity_challenge.py
# (assuming the code is stored in the current directory)


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
GPIO_TRIGGER = 11
GPIO_ECHO = 9

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Set the stop distance in cm
#   - we have set this by measuring the distance from the sensor to the front of the car
#     and added on a margin to reflect that we are using a moving average of three readings
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
    time.sleep(0.1)

    # Move forward
    MoveForward()

    # You seem to need to wait slightly after stopping
    # for electronics to settle and for car to stop moving
    time.sleep(0.1)

    # Repeat until the average distance is below our trigger point to stop
    while (rolling_average > STOP_DISTANCE):
        
        # Set trigger to False
        GPIO.output(GPIO_TRIGGER, False)
        time.sleep(0.1)
        
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
        print "Distance ", distance

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
    
# ---- END OF CODE ----