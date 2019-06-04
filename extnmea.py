#!/usr/bin/python
# coding: UTF-8

import sys
from sys import argv
import os

NMEA_START_CHAR = b'@Sonygps'   # Start characters of NMEA data.

# Read MOFF file.
def ReadMOFF(file_name):
    bin_data = b''
    with open(file_name, 'rb') as f:
        bin_data = f.read()
    return(bin_data)

# Search NMEA start characters from SONY moff file.
def SearchNMEA(bin_data):
    b_size = len(bin_data)
    start_code_size = len(NMEA_START_CHAR)
    if b_size < start_code_size:
        print("File size is too small.")
        return
    #print("start_code_size = %d" % start_code_size)
    found_flag = False
    for idx in range(0, b_size - 1):
        if bin_data[(idx):(start_code_size + idx)] == NMEA_START_CHAR:
            #print("Matched at [%d]" % idx)
            found_flag = True
            break
    if False == found_flag:
        idx = -1
    return idx

# Get NMEA string list
def GetNMEA_List(bin_data, nmea_idx):
    nmea_str_list = bin_data[nmea_idx:].decode()
    return(nmea_str_list.splitlines())

# Output NMEA txt file.
def OutputNMEA_List(file_name, nmea_str_list):
    with open(file_name, 'w') as f:
        nmea_lines = '\n'.join(nmea_str_list) + '\n'
        f.write(nmea_lines)

# Show usage.
def ShowUsage():
    #print("Usage: python " + os.path.basename(__file__) + " moff-file-name <output-file-name>")
    print("Usage: (python) " + os.path.basename(sys.argv[0]) + " moff-file-name <output-file-name>")

# Main
# Get Input & Output File names.
if len(sys.argv) < 2:
    ShowUsage()
    sys.exit(1)
input_file = sys.argv[1]
output_file = ''
if len(sys.argv) > 2:
    output_file = sys.argv[2]
else:
    name_body, name_ext = os.path.splitext(input_file)
    output_file = '.'.join([name_body, 'nmea'])

# Make NMEA data file.
if os.path.exists(input_file):
    # exist
    bin_data = ReadMOFF(input_file)
    nmea_idx = SearchNMEA(bin_data)
    nmea_str_list = GetNMEA_List(bin_data, nmea_idx)
    OutputNMEA_List(output_file, nmea_str_list)
else:
    # not exist
    ShowUsage()



