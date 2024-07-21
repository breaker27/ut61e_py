"""
Created on Sep 22, 2017

@author: Dmitry Melnichansky 4X1MD ex 4X5DM, 4Z7DTF
         https://github.com/4x1md
         http://www.qrz.com/db/4X1MD

@note: The script uses UT61E class which to reads data from UNI-T UT61E using
       serial interface and displays it in human readable form.
"""

from __future__ import print_function
from ut61e import UT61E
import sys
import time
import datetime
from serial import SerialException

SLEEP_TIME = 1
PORT = "/dev/ttyUSB0"

if __name__ == '__main__':
  print("Starting UT61E monitor...")

  try:
    if len(sys.argv) == 2:
      port = sys.argv[1]
      simplified = False
    elif len(sys.argv) == 3:
      port = sys.argv[1]
      simplified = True
    else:
      port = PORT
      simplified = False

    dmm = UT61E(port)

    while True:
      meas = dmm.get_readable(disp_norm_val=True, simplified=simplified)
      if not simplified:
        print()
        print(datetime.datetime.now())
        print(meas)
      else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ',', meas)

      time.sleep(SLEEP_TIME)

  except SerialException as e:
    print("Serial port error.")
    print(e)

  except KeyboardInterrupt:
    print()
    print("Extiting UT61E monitor.")
    sys.exit()
