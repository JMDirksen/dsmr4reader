#!/usr/bin/env python3

# DSMR4 = Dutch Smart Meter Requirements v4
# https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_bf3be9c18c.pdf

# Requirements:
# - pyserial: pip install pyserial
# - tty permissions: adduser USERNAME tty
# - dialout permissions: adduser USERNAME dialout

import sys, serial

def main():
  try:
    port = sys.argv[1]
    id_list = sys.argv[2:]
  except IndexError:
    usage()

  try:
    ser = serial.Serial(port, 115200, timeout=12)
  except Exception as e:
    print(e)
    usage()

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
  return value_list


def usage():
  print("Usage: ./dsmr4reader.py port id [id] [id]")
  print("Like: ./dsmr4reader.py /dev/ttyUSB0 0-0:1.0.0 0-0:96.1.1")
  sys.exit(1)


if __name__ == "__main__":
  main()
