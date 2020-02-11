# Cue2cu2
Cue2cu2 is a free software, open source Python program to create a CU2 sheet from an existing, monolithic bin/cue set for use with CybDyn Systems' PSIO.

## Status of this program
Cue2cu2 is somewhat experimental.
There is not too much error catching yet, so Python itself might throw an error if Cue2cu2 is caught off guard by something unusual in a cue sheet.
You are using this software at your own risk.
Feel free to report any bugs; the author might try to fix one or two. ;-)

## Installing
Once you have Python installed, download cue2cu2.py or git clone the repository. It might be helpful to put it or a symlink somewhere within $PATH if it's used often.

## Usage
To convert a cue sheet, change to the directory of the disc image and run cue2cu2.py with the cue sheet as an argument.
For example, if you cloned Cue2cu2 to it's own directory in your home directory on Linux/Mac:
```
~/cue2cu2/cue2cu2.py EURO_DEMO_GERMAN_04.cue
```
### Options
```
cue2cu2.py [options] cuesheet

optional arguments:
  -h, --help            show a help message and exit
  -nc, --nocompat       Disables compatibility mode, produces a CU2 sheet without 2/4 seconds offset. 
  -c, --compat          Enables compatibility mode, aims to be bit-identical to what Systems Console would produce (default)
  -1, --stdout          Output to stdout instead of a CU2 file named after the binary image file
  -s SIZE, --size SIZE  Manually specify binary filesize in bytes instead of obtaining it from the binary file
  -f FORMAT, --format FORMAT
                        Specify CU2 format revision:
			1 for Systems Console up to 2.4 (and sort of 2.5 to 2.7)
			2 for 2.8 and probably later versions (default)
  -o OFFSET, --offset OFFSET
                        Specify timecode offset for tracks and track end.
			Format: [+/-]MM:SS:ss, as in Minutes (00-99), Seconds (00-59), sectors (00-74).
			Example: -o=-00:13:37.
			Note: resulting output range is limited to 00:00:00 - 99:59:74 and will be clipped if either boundary is crossed

```

### Output and compatibility
#### Modes
##### Compatibility mode
Cue2cu2 aims to create a CU2 sheet that is bit identical to what the PSIO System Console would output in the given CU2 format revision.
##### Non-compatibility mode
Cue2cu2 does not shift the tracks, but instead uses the cue sheets' timecodes unaltered. The timecode notation is different when ending in a full second: 00:47:00 instead of 00:46:75.
This mode will probably not work correctly on either PSIO firmware revision as of yet, but is included for user experiments.
##### Selecting a mode
There are two switches to toggle compatibility mode either on or off in case somebody wants to use Cue2cu2 within a script or workflow. Use no switch to get the default behavior - which might change in the future to maintain compatibility with the current version of PSIO System Console.
#### CU2 file format revisions
As of Systems Console 2.8, a new revision of the CU2 format has been introduced. This includes a new string for the pregaps, while still being shifted +2 seconds, apparently for having the newer firmware be able to read old format CU2s without much fuss.
##### 1 - Systems Console up to 2.4 (and sort of 2.5 to 2.7)
The tracks are shifted +2 seconds and the track end is shifted an additional +2 for pregaps and lead-out respectively. Always assumes 2 second pregaps, which is inaccurate for a few titles.
##### 2 - Systems Console 2.8 and probably later
Same as 1, but has an additional line per track for the pregaps and the data track is also being shifted. Dynamic pregap length, as per CU2 sheet.

### Offset
It is possible to apply an additional offset. This will neither disable nor enable compatibility mode, but is applied after (not) applying the compatibility offsets to each audio track start, pregap and the last track's end values. This option is for user experiments as well.

### Multi-bin images
Multi-bin images, a cue sheet referencing multiple bin files or even Wave, FLAC or other formats, are not supported. These need to be converted to monolithic, or single-bin, images first. This can be done with [binmerge](https://github.com/putnam/binmerge) in most simple cases or a combination of cdemu and cdrdao in more advanced cases (for example, when using images with FLAC or MP3 audio). Please refer to the documentation of those programs for more information.

## License
Copyright 2019 NRGDEAD

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

## Trademarks
CybDyn, PSIO and PSIO System Console are registered(?) trademarks of CybDyn Systems Australia. The author is not affliated with CybDyn Systems Australia.
