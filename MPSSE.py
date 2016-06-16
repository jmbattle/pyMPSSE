# -*- coding: utf-8 -*-
"""MPSSE.py: A python wrapper for the FTDI-provided libMPSSE DLL (I2C only)

__author__ = "Jason M. Battle"
__copyright__ = "Copyright 2016, Jason M. Battle"
__license__ = "MIT"
__email__ = "jason.battle@gmail.com"
"""

import ctypes
from collections import OrderedDict

dll_loc = r'C:\Python27\Lib\site-packages\libMPSSE.dll'

try:
    dll = ctypes.CDLL(dll_loc)
except:
    print '%s not found' % dll_loc.split('\\')[-1]
        
#####GLOBALS###################################################################

 # Clock Rate Defines
I2C_CLOCK_STANDARD_MODE = 100000 # 1kHz Mode
I2C_CLOCK_FAST_MODE = 400000 # 4000kHz Mode
I2C_CLOCK_FAST_MODE_PLUS = 1000000 # 1MHz Mode
I2C_CLOCK_HIGH_SPEED_MODE = 3400000 # 3.4MHz Mode

# Latency Defines
I2C_LATENCY_TIMER = 255  # 255ms default; valid range of 0 - 255ms     

# Hardware Option Defines
# Three-phase clocking ON and open-drain drive ON -> I2C_DISABLE_3PHASE_CLK & I2C_DISABLE_DRIVE_ONLY_ZERO 
# Three-phase clocking OFF and open-drain drive ON -> I2C_DISABLE_3PHASE_CLK 
# Three-phase clocking ON and open-drain drive OFF -> I2C_DISABLE_DRIVE_ONLY_ZERO 
# Three-phase clocking OFF and open-drain drive OFF -> I2C_DISABLE_3PHASE_CLK | I2C_DISABLE_DRIVE_ONLY_ZERO  
I2C_DISABLE_3PHASE_CLK = 1 
I2C_DISABLE_DRIVE_ONLY_ZERO = 2

# I2C Transfer Option Defines
I2C_TRANSFER_OPTIONS_START_BIT = 1 # Default I2C transaction option
I2C_TRANSFER_OPTIONS_STOP_BIT = 2 # Default I2C transaction option
I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE = 8 # Default I2C transaction option
I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES = 16
I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BITS = 32
I2C_TRANSFER_OPTIONS_NO_ADDRESS = 64

# Status Codes
STATUS_CODES = {0: 'FT_OK',
          1: 'FT_INVALID_HANDLE',
          2: 'FT_DEVICE_NOT_FOUND',
          3: 'FT_DEVICE_NOT_OPENED',
          4: 'FT_INVALID_HANDLE',
          5: 'FT_IO_ERROR',
          6: 'FT_INVALID_PARAMETER',
          7: 'FT_INVALID_BAUD_RATE',
          8: 'FT_DEVICE_NOT_OPENED_FOR_ERASE',
          9: 'FT_DEVICE_NOT_OPENED_FOR_WRITE',
          10: 'FT_FAILED_TO_WRITE_DEVICE',
          11: 'FT_EEPROM_READ_FAILED',
          12: 'FT_EEPROM_WRITE_FAILED',
          13: 'FT_EEPROM_ERASE_FAILED',
          14: 'FT_EEPROM_NOT_PRESENT',
          15: 'FT_EEPROM_NOT_PROGRAMMED',
          16: 'FT_INVALID_ARGS',
          17: 'FT_NOT_SUPPORTED',
          18: 'FT_OTHER_ERROR',
          19: 'FT_DEVICE_LIST_NOT_READY'}

# Device Types
DEVICE_TYPES = {0: 'FT_DEVICE_BM',
          1: 'FT_DEVICE_BM',
          2: 'FT_DEVICE_100AX',
          3: 'FT_DEVICE_UNKNOWN',
          4: 'FT_DEVICE_2232C',
          5: 'FT_DEVICE_232R',
          6: 'FT_DEVICE_2232H',
          7: 'FT_DEVICE_4232H',
          8: 'FT_DEVICE_232H',
          9: 'FT_DEVICE_X_SERIES'}
          
#####STRUCTS###################################################################
          
class FT_DEVICE_LIST_INFO_NODE(ctypes.Structure):
    _fields_ = [
        ('Flags', ctypes.c_ulong),        
        ('Type', ctypes.c_ulong),
        ('ID', ctypes.c_ulong),
        ('LocID', ctypes.c_ulong),
        ('SerialNumber', ctypes.c_ubyte*16),
        ('Description', ctypes.c_ubyte*64),
        ('ftHandle', ctypes.c_ulong)]
        
class CHANNEL_CONFIG(ctypes.Structure):
    _fields_ = [
        ('ClockRate', ctypes.c_ulong),        
        ('LatencyTimer', ctypes.c_ubyte),
        ('Options', ctypes.c_ulong)]
          
#####CLASSES###################################################################

class I2CMaster():
    
    def __init__(self):
        pass

# I2C_GetNumChannels(uint32 *numChannels)

    def GetNumChannels(self):
        dll.I2C_GetNumChannels.argtypes = [ctypes.POINTER(ctypes.c_ulong)]    
        dll.I2C_GetNumChannels.restype = ctypes.c_ulong
        self._numchannels = ctypes.c_ulong()
        if dll.I2C_GetNumChannels(ctypes.byref(self._numchannels)) != 0:
            print STATUS_CODES[dll.I2C_GetNumChannels(ctypes.byref(self._numchannels))]
        else:
            print 'Number of Channels: %i' % self._numchannels.value
            return self._numchannels.value

# I2C_GetChannelInfo(uint32 index, FT_DEVICE_LIST_INFO_NODE *chanInfo)
            
    def GetChannelInfo(self):
        dll.I2C_GetChannelInfo.argtypes = [ctypes.c_ulong, ctypes.POINTER(FT_DEVICE_LIST_INFO_NODE)]    
        dll.I2C_GetChannelInfo.restype = ctypes.c_ulong
        self._chaninfo = FT_DEVICE_LIST_INFO_NODE()
        self._fulldevlist = OrderedDict()
        for idx in range(self._numchannels.value):
            self._index = ctypes.c_ulong(idx)
            if dll.I2C_GetChannelInfo(self._index, ctypes.byref(self._chaninfo)) != 0:
                print STATUS_CODES[dll.I2C_GetChannelInfo(self._index, ctypes.byref(self._chaninfo))]
            else:
                self._Type = DEVICE_TYPES[self._chaninfo.Type]            
                self._SerialNumber = ''.join(map(chr, self._chaninfo.SerialNumber)).split('\x00')[0]  # Remove non-ASCII characters
                self._Description = ''.join(map(chr, self._chaninfo.Description)).split('\x00')[0] # Remove non-ASCII characters
                print 'Flags: %i' % self._chaninfo.Flags 
                print 'Type: %s' % self._Type
                print 'ID: %i' % self._chaninfo.ID
                print 'LocID: %i' % self._chaninfo.LocID
                print 'SerialNumber: %s' % self._SerialNumber
                print 'Description: %s' % self._Description
                print 'Handle: %i' % self._chaninfo.ftHandle
                devinfolist = OrderedDict([('Flags', self._chaninfo.Flags), ('Type', self._Type), ('ID', self._chaninfo.ID), ('LocID', self._chaninfo.LocID), ('SerialNumber', self._SerialNumber), ('Description', self._Description), ('Handle', self._chaninfo.ftHandle)])
                self._fulldevlist['Dev%i' % idx] = devinfolist                
            return self._fulldevlist

# I2C_OpenChannel(uint32 index, FT_HANDLE *handle)
            
    def OpenChannel(self):
        dll.I2C_OpenChannel.argtypes = [ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)]    
        dll.I2C_OpenChannel.restype = ctypes.c_ulong
        for idx, device in enumerate(self._fulldevlist.values()):
            if device['Type'] ==  'FT_DEVICE_232H':
                self._index = ctypes.c_ulong(idx)
                if device['Handle'] == 0:
                    self._handle = ctypes.c_ulong()
                else:
                    self._handle = ctypes.c_ulong(device['Handle'])
            else:
                continue
            break
        if self._handle.value == 0: 
            if dll.I2C_OpenChannel(self._index, ctypes.byref(self._handle)) != 0:
                print STATUS_CODES[dll.I2C_OpenChannel(self._index, ctypes.byref(self._handle))]
            else:
                print 'Successfully opened device channel %i with handle %i' % (self._index.value, self._handle.value)
        else:
            print 'Device channel %i is already open with handle %i' % (self._index.value, self._handle.value)

# I2C_InitChannel(FT_HANDLE handle, ChannelConfig *config)

    def InitChannel(self, mode='Standard'):
        dll.I2C_InitChannel.argtypes = [ctypes.c_ulong, ctypes.POINTER(CHANNEL_CONFIG)]    
        dll.I2C_InitChannel.restype = ctypes.c_ulong
        if mode == 'Standard': # All modes default to open-drain drive with three-phase clocking
            self._config = CHANNEL_CONFIG(I2C_CLOCK_STANDARD_MODE, I2C_LATENCY_TIMER, I2C_DISABLE_3PHASE_CLK & I2C_DISABLE_DRIVE_ONLY_ZERO) 
        elif mode == 'Fast':
            self._config = CHANNEL_CONFIG(I2C_CLOCK_FAST_MODE, I2C_LATENCY_TIMER, I2C_DISABLE_3PHASE_CLK & I2C_DISABLE_DRIVE_ONLY_ZERO)
        elif mode == 'FastPlus':
            self._config = CHANNEL_CONFIG(I2C_CLOCK_FAST_MODE_PLUS, I2C_LATENCY_TIMER, I2C_DISABLE_3PHASE_CLK & I2C_DISABLE_DRIVE_ONLY_ZERO)
        elif mode == 'HighSpeed':
            self._config = CHANNEL_CONFIG(I2C_CLOCK_HIGH_SPEED_MODE, I2C_LATENCY_TIMER, I2C_DISABLE_3PHASE_CLK & I2C_DISABLE_DRIVE_ONLY_ZERO)
        else:
            self._config = CHANNEL_CONFIG(I2C_CLOCK_STANDARD_MODE, I2C_LATENCY_TIMER, I2C_DISABLE_3PHASE_CLK & I2C_DISABLE_DRIVE_ONLY_ZERO)
            print 'Mode not recognized. Defaulted to standard mode'
        if dll.I2C_InitChannel(self._handle, ctypes.byref(self._config)) != 0:
            print STATUS_CODES[dll.I2C_InitChannel(self._handle, ctypes.byref(self._config))]
        else:
            print 'Successfully initialized device channel %i with handle %i' % (self._index.value, self._handle.value)
            if (self._config.Options == 0 or self._config.Options == 2 ):
                print 'Clock Rate: %i' % int(self._config.ClockRate / 1.5) # libMPSSE DLL increases base clock by 1.5x when Three-phase clocking enabled
            else:
                print self._config.ClockRate 
            print 'Latency Timer: %i' % self._config.LatencyTimer
            print 'Options: %i' % self._config.Options
            
# I2C_CloseChannel(FT_HANDLE handle)
        
    def CloseChannel(self):
        dll.I2C_CloseChannel.argtypes = [ctypes.c_ulong]    
        dll.I2C_CloseChannel.restype = ctypes.c_ulong
        if dll.I2C_CloseChannel(self._handle) != 0:
            print STATUS_CODES[dll.I2C_CloseChannel(self._handle)]
        else:
            print 'Successfully closed device channel %i with handle %i' % (self._index.value, self._handle.value)
        
# I2C_DeviceRead(FT_HANDLE handle, uint32 deviceAddress, uint32 sizeToTransfer, uint8 *buffer, uint32 *sizeTransfered, uint32 options)       

    def DeviceRead(self, devaddress, regaddress, numbytes, fastbytes=False):
        dll.I2C_DeviceWrite.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulong), ctypes.c_ulong] # Buffer argtype is single byte only (register address)    
        dll.I2C_DeviceWrite.restype = ctypes.c_ulong
        dll.I2C_DeviceRead.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ubyte*numbytes), ctypes.POINTER(ctypes.c_ulong), ctypes.c_ulong] # Buffer argtype is specified read length
        dll.I2C_DeviceRead.restype = ctypes.c_ulong
        self._writebuffer = (ctypes.c_ubyte)(regaddress) # Buffer size is set from total data length. Pass data to buffer as variable length argument  
        self._writebytes = ctypes.c_ulong(1) # Number of bytes to write is total data length (register address + data)
        self._devaddress = ctypes.c_ulong(devaddress)  # Slave address of target device
        self._readbytes = ctypes.c_ulong(numbytes) # Number of bytes to read is user-specified (passed to function)
        self._readbuffer = (ctypes.c_ubyte*numbytes)() # Buffer size is set from number of bytes to read
        self._numsent = ctypes.c_ulong() # Number of bytes transmitted is number of bytes to read  
        if fastbytes == True:
            self._options = ctypes.c_ulong(I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT | I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE | I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES)
        else:
            self._options = ctypes.c_ulong(I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT | I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE)
        if dll.I2C_DeviceWrite(self._handle, self._devaddress, self._writebytes, ctypes.byref(self._writebuffer), ctypes.byref(self._numsent), self._options) != 0:
            print STATUS_CODES[dll.I2C_DeviceWrite(self._handle, self._devaddress, self._writebytes, ctypes.byref(self._writebuffer), ctypes.byref(self._numsent), self._options)]
        if dll.I2C_DeviceRead(self._handle, self._devaddress, self._readbytes, ctypes.byref(self._readbuffer), ctypes.byref(self._numsent), self._options) != 0:
            print STATUS_CODES[dll.I2C_DeviceRead(self._handle, self._devaddress, self._readbytes, ctypes.byref(self._readbuffer), ctypes.byref(self._numsent), self._options)]
        else:
            print 'I2C read transaction complete'
            print 'Device Address: 0x%02X' % self._devaddress.value
            print 'Register Address: 0x%02X' % regaddress
            for idx, byte in enumerate(self._readbuffer[:]):
                print 'Data Byte %i: 0x%02X' % (idx+1, byte)
            print 'Data Length: %i' % self._numsent.value
            return self._readbuffer[:]

# I2C_DeviceWrite(FT_HANDLE handle, uint32 deviceAddress, uint32 sizeToTransfer, uint8 *buffer, uint32 *sizeTransfered, uint32 options)

    def DeviceWrite(self, devaddress, regaddress, data, fastbytes=False):
        data.insert(0, regaddress) # Prepend data array with register address
        dll.I2C_DeviceWrite.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ubyte*len(data)), ctypes.POINTER(ctypes.c_ulong), ctypes.c_ulong] # Buffer argtype is total data length (register address + data)     
        dll.I2C_DeviceWrite.restype = ctypes.c_ulong
        self._devaddress = ctypes.c_ulong(devaddress) # Slave address of target device
        self._writebytes = ctypes.c_ulong(len(data)) # Number of bytes to write is total data length (register address + data)
        self._buffer = (ctypes.c_ubyte*len(data))(*data) # Buffer size is set from total data length. Pass data to buffer as variable length argument  
        self._numsent = ctypes.c_ulong() # Number of bytes transmitted is total data length (register address + data) 
        if fastbytes == True:
            self._options = ctypes.c_ulong(I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT | I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE | I2C_TRANSFER_OPTIONS_FAST_TRANSFER_BYTES)
        else:
            self._options = ctypes.c_ulong(I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT | I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE)
        if dll.I2C_DeviceWrite(self._handle, self._devaddress, self._writebytes, ctypes.byref(self._buffer), ctypes.byref(self._numsent), self._options) != 0:
            print STATUS_CODES[dll.I2C_DeviceWrite(self._handle, self._devaddress, self._writebytes, ctypes.byref(self._buffer), ctypes.byref(self._numsent), self._options)]
        else:
            print 'I2C write transaction complete'
            print 'Device Address: 0x%02X' % self._devaddress.value
            print 'Register Address: 0x%02X' % regaddress
            for idx, byte in enumerate(self._buffer[:]):
                print 'Data Byte %i: 0x%02X' % (idx+1, byte)
            print 'Data Length: %i' % self._numsent.value
        
# FT_WriteGPIO(FT_HANDLE handle, uint8 dir, uint8 value)
        
    def WriteGPIO(self, direction, value):
        dll.FT_WriteGPIO.argtypes = [ctypes.c_ulong, ctypes.c_ubyte, ctypes.c_ubyte]    
        dll.FT_WriteGPIO.restype = ctypes.c_ulong
        self._direction = ctypes.c_ubyte(direction) # 1 is output, 0 is input for 8-bit GPIO port; valid range of 0-255
        self._value = ctypes.c_ubyte(value) # 1 is logic high, 0 is logic low for 8-bit GPIO port; valid range of 0-255
        if dll.FT_WriteGPIO(self._handle, self._direction, self._value) != 0:
            print STATUS_CODES[dll.FT_WriteGPIO(self._handle, self._direction, self._value)]
        else:
            print 'GPIO write transaction complete'
            print 'P.0: Direction = %s, State = %s' % ('Output' if (self._direction.value & 1) else 'Input', 'High' if (self._value.value & 1) else 'Low') 
            print 'P.1: Direction = %s, State = %s' % ('Output' if (self._direction.value & 2) else 'Input', 'High' if (self._value.value & 2) else 'Low') 
            print 'P.2: Direction = %s, State = %s' % ('Output' if (self._direction.value & 4) else 'Input', 'High' if (self._value.value & 4) else 'Low') 
            print 'P.3: Direction = %s, State = %s' % ('Output' if (self._direction.value & 8) else 'Input', 'High' if (self._value.value & 8) else 'Low') 
            print 'P.4: Direction = %s, State = %s' % ('Output' if (self._direction.value & 16) else 'Input', 'High' if (self._value.value & 16) else 'Low') 
            print 'P.5: Direction = %s, State = %s' % ('Output' if (self._direction.value & 32) else 'Input', 'High' if (self._value.value & 32) else 'Low') 
            print 'P.6: Direction = %s, State = %s' % ('Output' if (self._direction.value & 64) else 'Input', 'High' if (self._value.value & 64) else 'Low') 
            print 'P.7: Direction = %s, State = %s' % ('Output' if (self._direction.value & 128) else 'Input', 'High' if (self._value.value & 128) else 'Low')
        
# FT_ReadGPIO(FT_HANDLE handle, uint8 *value)

    def ReadGPIO(self):
        dll.FT_ReadGPIO.argtypes = [ctypes.c_ulong, ctypes.POINTER(ctypes.c_ubyte)]    
        dll.FT_ReadGPIO.restype = ctypes.c_ulong
        self._value = ctypes.c_ubyte() # 1 is logic high, 0 is logic low for 8-bit GPIO port; valid range of 0-255
        if dll.FT_ReadGPIO(self._handle, ctypes.byref(self._value)) != 0:
            print STATUS_CODES[dll.FT_ReadGPIO(self._handle, ctypes.byref(self._value))]
        else:
            print 'GPIO read transaction complete'
            print 'P.0: State = %s' % ('High' if (self._value.value & 1) else 'Low') 
            print 'P.1: State = %s' % ('High' if (self._value.value & 2) else 'Low') 
            print 'P.2: State = %s' % ('High' if (self._value.value & 4) else 'Low') 
            print 'P.3: State = %s' % ('High' if (self._value.value & 8) else 'Low') 
            print 'P.4: State = %s' % ('High' if (self._value.value & 16) else 'Low') 
            print 'P.5: State = %s' % ('High' if (self._value.value & 32) else 'Low') 
            print 'P.6: State = %s' % ('High' if (self._value.value & 64) else 'Low') 
            print 'P.7: State = %s' % ('High' if (self._value.value & 128) else 'Low')
            return self._value.value

#  Init_libMPSSE(void)
        
    def Init_libMPSSE(self):
        dll.Init_libMPSSE.argtypes = []    
        dll.Init_libMPSSE.restype = None
        dll.Init_libMPSSE()
        
# Cleanup_libMPSSE(void)
        
    def Cleanup_libMPSSE(self):
        dll.Cleanup_libMPSSE.argtypes = []    
        dll.Cleanup_libMPSSE.restype = None
        dll.Cleanup_libMPSSE()
