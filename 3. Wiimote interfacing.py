# This Python code requires the Cwiid module which is not part
# of the standard Raspian build.  You will need to install this
# by running the following command from the LXTerminal:
#    apt-get cwiid ?????

# To connect to a Wiimote, you will also need a bluetooth adapter
# which has been set up and installed, by running the following
# commands from the LXTerminal:
#
#   TO FOLLOW
#
#

import cwiid
import time

# This code is to set up the connection to the Wiimote.
# This allows several attempts as first few often fail.
# So we use a loop which tries to connect,and for which
# we catch the error if the connection is unsuccessful
# which is a Runtime error from the command cwiid.Wiimote()

print 'Press 1+2 on your Wiimote now...'
wm = None
intNumTries = 1
while not wm:
	try:
		wm = cwiid.Wiimote()
	except RuntimeError:
		if (i<10):
			print "Error opening wiimote connection"
			print "attempt " + str(i)
			wait(10) #wait 0.1 seconds
			i +=1
		else:
			print("cannot create connection")
			quit()

#End of loop to try and connect to a Wiimote			

# Set up the Wiimote
# (1) to report button presses and accelerometer state
# [the AND operator is the vertical line character by pressing Shift+\]
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

# (2) turn on led to show connected
wm.led = 1

# ----------------------------------------------------------
# Checking Wiimote button presses

while True:
	buttons = wm.state['buttons']
	if (buttons & cwiid.BTN_B):
		# Pressed button B
	if (buttons & cwiid.BTN_2):
		# Pressed button 2
	if (buttons & cwiid.BTN_1):
		# Pressed button 1
	time.sleep(0.2)