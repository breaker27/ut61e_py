"""
Created on Sep 22, 2017

@author: Dmitry Melnichansky 4X1MD ex 4X5DM, 4Z7DTF
         https://github.com/4x1md
         http://www.qrz.com/db/4X1MD

@note: The script uses UT61E class which to reads data from UNI-T UT61E using
       serial interface and displays it in human readable form.
"""

from __future__ import print_function
from lib.ut61e import UT61E
import sys
import time
import datetime
from serial import SerialException

SLEEP_TIME = 1
port = "/dev/ttyUSB0"
outfile = "/dev/null"
sec = -1

def syntax():
    print("\nSyntax: " + sys.argv[0] + " [PORT] [FILE]")
    print("   [PORT] is e.g. /dev/ttyUSB0 (= default)")
    print("   [FILE] is the filename to append the measurements.")
    print("          Use AUTO to create file name automatically using format YYYY-MM-DD-HH-MM-SS_ut61e.txt.")
    print()

# Wait until next second with 10ms accuracy. Don't sleep, since over time there would be seconds without data.
#def waitNextSec():
#    global sec
#    while sec == int(time.time()):
#        time.sleep(0.01)
#    sec = int(time.time())

if __name__ == '__main__':
  print("Starting UT61E monitor...")
  simplified = True

  try:
    if len(sys.argv) == 1:
      syntax()
    elif len(sys.argv) == 2:
      port = sys.argv[1]
    elif len(sys.argv) == 3:
      port = sys.argv[1]
      if sys.argv[2] == "AUTO":
        outfile = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S_ut61e.txt')
      else:
        outfile = sys.argv[2]
      print("Writing to file " + outfile)
    else:
      syntax()
      sys.exit()

    dmm = UT61E(port)

    f = open(outfile, "a")

    while True:
      meas = dmm.get_readable(disp_norm_val=True, simplified=simplified)
      now = datetime.datetime.now()

      if now.strftime('%S') != sec:
        s = now.strftime('%Y-%m-%d %H:%M:%S') + ',' + meas
        print(s)

        if meas != "UT61E is not connected.":
            f.write(s + "\n")
            sec = now.strftime('%S')

  except SerialException as e:
    print("Serial port error.")
    print(e)

  except KeyboardInterrupt:
    print()
    print("Extiting UT61E monitor.")
    f.close()
    sys.exit()
