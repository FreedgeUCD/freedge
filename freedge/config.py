# #######################
# Hardware Configuration
# #######################
# The below config shows how each sensor is connected to the Rasp Pi 3.

# ########################
# Door Sensor
# ########################
# Also, the ground (BLACK) wire is connected to PIN 4.
PIN_GPIO_DOOR_RED = 14  # in BCM Mode
PIN_GPIO_DOOR_BLACK = 4

# Weather sensor (AM2315) uses I2C protocol, 
# we follow this tutorial to determine the  address mapping on Linux: 
# [1] https://shop.switchdoc.com/products/am2315-encased-i2c-temperature-humidity-sensor-for-raspberry-pi-arduino
I2C_AM2315_ADDRESS = 0x5c

# Reference:
# ---------
# Rasp Pi 3B GPIO Pinout:
# Ref: http://pi4j.com/pins/model-3b-rev1.html