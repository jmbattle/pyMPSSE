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
    test.Init_libMPSSE()
    test.GetNumChannels()
    test.GetChannelInfo(0) # Channel index starts at 0
    handle = test.OpenChannel(0) # Assign handle to channel 0
    test.InitChannel(handle, mode='Standard') # Configure I2C port in 100kHz mode
    test.DeviceWrite(handle, 0x71, 0x00, []) # Write register address 0x00 to device address 0x71 (R/W bitis omitted!)
    test.DeviceRead(handle, 0x71, 0x07, [], 2) # Read two bytes from register address 0x07 (device address 0x71)
    #test.FT_WriteGPIO(handle, 255, 0)
    #test.FT_ReadGPIO(handle)
    test.CloseChannel(handle) # Free channel at specified handle 
    test.Cleanup_libMPSSE() # Graceful exit