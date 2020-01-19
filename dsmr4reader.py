#!/usr/bin/env python3

# DSMR4 = Dutch Smart Meter Requirements v4
# https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_32ffe3cc38.pdf
# Requirements:
# - pyserial: pip install pyserial
# - tty permissions: adduser USERNAME tty
# - dialout permissions: adduser USERNAME dialout

import sys, serial

def main():

  # Get command line arguments
  try:
    port = sys.argv[1]
    id_list = sys.argv[2:]
  except IndexError:
    usage()

  # Connect to serial port
  try:
    ser = serial.Serial(port, 115200, timeout=12)
  except Exception as e:
    print(e)
    usage()

  # Convert names to id's
  id_list = list(map(name_to_id, id_list))

  # Read values
  values = read_values(ser, id_list)

  print(values)

  ser.close()


def read_values(serial, id_list):
  value_list = []
  for x in range(50):
    read = serial.readline().decode("utf-8")
    if not read: raise Exception("ReadTimeout")
    if read[:1] == "!": break
    if "(" in read:
      id = read.split("(")[0].strip()
      value = read[read.find("("):].replace("(", "").replace(")", " ").strip()
      if id in id_list: value_list.append([id,value])
      if id_list[0] == "all": value_list.append([id,value])
  return value_list


def name_to_id(name):
  # e = electricity
  # d = delivered
  # r = received
  # tc = to client
  # bc = by client
  # t# = tariff #
  # a = actual
  # pf = power failures
  # lpf = long power failures
  # pfl = power failure log
  # vs = voltage sags
  # l# = phase
  # c = current
  # p = power
  # g = gas

  table = {
    "version"   : "1-3:0.2.8",
    "datetime"  : "0-0:1.0.0",
    "id"        : "0-0:96.1.1",
    "e-d-tc-t1" : "1-0:1.8.1",
    "e-d-tc-t2" : "1-0:1.8.2",
    "e-d-bc-t2" : "1-0:2.8.2",
    "tariff"    : "0-0:96.14.0",
    "a-e-d"     : "1-0:1.7.0",
    "a-e-r"     : "1-0:2.7.0",
    "pf"        : "0-0:96.7.21",
    "lpf"       : "0-0:96.7.9",
    "pfl"       : "1-0:99.97.0",
    "vs-l1"     : "1-0:32.32.0",
    "volt"      : "1-0:32.36.0",
    "txtcode"   : "0-0:96.13.1",
    "txtmsg"    : "0-0:96.13.0",
    "c-l1"      : "1-0:31.7.0",
    "p-l1"      : "1-0:21.7.0",
    "p-l1-p"    : "1-0:22.7.0",
    "type"      : "0-1:24.1.0",
    "id-g"      : "0-1:96.1.0",
    "g-d-tc"    : "0-1:24.2.1",
  }
  return table.get(name, name)


def usage():
  print("Usage: ./dsmr4reader.py port id [id] [id]")
  print("Like: ./dsmr4reader.py /dev/ttyUSB0 0-0:1.0.0 0-0:96.1.1")
  sys.exit(1)


if __name__ == "__main__":
  main()
