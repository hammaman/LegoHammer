# This Python code requires the Cwiid module which is not part
# of the standard Raspian build.  You will need to install this
# by running the following command from the LXTerminal:
#    apt-get install python-cwiid

# To connect to a Wiimote, you will also need a bluetooth adapter
# which has been set up and installed, by running the following
# commands from the LXTerminal:
#
#   TO FOLLOW
#
#

import cwiid

# Define buttons for forwards back, left and right
# and for safety, an emergency stop.

btnForward = cwiid.BTN_A     # forward is button A
btnReverse = cwiid.BTN_B     # reverse is button B
btnLeft    = cwiid.BTN_1     # left is button 1
btnRight   = cwiid.BTN_2     # right is button 2
btnStop    = cwiid.BTN_DOWN  # stop is down or (when held horisontaly) right

# This code also uses the Ryanteck motor controller board
# (c) Ryanteck LTD 2014

import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)      # Ignore any errors

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


# This code is to set up the connection to the Wiimote.
# This allows several attempts as first few often fail.
# So we use a loop which tries to connect,and for which
# we catch the error if the connection is unsuccessful
# which is a Runtime error from the command cwiid.Wiimote()

import time

print 'Press 1+2 on your Wiimote now...'
wm = None
intNumTries = 1
while not wm:
    try:
        wm = cwiid.Wiimote()
    except RuntimeError:
        if (intNumTries<10):
            print "Error opening wiimote connection"
            print "attempt " + str(intNumTries)
            time.sleep(0.1) #wait 0.1 seconds
            intNumTries +=1
        else:
            print("cannot create connection")
            quit()

#End of loop to try and connect to a Wiimote            

# Set up the Wiimote
# (1) to report button presses and accelerometer state
# [the AND operator is the vertical line character by pressing Shift+\]+

wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

# (2) turn on led to show connected
wm.led = 1

# ----------------------------------------------------------
# Checking Wiimote button presses

while True:
    try:
        buttons = wm.state['buttons']
        if (buttons & btnForward):
            #Forward
            print "forward"
            MoveForward()
        if (buttons & btnReverse):
            #Reverse
            print "reverse"
            Reverse()
        if (buttons & btnLeft):
            #Left
            print "left"
            MoveLeft()
        if (buttons & btnRight):
            #Right
            print "right"
            MoveRight()
        if (buttons & btnStop):
            #Stop
            print "Emergency stop"
            wm.rumble = 1 #Rumble the wiimote
            AllStop()
        
        time.sleep(0.2)
        wm.rumble = 0 #Turn off rumble

    except RuntimeError:
        AllStop()
    
