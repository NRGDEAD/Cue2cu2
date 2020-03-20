# Cue2cu2
Cue2cu2 is a free software, open source Python program to create a CU2 sheet from an existing, monolithic bin/cue set for use with CybDyn Systems' PSIO.
## Status of this program
After almost a year in the wild and various bug fixes, Cue2cu2 can be considered stable. Semi-automated testing with various selected cue sheets, including a special stress test cue sheet with many quirks at once, ensure that each release can at least handle what has been encountered so far.
While the most common errors now should produce an individual error message explaining what went wrong, there might still be cases where Python itself throws an error. Please report such cases with the cue sheet attached either through [GitHub](https://github.com/NRGDEAD/Cue2cu2) or the [CybDyn forum](https://www.cybdyn-systems.com.au/forum/viewtopic.php?f=17&t=1760).\
You are using this software at your own risk.
## Installing
Once you have Python installed, download cue2cu2.py or git clone the repository. It might be helpful to put it or a symlink somewhere within $PATH if it's used often.
## Usage
To convert a cue sheet, change to the directory of the disc image and run cue2cu2.py with the cue sheet as an argument.
### Example
If you cloned Cue2cu2 to it's own directory in your home directory on Linux/Mac, and want to create a CU2 sheet for the most recent PSIO firmware:
```
~/cue2cu2/cue2cu2.py EURO_DEMO_GERMAN_04.cue
```
### Options and syntax
```
cue2cu2.py [options] cuesheet
```

## Optional arguments
#### -h, --help
show a help message and exit.
#### -f FORMAT, --format FORMAT
Specify CU2 format revision:\
1 for Systems Console up to 2.4 (and sort of 2.5 to 2.7).\
2 for 2.8 and probably later versions (default.)
#### -c, --compat
Enables compatibility mode, aims to be bit-identical to what Systems Console would produce. This is the default mode.
#### -nc, --nocompat
Disables compatibility mode, produces a CU2 sheet without offset correction.
#### -s SIZE, --size SIZE
Manually specify binary filesize in bytes instead of obtaining it from the binary file.
#### -n NAME, --name NAME
Override the automatically determined output filename.
#### -o OFFSET, --offset OFFSET
Specify timecode offset for tracks and track end.\
Format: [+/-]MM:SS:ss, as in Minutes (00-99), Seconds (00-59), sectors (00-74).\
Example:
```
-o=-00:13:37
```
Note: resulting output range is limited to 00:00:00 - 99:59:74 and will be clipped if either boundary is crossed.
#### -os OFFSET_SELECT, --offset-select OFFSET_SELECT
Select the variables the offset will be applied to instead of the default audio tracks, pregaps, and track end only. Capitalization and order is arbitrary. Variables are represented by single letters: A (audio tracks), P (pregaps), E (track end), S (size), D (data1). Example to select everything: -os PASED
#### -1, --stdout
Output to stdout instead of a CU2 file named after the binary image file.
#### -q, --quiet
Suppress warning messages on inconveniences that don't hinder the program from continuing but might negatively affect the result.
## Output and compatibility
### Modes
#### Compatibility mode
Cue2cu2 aims to create a CU2 sheet that is bit identical to what the PSIO System Console would output in the given CU2 format revision. This is the default mode, which should be used in virtually all cases.
#### Non-compatibility mode
Cue2cu2 does not correct the track position timecodes's offsets, but instead uses the cue sheets' timecodes unaltered.\
The timecode notation is different when ending in a full second: 00:47:00 instead of 00:46:75.\
The last line has a CRLF line terminator.\
This mode will probably not work correctly on either PSIO firmware revision as of yet, and should usually not be used. It is included for user experiments.
#### Selecting a mode
There are two switches to toggle compatibility mode either on or off in case somebody wants to use Cue2cu2 within a script or workflow. Using neither will default to compatibility mode.
### Offset
It is possible to apply an additional offset. This will neither disable nor enable compatibility mode, but is applied after applying the compatibility offset correction to the data track start, each audio track start, pregap and the last track's end values. This option is for user experiments as well.
### The CU2 Format
The CU2 format was designed by CybDyn Systems specifically for use with the PSIO. The advantages over cue sheets from the PSIO's perspective are a simpler file structure and less format dialects.\
A key difference is that with cue sheets, timecode 00:00:00 refers to the first position after the lead-in/TOC, which is two seconds or 150 sectors long. While with the CU2 format, it refers to the absolute first sector. Thus, at first glance, it appears that CU2 sheets are shifted +2 seconds. This is not the case; both cue and CU2 sheet notations refer to the same physical sectors.\
The track end includes an additional two seconds for the lead-out.
#### Revision 1 - Systems Console up to 2.4 (and sort of 2.5 to 2.7)
With this format, the PSIO always assumes 2 second pregaps, which is inaccurate for a few titles.
Size is shifted +2 seconds for the lead-in.
The track end is shifted an additional +4 seconds compared to size, +6 in total.
#### Revision 2 - Systems Console 2.8 and later
The new revision includes a second line per track for the pregaps; Supported by PSIO firmware 2.6.11 and onwards, pregap lengths are now always respected.
Size is not shifted +2 seconds anymore and track end is shifted +2 compared to size.
#### Comparison
Here are the CU2 sheets for Euro Demo German 04 in both formats, compared via diff.
```
Format revision 1               Format revision 2
--------------------------------------------------
ntracks 4                       ntracks 4
size      38:02:32      |       size      38:00:32
data1     00:02:00              data1     00:02:00
                        >       pregap02  29:03:11
track02   29:05:11              track02   29:05:11
                        >       pregap03  32:53:36
track03   32:55:36              track03   32:55:36
                        >       pregap04  34:50:23
track04   34:52:23              track04   34:52:23
trk end   38:06:32      |       trk end   38:02:32
```
## Multi-bin images
Multi-bin images, a cue sheet referencing multiple bin files or even Wave, FLAC or other formats, are not supported. These need to be converted to monolithic, or single-bin, images first. This can be done with [binmerge](https://github.com/putnam/binmerge) in most simple cases or a combination of cdemu and cdrdao in more advanced cases (for example, when using images with FLAC or MP3 audio). Please refer to the documentation of those programs for more information.
## License
Copyright 2019-2020 NRGDEAD

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
## Trademarks
CybDyn, PSIO and PSIO System Console are registered(?) trademarks of CybDyn Systems Australia. The author is not affliated with CybDyn Systems Australia.
