# pyMPSSE
A Python wrapper for the [libMPSSE] library, intended for use with FTDI USB-Serial Bridge ICs to enable simple communication with embedded devices without having to endure the complexities of working with the USB protocol.

Two variants of libMPSSE exist ([I2C] and [SPI]), however, the initial pyMPSSE release only covers **I2C communication** and **GPIO control**. Future enhancements may include support for SPI and JTAG. 

**NOTE:** libMPSSE is a library extension to the [ftd2xxx] device driver. 
Please ensure that you've installed both ft2dxxx and libMPSSE before attempting to use pyMPSSE.  

**NOTE:** Tested with Python 2.7 on Windows 7. 

Enjoy! :metal:

## Setup
The script currently looks for libMPSSE.dll in `C:\Python27\Lib\site-packages\`. 
The location must be updated if residing elsewhere on your system.   

## References
[MPSSE Basics]

[libMPSSE User Guide]

[libMPSSE-I2C Sample Project]

[libMPSSE Source]

[FT232H Datasheet]

[C232HM-DDHSL-0 Datasheet]

[libMPSSE]: http://www.ftdichip.com/Support/SoftwareExamples/MPSSE/LibMPSSE-I2C/libMPSSE-I2C.zip
[I2C]: http://www.ftdichip.com/Support/SoftwareExamples/MPSSE/LibMPSSE-I2C.htm
[SPI]: http://www.ftdichip.com/Support/SoftwareExamples/MPSSE/LibMPSSE-SPI.htm
[ftd2xxx]: http://www.ftdichip.com/Drivers/D2XX.htm
[MPSSE Basics]:  http://www.ftdichip.com/Support/Documents/AppNotes/AN_135_MPSSE_Basics.pdf
[libMPSSE User Guide]:  http://www.ftdichip.com/Support/Documents/AppNotes/AN_177_User_Guide_For_LibMPSSE-I2C.pdf
[libMPSSE Source]:  http://www.ftdichip.com/Support/SoftwareExamples/MPSSE/LibMPSSE-I2C/LibMPSSE-I2C_source.zip
[FT232H Datasheet]: http://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT232H.pdf
[C232HM-DDHSL-0 Datasheet]: http://www.ftdichip.com/Support/Documents/DataSheets/Cables/DS_C232HM_MPSSE_CABLE.pdf
[libMPSSE-I2C Sample Project]: http://www.ftdichip.com/Support/Documents/AppNotes/AN_190_C232HM_MPSSE_Cable_in_USB_to_I2C_Interface.pdf
