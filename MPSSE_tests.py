# -*- coding: utf-8 -*-
"""MPSSE_tests.py: Simple test routine for pyMPSSE wrapper functions

__author__ = "Jason M. Battle"
"""

from MPSSE import I2CMaster
                                 
if __name__ == "__main__": 
    
    test = I2CMaster()
    test.Init_libMPSSE() # Graceful initialization
    test.GetNumChannels()
    test.GetChannelInfo() # Channel index starts at 0
    test.OpenChannel() # Assign handle to channel 0
    test.InitChannel('Standard') # Configure I2C port in 100kHz mode
    test.DeviceWrite(0x71, 0x00, []) # Write register address 0x00 to device address 0x71 (R/W bit is omitted!)
    i2cdat = test.DeviceRead(0x71, 0x07, 2) # Read two bytes from register address 0x07 (device address 0x71)
    test.WriteGPIO(255, 0) # Set all GPIO pins to drive low
    gpiodatlo = test.ReadGPIO()
    test.WriteGPIO(255, 255) # Set all GPIO pins to drive high
    gpiodathi = test.ReadGPIO()
    test.CloseChannel() # Free channel at specified handle 
    test.Cleanup_libMPSSE() # Graceful exit
    
