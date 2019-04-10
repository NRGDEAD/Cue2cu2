#!/bin/python

# cue2cu2 - converts a cue sheet to CU2 format.
# Originally written by NRGDEAD in 2019. Use at your own risk.
# This program was written based on my web research and my reverse engineering of the CU2 format.
# Sorry, this is my first Python thingie. I have no idea what I'm doing. Thanks.

# Copyright 2019 NRGDEAD
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import functions or something?
import os
import argparse

# argparse - parsing arguments - this seemed to be easier in zsh
parser = argparse.ArgumentParser(description="Cue2cu2 converts a cue sheet to CU2 format.")
parser.add_argument("--nocompat", action="store_true", help="Disables compatibility mode")
parser.add_argument("--compat", action="store_true",  help="Enables compatibility mode (default)")
parser.add_argument("--stdout", action="store_true",  help="Output to stdout instead of a CU2 file matching the binary image file")
parser.add_argument("cuesheet")
args = parser.parse_args()
compatibility_mode = bool(True)
if args.nocompat:
	compatibility_mode = bool(False)
if args.compat:
	compatibility_mode = bool(True)
if args.stdout:
	stdout = bool(True)
else:
	stdout = bool(False)

cuesheet = args.cuesheet
cuesheet_file = open(cuesheet,"r") # We will close this later
for line in cuesheet_file:
	if "FILE" in line and "BINARY" in line:
		binaryfile = str(line)[6:][::-1][9:][::-1]
		break

# Function to convert timecode/index position to sector count
def convert_timecode_to_sectors(timecode):
	minutes = int(timecode[0:2])
	seconds = int(timecode[3:5])
	sectors = int(timecode[6:8])
	minutes_sectors = int(minutes*60*75)
	seconds_sectors = int(seconds*75)
	total_sectors = int(minutes_sectors+seconds_sectors+sectors)
	return total_sectors

# Function to convert sectors to timcode
def convert_sectors_to_timecode(sectors):
	total_seconds = int(int(sectors)/75)
	modulo_sectors = int(int(sectors)%75)
	total_minutes = int(total_seconds/60)
	modulo_seconds = int(total_seconds%60)
	timecode = str(total_minutes).zfill(2)+":"+str(modulo_seconds).zfill(2)+":"+str(modulo_sectors).zfill(2)
	return timecode

# Function to get the total runtime timecode for a given file
def convert_filesize_to_sectors(binaryfile):
	return int(int(os.path.getsize(binaryfile))/2352)

# Function to add two timecodes together
def timecode_addition(timecode, offset):
	return convert_sectors_to_timecode(convert_timecode_to_sectors(timecode)+convert_timecode_to_sectors(offset))

# Function to substract timecodes
def timecode_substraction(timecode, offset):
	return convert_sectors_to_timecode(convert_timecode_to_sectors(timecode)-convert_timecode_to_sectors(offset))

# Now obtain the variables to be used for the output and add them to said output

output = str()

# Get number of tracks from cue sheet
ntracks = 0
for line in cuesheet_file:
	if "TRACK" in line:
		ntracks += 1
cuesheet_file.close() # We don't need to read this anymore
output = output+"ntracks "+str(ntracks)+"\r\n"

# Get the total runtime/size
size = convert_sectors_to_timecode(convert_filesize_to_sectors(binaryfile))
if compatibility_mode == True:
	size = timecode_addition(size,"00:02:00")
output = output+"size      "+size+"\r\n"

# Get data1
# This was, in every CU2 sheet I looked at, set to two seconds. I have no idea how else this is obtained, so:
data1 = "00:00:00"
if compatibility_mode == True:
	data1 = timecode_addition(data1,"00:02:00")
output = output+"data1     "+data1+"\r\n"

# Get the tracks lengths
tracks = [] # Create empty array
for line in open(cuesheet): # Open the cue sheet and
	if "INDEX 01" in line: # Look for the lines with INDEX 01, then
		tracks.append(line) # Add them to the array
for track in range(2, ntracks+1): # Why do I have to +1 this? Python is weird
	track_position = tracks[track-1][::-1][:9][::-1][:8] # This is akward
	if compatibility_mode == True:
		track_position = timecode_addition(track_position,"00:02:00")
	output = output+"track"+str(track).zfill(2)+"   "+track_position+"\r\n"

# Add the end for the last track.
if compatibility_mode == True:
	track_end = timecode_addition(size,"00:04:00")
else:
	track_end = size
output = output+"\r\ntrk end   "+track_end

if stdout == True:
	print(output)
else:
	cu2sheet = binaryfile[::-1][4:][::-1]+".cu2"
	cu2file = open(cu2sheet,"w")
	cu2file.write(output)
	cu2file.close
