# -*- coding: utf-8 -*-
"""MPSSE.py: A python wrapper for the FTDI-provided libMPSSE DLL (I2C only)

__author__ = "Jason M. Battle"
__copyright__ = "Copyright 2016, Jason M. Battle"
__license__ = "MIT"
__email__ = "jason.battle@gmail.com"
"""

from MPSSE import I2CMaster
                                 
if __name__ == "__main__": 
    
    test = I2CMaster()
    test.Init_libMPSSE() # Graceful initialization
    numchan = test.GetNumChannels()
    chaninfo = test.GetChannelInfo(0) # Channel index starts at 0
    handle = test.OpenChannel(0) # Assign handle to channel 0
    test.InitChannel(handle, mode='Standard') # Configure I2C port in 100kHz mode
    test.DeviceWrite(handle, 0x71, 0x00, []) # Write register address 0x00 to device address 0x71 (R/W bit is omitted!)
    i2cdat = test.DeviceRead(handle, 0x71, 0x07, [], 2) # Read two bytes from register address 0x07 (device address 0x71)
    test.WriteGPIO(handle, 255, 0) # Set all GPIO pins to drive low
    gpiodatlo = test.ReadGPIO(handle)
    test.WriteGPIO(handle, 255, 255) # Set all GPIO pins to drive high
    gpiodathi = test.ReadGPIO(handle)
    test.CloseChannel(handle) # Free channel at specified handle 
    test.Cleanup_libMPSSE() # Graceful exit
    
