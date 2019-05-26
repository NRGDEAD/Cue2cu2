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

# Function to throw an error and exit when something went wrong
def error(message):
	if message:
		sys.exit("Cue2cu2 error: "+message)
	else:
		sys.exit("Cue2cu2 error.")

# Parsing arguments with argparse
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

cuesheet = args.cuesheet # Make this a little more handy

# Copy the cue sheet into a variable so we don't have to re-read it from disk again.
with open(cuesheet,"r") as cuesheet_file:
	cuesheet_content = cuesheet_file.read()

# Check the cue sheet if the image is supposed to be in Mode 2 with 2352 bytes per sector
for line in cuesheet_content.splitlines():
	cuesheet_mode_valid = bool(False)
	if "MODE2/2352" in line:
		cuesheet_mode_valid = bool(True)
		break
if cuesheet_mode_valid == False:
	error("Cue sheet indicates this image is not in MODE2/2352")

# Extract the filename of the main image or binary file
for line in cuesheet_content.splitlines():
	if "FILE" in line and "BINARY" in line:
		binaryfile = str(line)[6:][::-1][8:][::-1]
		break

# Now obtain the variables to be used for the output and add them to said output

output = str()

# Get number of tracks from cue sheet
ntracks = 0
for line in cuesheet_content.splitlines():
	if "TRACK" in line:
		ntracks += 1
#cuesheet_file.close() # We don't need to read this anymore
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
for line in cuesheet_content.splitlines():
	if "INDEX 01" in line: # Look for the lines with INDEX 01, then
		tracks.append(line) # Add them to the array

for track in range(2, ntracks+1): # Why do I have to +1 this? Python is weird
	#track_position = tracks[track-1][::-1][:9][::-1][:9] # This was when accessing the cue sheet file rather than copying it into a variable for performance
	track_position = tracks[track-1][::-1][:8][::-1][:9] # I have no idea what I'm doing
	if compatibility_mode == True:
		track_position = timecode_addition(track_position,"00:02:00")
	output = output+"track"+str(track).zfill(2)+"   "+track_position+"\r\n"

# Add the end for the last track.
if compatibility_mode == True:
	track_end = timecode_addition(size,"00:04:00")
else:
	track_end = size
output = output+"\r\ntrk end   "+track_end


if compatibility_mode == False:
	output = output + "\r\n"

if stdout == True:
	print(output)
else:
	cu2sheet = binaryfile[::-1][4:][::-1]+".cu2"
	cu2file = open(cu2sheet,"w")
	cu2file.write(output)
	cu2file.close
