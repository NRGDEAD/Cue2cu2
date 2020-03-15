#!/usr/bin/env python3

# cue2cu2 - converts a cue sheet to CU2 format.
# Originally written by NRGDEAD in 2019. Use at your own risk.
# This program was written based on my web research and my reverse engineering of the CU2 format.
# Sorry, this is my first Python thingie. I have no idea what I'm doing. Thanks.
# WWW: https://github.com/NRGDEAD/Cue2cu2

# Copyright 2019-2020 NRGDEAD
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
import argparse
import os
import sys
import re

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

# Function to convert sectors to timcode - but use MM:SS-1:75 instead of MM:SS:00. Thanks for finding that oddity, bikerspade!
def convert_sectors_to_timecode_with_alternative_notation(sectors):
	total_seconds = int(int(sectors)/75)
	modulo_sectors = int(int(sectors)%75)
	total_minutes = int(total_seconds/60)
	modulo_seconds = int(total_seconds%60)
	if modulo_sectors == 0:
		modulo_sectors = int(75)
		if modulo_seconds != 0:
			modulo_seconds = modulo_seconds - 1
		else:
			modulo_seconds = 59
			total_minutes = total_minutes - 1
	timecode = str(total_minutes).zfill(2)+":"+str(modulo_seconds).zfill(2)+":"+str(modulo_sectors).zfill(2)
	return timecode

# Function to get the total runtime timecode for a given filesize
def convert_bytes_to_sectors(filesize):
	if filesize % 2352 == 0:
		return int(int(filesize)/2352)
	else:
		error("The filesize of the binary file or --size parameter indicates that this is not a valid image in MODE2/2352")

# Function to get the total runtime timecode for a given file
def convert_filesize_to_sectors(binaryfile):
	if os.path.exists(binaryfile):
		return convert_bytes_to_sectors(os.path.getsize(binaryfile))
	else:
		error("Cue sheet refers to a binary file, "+binaryfile+", that could not be found. To manually override, use the --size parameter. See --help.")

# Function to add two timecodes together
def timecode_addition(timecode, offset):
	result = convert_timecode_to_sectors(timecode)+convert_timecode_to_sectors(offset)
	if result > int("449999"):
		result = int("449999") 
	return convert_sectors_to_timecode(result)

# Function to substract timecodes
def timecode_substraction(timecode, offset):
	result = convert_timecode_to_sectors(timecode)-convert_timecode_to_sectors(offset)
	if result < int("0"):
		result = int("0") 
	return convert_sectors_to_timecode(result)

# Function to throw an error and exit when something went wrong
def error(message):
	if message:
		print("Cue2cu2: Error while processing "+cuesheet+": "+message+".", file=sys.stderr)
		sys.exit(-1)
	else:
		print("Cue2cu2: Error while processing "+cuesheet+".", file=sys.stderr)
		sys.exit(-1)

# Function to warn about something, but continue
def warning(message):
	if message:
		print("Cue2cu2: Warning while processing "+cuesheet+": "+message+".", file=sys.stderr)
	else:
		print("Cue2cu2: Undefined warning while processing "+cuesheet+".", file=sys.stderr)

# Parsing arguments with argparse
parser = argparse.ArgumentParser(description="Cue2cu2 converts a cue sheet to CU2 format")
parser.add_argument("-nc","--nocompat", action="store_true", help="Disables compatibility mode, produces a CU2 sheet without offset correction. Included for user experiments")
parser.add_argument("-c","--compat", action="store_true",  help="Enables compatibility mode, aims to be bit-identical to what Systems Console would produce (default)")
parser.add_argument("-1","--stdout", action="store_true",  help="Output to stdout instead of a CU2 file named after the binary image file")
parser.add_argument("-s","--size", type=int, help="Manually specify binary filesize in bytes instead of obtaining it from the binary file")
parser.add_argument("-n","--name", type=str, help="Specify output filename instead of obtaining it from the cue sheet")
parser.add_argument("-f","--format", type=int, help="Specify CU2 format revision: 1 for Systems Console up to 2.4 (and sort of 2.5 to 2.7), 2 for 2.8 and probably later versions (default: 2)")
parser.add_argument("-o","--offset", type=str, help="Specify timecode offset for tracks and track end. Format: [+/-]MM:SS:ss, as in Minutes (00-99), Seconds (00-59), sectors (00-74). Example: -o=-00:13:37. Note: resulting output range is limited to 00:00:00 - 99:59:74")
parser.add_argument("cuesheet")
args = parser.parse_args()

# Configure compatibility mode
compatibility_mode = bool(True) # Default value
if args.nocompat:
	compatibility_mode = bool(False)
if args.compat:
	compatibility_mode = bool(True)
if args.compat == args.nocompat == True:
	error("Can not enable and disable compatibility mode at the same time, d'uh")

# Configure CU2 format revision
format_revision = int(2) # Default value
if args.format or str(args.format) == "0":
	if args.format == int(1):
		format_revision = int(1)
	elif args.format == int(2):
		format_revision = int(2)
	else:
		error("CU2 format revision must be either 1 or 2. Supplied: "+str(args.format))

# Should we output to the filesystem or stdout?
if args.stdout:
	stdout = bool(True)
else:
	stdout = bool(False)

# Do we get the filesize for the binary file from the file listed in the cue sheet or from an argument?
if args.size:
	filesize = int(args.size)
else:
	filesize = bool(False)

# Do we have an output filename? If not, we'll think about one later
if args.name:
	cu2sheet = args.name
else:
	cu2sheet = bool(False)

# Do we want to apply an offset to the timecodes?
if args.offset:
	offset_supplied = bool(True)
	# Is this a valid timecode with optional sign?
	if re.compile("^[+-]{0,1}[0-9]{2}:[0-5][0-9]:[0-7][0-9]$").match(args.offset) and int(args.offset[::-1][0:2][::-1]) <= int("74"):
		# Do we add or substract the timecode?
		if args.offset[0] == str("+"):
			offset_mode_is_add = bool(True)
			offset_timecode = str(args.offset[1:9])
		elif re.compile("^[0-9]$").match(args.offset[0]):
			offset_mode_is_add = bool(True)
			offset_timecode = str(args.offset)
		elif args.offset[0] == str("-"):
			offset_mode_is_add = bool(False)
			offset_timecode = str(args.offset[1:9])
	else:
		error("Supplied offset is invalid. Format: [+/-]MM:SS:ss, as in Minutes (00-99), Seconds (00-59), sectors (00-74)")
else:
	offset_supplied = bool(False)

# Make this a little more handy
cuesheet = args.cuesheet

# Now, onto the actual work

# Copy the cue sheet into an array so we don't have to re-read it from disk again and can navigate it easily
try:
	with open(cuesheet,"r") as cuesheet_file:
		cuesheet_content = cuesheet_file.read().splitlines()
		cuesheet_file.close
except:
	error("Could not open "+str(cuesheet))

# Check the cue sheet if the image is supposed to be in Mode 2 with 2352 bytes per sector
for line in cuesheet_content:
	cuesheet_mode_valid = bool(False)
	if re.compile(".*[Mm][Oo][Dd][Ee]2/2352.*").match(line):
		cuesheet_mode_valid = bool(True)
		break
if cuesheet_mode_valid == False: # If it's not, we can't continue
	error("Cue sheet indicates this image is not in MODE2/2352")

# Make sure this not a multi bin image, but does include exactly one FILE statement
files = int(0)
for line in cuesheet_content:
	if re.compile("[ \t]*[Ff][Ii][Ll][Ee].*").match(line):
		files += 1
if not files == int(1):
	error("The cue sheet is either invalid or part of an image with multiple binary files, which are not supported by this version of Cue2cu2")

# Extract the filename of the main image or binary file
for line in cuesheet_content:
	if re.compile("[ \t]*[Ff][Ii][Ll][Ee].*[Bb][Ii][Nn][Aa][Rr][Yy].*").match(line):
		binaryfile = str(line)[6:][::-1][8:][::-1]
		break
	else:
		error("Could not find binary file")

# Now obtain the variables to be used for the output and add them to said output

output = str()

# Get number of tracks from cue sheet
ntracks = 0
for line in cuesheet_content:
	if re.compile("[ \t]*[Tt][Rr][Aa][Cc][Kk].*").match(line) and not re.compile("[ \t]*[Ff][Ii][Ll][Ee].*[Tt][Rr][Aa][Cc][Kk].*").match(line): # Thanks for finding that bug, staticanime!
		ntracks += 1
output = output+"ntracks "+str(ntracks)+"\r\n"

# Get the total runtime/size
if not filesize == bool(False):
	size = convert_sectors_to_timecode(convert_bytes_to_sectors(filesize))
else:
	size = convert_sectors_to_timecode(convert_filesize_to_sectors(binaryfile))
# Add the two seconds for compatibility if needed
if compatibility_mode == True and format_revision == int(1):
	size = timecode_addition(size,"00:02:00")

output = output+"size      "+size+"\r\n"

# Get data1 - well, this is always the same for our kind of disc images, so...
# At some point I should do this the proper way and grab it from Track 1.
data1 = "00:00:00"
if compatibility_mode == True:
	data1 = timecode_addition(data1,"00:02:00")
# Apply offset if supplied
if offset_supplied == bool(True):
	if offset_mode_is_add == bool(True):
		data1 = timecode_addition(data1, offset_timecode)
	elif offset_mode_is_add == bool(False):
		data1 = timecode_substraction(data1, offset_timecode)
output = output+"data1     "+data1+"\r\n"

# Get the track and pregap lengths
for track in range(2, ntracks+1): # Why do I have to +1 this? Python is weird
	# Find current track number in cuesheet_content
	current_track_in_cuesheet = -1;
	for line in cuesheet_content:
		current_track_in_cuesheet += 1
		if re.compile(".*[Tt][Rr][Aa][Cc][Kk] 0?"+str(track)+".*").match(line):
			break
	# See if the next line is index 00, and if so, get and output the pregap if the CU2 format requires it
	if re.compile(".*[Ii][Nn][Dd][Ee][Xx] 0?0.*").match(cuesheet_content[current_track_in_cuesheet+1]) and format_revision == int(2):
		pregap_position = cuesheet_content[current_track_in_cuesheet+1][::-1][:8][::-1][:9]
		if compatibility_mode == True:
			# Add the famous two second offset for PSIO and convert to alternative notation used by Systems Console for tracks
			pregap_position = convert_sectors_to_timecode_with_alternative_notation(convert_timecode_to_sectors(timecode_addition(pregap_position,"00:02:00")))
		# Apply offset if supplied
		if offset_supplied == bool(True):
			if offset_mode_is_add == bool(True):
				pregap_position = timecode_addition(track_position, offset_timecode)
			elif offset_mode_is_add == bool(False):
				pregap_position = timecode_substraction(track_position, offset_timecode)
		output = output+"pregap"+str(track).zfill(2)+"  "+pregap_position+"\r\n"
	elif format_revision == int(2):
		error("Could not find pregap position (index 00) for track "+str(track))
	# Else-If is it index 01? If so, output track start, or get it from the following line
	if re.compile(".*[Ii][Nn][Dd][Ee][Xx] 0?1.*").match(cuesheet_content[current_track_in_cuesheet+1]):
		track_position = cuesheet_content[current_track_in_cuesheet+1][::-1][:8][::-1][:9] # I have no idea what I'm doing
	elif re.compile(".*[Ii][Nn][Dd][Ee][Xx] 0?1.*").match(cuesheet_content[current_track_in_cuesheet+2]):
		track_position = cuesheet_content[current_track_in_cuesheet+2][::-1][:8][::-1][:9]
	else:
		error("Could not find starting position (index 01) for track "+str(track))
	if compatibility_mode == True:
		# Add the famous two second offset for PSIO and convert to alternative notation used by Systems Console for tracks
		track_position = convert_sectors_to_timecode_with_alternative_notation(convert_timecode_to_sectors(timecode_addition(track_position,"00:02:00")))
	# Apply offset if supplied
	if offset_supplied == bool(True):
		if offset_mode_is_add == bool(True):
			track_position = timecode_addition(track_position, offset_timecode)
		elif offset_mode_is_add == bool(False):
			track_position = timecode_substraction(track_position, offset_timecode)
	output = output+"track"+str(track).zfill(2)+"   "+track_position+"\r\n"

# Add the end for the last track
if compatibility_mode == True and format_revision == int(1):
	track_end = convert_sectors_to_timecode_with_alternative_notation(convert_timecode_to_sectors(timecode_addition(size,"00:04:00")))
elif compatibility_mode == True and format_revision == int(2):
	track_end = convert_sectors_to_timecode_with_alternative_notation(convert_timecode_to_sectors(timecode_addition(size,"00:02:00")))
else:
	track_end = size
# Apply offset if supplied
if offset_supplied == bool(True):
	if offset_mode_is_add == bool(True):
		track_end = timecode_addition(track_end, offset_timecode)
	elif offset_mode_is_add == bool(False):
		track_end = timecode_substraction(track_end, offset_timecode)
output = output+"\r\ntrk end   "+track_end


if compatibility_mode == False:
	output = output + "\r\n"

# We are now ready to output our CU2 sheet
if stdout == True:
	if compatibility_mode == True:
		warning("Piping stdout to a file will add a proper linebreak to the last line. While not a problem per se, the CU2 sheet will not be bit identical to Systems Console output")
	print(output)
else:
	# Unless an output file name was specified, derive it from the binary file's filename
	if not cu2sheet:
		cu2sheet = binaryfile[::-1][4:][::-1]+".cu2"
	try:
		cu2file = open(cu2sheet,"wb")
		cu2file.write(output.encode())
		cu2file.close
	except:
		error("Could not write to "+str(cu2sheet))
