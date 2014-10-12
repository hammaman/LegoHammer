# From http://think-bowl.com/raspberry-pi/i2c-python-library-3-axis-digital-compass-hmc5883l-with-the-raspberry-pi/

from i2clibraries import i2c_hmc5883l
 
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(0)
 
hmc5883l.setContinuousMode()
hmc5883l.setDeclination(9,54)
 
# To get degrees and minutes into variables
(degrees, minutes) = hmc5883l.getDeclination()
(degress, minutes) = hmc5883l.getHeading()
 
# To get string of degrees and minutes
declination = hmc5883l.getDeclinationString()
heading = hmc5883l.getHeadingString()