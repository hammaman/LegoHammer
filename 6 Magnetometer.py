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
DEVICE_REG1 = 0xF0
DEVICE_REG2 = 0xFB
DEVICE_REGTYPE = 0xFA
full_data = [0,0,0,0,0,0,0]
device_data = [0, 0, 0, 0, 0, 0]
device_text = '000000000000'


# To initialise each device:
# you must first write 0x55 to 0x(4)a400f0 (for the Pi, this is just 0xf0),
# then 0 to 0x(4)a400fb (0xfb)
#
def Device_Setup():
    # Set up the device by writing 0x55 to Register 1 and 0x00 to Register 2
    #try
    bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG1, 0x55)
    bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG2, 0x00)

# End of Device_Setup
    
def Get_Device_Connected():
    # Determine the device connected - by sending a byte to Register REGTYPE
    # and look at the 6 bytes of data returned
    
    bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REGTYPE, 0x00)
    time.sleep(SLEEP_TIME)
    full_data = bus.read_i2c_block_data(DEVICE_ADDRESS, DEVICE_REGTYPE) 

    #Extract first 6 bytes and store as a string in hex format
    device_text = ''
    for i in range(0,6):
        device_text = device_text + ("%02x" % full_data[i])
    #next i

    if device_text == '0000a4200103':
        device_connected = 'Guitar'
    elif device_text == '0100a4200103':
        device_connected = 'Drums'
    else:
        device_connected = 'Unknown'
    #end if

    return device_connected

#End of Get_Device_Connected

def MyReadData(MY_DEVICE_ADDRESS, MY_DEVICE_REG, Debugmode):
    # this is my function to read only 6 bytes of data returned over I2C
    # instead of reading 256 bytes!
    # and is equivalent to read_i2c_block_data
    # Returns a list of 6 bytes

    # First send a byte of data to request the information

    bus.write_byte_data(MY_DEVICE_ADDRESS, MY_DEVICE_REG, 0x00)
    time.sleep(SLEEP_TIME)
    full_data = bus.read_i2c_block_data(MY_DEVICE_ADDRESS, MY_DEVICE_REG) 

    #Extract first 6 bytes
    device_text = ''
    for i in range(0,6):
        device_data[i] = full_data[i]
        device_text = device_text + ("%02x" % full_data[i])
    #next i

    # Print the output to screen if Debugmode set to True
    if (Debugmode == True):
        print "Device type = ", device_text
    #endif
        
    return device_data

# End of MyReadData
