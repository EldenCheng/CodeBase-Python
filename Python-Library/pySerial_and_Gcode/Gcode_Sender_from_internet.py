#!/usr/bin/env python
"""\
Simple g-code streaming script for grbl
"""

import serial
import time

if __name__ == '__main__':
    # Open grbl serial port
    s = serial.Serial('COM3', 115200)

    # Open g-code file
    gcode = bytes('G1G90 Z0.0F100', encoding='ascii')

    # Wake up grbl
    s.write(b"\r\n\r\n")
    time.sleep(2)  # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input

    # Stream g-code to grbl

    print('Sending: {0}'.format(gcode), s.write(gcode))  # Send g-code block to grbl
    grbl_out = s.readline()  # Wait for grbl response with carriage return
    print(' : ' + str(grbl_out.strip()))

    # Wait here until grbl is finished to close serial port and file.
    input("  Press <Enter> to exit and disable grbl.")

    # Close file and serial port
    f.close()
    s.close()
