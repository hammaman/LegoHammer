# ---- WORKSHEET 1 LINE DETECTOR ----

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

# Define GPIO pins to use on the Pi
GPIO_DETECTLFT = 25
GPIO_DETECTMID = 7
GPIO_DETECTRGH = 8

print "Line detection"

# Set pin as input
GPIO.setup(GPIO_DETECTLFT, GPIO.IN)
GPIO.setup(GPIO_DETECTMID, GPIO.IN)
GPIO.setup(GPIO_DETECTRGH, GPIO.IN)


try:
    # Repeat the next indented block forever
    while True:

        # If the sensor is HIGH (=1), the surface is detected as black
        if GPIO.input(GPIO_DETECTMID) == 1:
            print "MID: Detecting a black surface"
        
        # If not, the surface is detected as white
        else:
            print "MID: Detecting a white surface"

        # If the sensor is HIGH (=1), the surface is detected as black
        if GPIO.input(GPIO_DETECTLFT) == 1:
            print "LEFT: Detecting a black surface"
        
        # If not, the surface is detected as white
        else:
            print "LEFT: Detecting a white surface"

        # If the sensor is HIGH (=1), the surface is detected as black
        if GPIO.input(GPIO_DETECTRGH) == 1:
            print "RIGHT: Detecting a black surface"
        
        # If not, the surface is detected as white
        else:
            print "RIGHT: Detecting a white surface"
            
        # Wait a second, then do the same again
        time.sleep(1)
    
# If you press Ctrl-C, this will generate a keyboard interrupt
# and if so, clean up and stop
except KeyboardInterrupt:

    # Reset GPIO settings
    GPIO.cleanup()

# ---- END OF CODE ----
