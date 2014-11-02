#!/usr/bin/python
#
# Raspberry Pi Magnetometer
#   by Andrew Hammacott
#
# This is built for Python 2
#
# HOW TO GET STARTED
# 1. Activate I2C on the Raspberry Pi
#    I followed the Adafruit instructions here:
#    https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
#
#    but there are also instructions here:
#    http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/io-pins-raspbian/i2c-pins
#
#    I2C works using 4 connections:
#      Positive voltage (3v3 which means 3.3 volts - in electronics, decimal points are avoided)
#      Data channel #1 - SDA
#      Data channel #2 - SCL
#      Ground (GND or 0v)
#
#    This is not the place for a wiring diagram!  So you will need to google to find out how to connect 4 leads to the headers 
#
# The device has an I2C "location" of 0x1e
#
# This can be checked by running in the LXTerminal window (or command prompt if not using X):
#    sudo i2cdetect -y 1
# NOTE: if you have an early Raspberry Pi (like I do), the I2C was setup differently to use 0
# i.e. the command becomes:   sudo i2cdetect -y 0
#
# If connected, you will see a grid with "1e" mentioned in the middle
#

import smbus

# The interface is numbered differently depending on the Raspberry Pi model
# We can check this from getting the revision number available in the GPIO library
import RPi.GPIO as GPIO
version = GPIO.RPI_REVISION
if version == 1: 
    RPI_VERSION = 0
else:
	RPI_VERSION = 1

# 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
bus = smbus.SMBus(RPI_VERSION)

import time
SLEEP_TIME = 0.02

# Set up device
DEVICE_ADDRESS = 0x1e      #7 bit address (will be left shifted to add the read write bit)
DEVICE_REG0 = 0x00
DEVICE_REG1 = 0x01
DEVICE_REG2 = 0x02

def Device_Setup():
    # Set up the device by writing 0x70 to Register 0
	# 0x20 to Register 1 (which corresponds to gauss of 1090)
	# and 0x00 to Register 2 (for continuous measurement)
    #try
    bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG1, 0x70)
    bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG1, 0x20)
	bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG2, 0x00)

# End of Device_Setup
    
def MyReadData(MY_DEVICE_ADDRESS, MY_DEVICE_REG, Debugmode):
    # this is my function to read only 8 bytes of data returned over I2C
    # instead of reading 256 bytes!
    # and is equivalent to read_i2c_block_data
    # Returns a list of 8 bytes

    # First send a byte of data to request the information

    full_data = bus.read_i2c_block_data(MY_DEVICE_ADDRESS, MY_DEVICE_REG) 

    #Extract first 8 bytes
    device_text = ''
    for i in range(0,7):
        device_data[i] = full_data[i]
        device_text = device_text + ("%02x" % full_data[i])
    #next i

    # Print the output to screen if Debugmode set to True
    if (Debugmode == True):
        print "Device type = ", device_text
    #endif
        
    return device_data

# End of MyReadData

def Magnet_Value(MY_DATA, MY_AXIS):
    # this is my function to calculate the value of each axis
	# Axis 0 = X  (byte 3)
	# Axis 1 = Z  (byte 5)
	# Axis 2 = Y  (byte 7)
	m_axis = MY_AXIS * 2 + 1
	# the value is stored as a binary number 00000000 00000000 over two bytes
	m_value = MY_DATA[m_axis] * 256 + MY_DATA[m_axis + 1]
    # if the value is above 10000000 00000000, then it is negative 
	if m_value > (128 * 256):
	    m_value = (128 * 256) - m_value
	return m_value
