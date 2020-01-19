#!/usr/bin/env python3

# DSMR4 = Dutch Smart Meter Requirements v4
# OBIS = Object Identification System
# https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_bf3be9c18c.pdf

# Requirements:
# - pyserial: pip install pyserial
# - tty permissions: adduser USERNAME tty
# - dialout permissions: adduser USERNAME dialout

import sys, serial

try:
  port = sys.argv[1]
  obis = sys.argv[2]
except IndexError:
  print("Usage: ./dsmr4reader.py port obis")
  print("Like: ./dsmr4reader.py /dev/ttyUSB0 0-0:1.0.0")
  sys.exit(1)

ser = serial.Serial(port, 115200, timeout=12)

for x in range(50):
  read = ser.readline().decode("utf-8")
  if not read: raise Exception("ReadTimeout")
  if read[:1] == "!": break
  if "(" in read:
    id = read.split("(")[0].strip()
    value = read[read.find("("):].replace("(", "").replace(")", " ").strip()
    if id == obis: print(id+": "+value)
ser.close()
