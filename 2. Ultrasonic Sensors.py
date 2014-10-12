# ---- WORKSHEET 2 ULTRASONIC DISTANCE MEASUREMENT ----

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
GPIO_TRIGGER = 17
GPIO_ECHO = 18

print "Ultrasonic measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

try:
    # Repeat the next indented block forever
    while True:
	    # Set trigger to False
		GPIO.output(GPIO_TRIGGER, False)
		
		# Allow module to settle
		time.sleep(0.5)
		
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
		
		print "Distance : %.lf" % distance
		
# If you press Ctrl-C, this will generate a keyboard interrupt
# and if so, clean up and stop
except KeyboardInterrupt:

    # Reset GPIO settings
    GPIO.cleanup()

