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
import math

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

device_data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00]

def Device_Setup(MY_DEVICE_ADDRESS):
    # Set up the device by writing 0x70 to Register 0
    # 0x20 to Register 1 (which corresponds to gauss of 1090)
    # and 0x00 to Register 2 (for continuous measurement)
    #try
    bus.write_byte_data(MY_DEVICE_ADDRESS, DEVICE_REG0, 0x70)
    bus.write_byte_data(MY_DEVICE_ADDRESS, DEVICE_REG1, 0x20)
    bus.write_byte_data(MY_DEVICE_ADDRESS, DEVICE_REG2, 0x00)

# End of Device_Setup
    
def MyReadData(MY_DEVICE_ADDRESS, Debugmode):
    # this is my function to read only 8 bytes of data returned over I2C
    # instead of reading 256 bytes!
    # and is equivalent to read_i2c_block_data
    # Returns a list of 8 bytes

    # First send a byte of data to request the information

    #Extract 6 bytes from the fourth byte
    device_text = ''
    for i in range(0,5):
        device_data[i] = bus.read_byte_data(MY_DEVICE_ADDRESS, i+3) 
        device_text = device_text + ("%02x" % device_data[i])
    #next i

    # Print the output to screen if Debugmode set to True
    if (Debugmode == True):
        print "Device type = ", device_text
    #endif
        
    return device_data

# End of MyReadData

def Sensor_value(m_value):
    # if the value is above 10000000 00000000, then it is negative 
    if m_value > (128 * 256):
        m_value = -((65535 - m_value) + 1)
    return m_value


def Bearing_Value(MY_DATA, Debugmode):
    # this is my function to calculate the value of each axis
    # Axis 0 = X  (byte 3)
    # Axis 1 = Z  (byte 5)
    # Axis 2 = Y  (byte 7)
    x_axis = Sensor_value(MY_DATA[3] * 256 + MY_DATA[4])
    y_axis = Sensor_value(MY_DATA[7] * 256 + MY_DATA[8])

    if (Debugmode == True):
        print "x: ", x_axis, "y: ", y_axis
    #endif
    
    bearing = math.atan2(y_axis,x_axis)
    if (bearing < 0):
        bearing = bearing + 2 * math.pi
    #endif

    angle = math.degrees(bearing)

    return angle



Device_Setup(DEVICE_ADDRESS)
while True:
    short_data = MyReadData(DEVICE_ADDRESS, True)
    mybearing = Bearing_Value(short_data, False)
    print "Bearing: ", mybearing
    
