# Cue2cu2
Cue2cu2 is a Python program to create a CU2 sheet from an existing bin/cue set. As in a cue sheet with a single accompanying bin file.

## Status of this program
Cue2cu2 is somewhat experimental.
There is not too much error catching yet, so Python itself might throw an error if Cue2cu2 is caught off guard by something unusual in a cue sheet.
You are using this software at your own risk.
Feel free to report any bugs; the author might try to fix one or two. ;-)

## Installing
Once you have Python installed, download cue2cu2.py or git clone the repository. It might be helpful to put it or a symlink somewhere within $PATH if it's used often.

## Usage
To convert a cue sheet, change to the directory of the disc image and run cue2cu2.py with the cue sheet as an argument. For example:
```
./cue2cu2.py EURO_DEMO_GERMAN_04.cue
```
### Options
```
cue2cu2.py [options] cuesheet

Options:	-h	--help			Show help
			--compat		Use compatibility mode (default)
			--nocompat		Don't use compatibility mode
			--stdout		Don't write a CU2 sheet, echo to stdout instead
			-s SIZE, --size SIZE	Manually specify filesize of the binary file instead of obtaining it automatically
			-o OFFSET, --offset OFFSET
                        Specify timecode offset for tracks and track end.
			Format: [+/-]MM:SS:ss, as in Minutes (00-99), Seconds (00-59), sectors (00-74).
			Example: -o=-00:13:37. Note: resulting output range is limited to 00:00:00 - 99:59:74
```
### Multi-bin images
Multi-bin images, a cue sheet referencing multiple bin files or even Wave, FLAC or other formats, are not supported at this time. These need to be converted to single-bin images (one cue sheet with one bin file) first. This can be done with [binmerge](https://github.com/putnam/binmerge) in simple cases or a combination of cdemu and cdrdao in more advanced cases (for example, when using images with FLAC or MP3 audio). Please refer to the documentation of those programs for more information.

### Compatibility
By default, Cue2cu2 uses the compatibility mode, and thus, aims to create a CU2 sheet that is bit identical to what the PSIO System Console would output.
While the resulting CU2 sheets seem to work fine with the PSIO, they appear to be inconsistent. Each track's starting position is 2 seconds behind the position noted in the original cue sheet, and "trk end" is 6 seconds beyond the bin file's end. Disabling compatibility mode uses the timecodes from the original cue sheet as well as seemingly correct values for size, data1 and trk end. The author has since confirmed with CybDyn that this is indeed expected behaviour by the PSIO System Console. Thus, the non-compatibility mode is to be treated as experimental.

There are two switches to toggle compatibility mode either on or off in case somebody wants to use Cue2cu2 within a script or workflow. Use no switch to get the default behavior - which might change in the future to maintain compatibility with the current version of PSIO System Console.

Furthermore, it is now possible to apply an additional offset. This will neither disable nor enable compatibility mode, but is applied after (not) applying the compatibility offsets to each track and the track end value. This option is for user experiments.

## License
Copyright 2019 NRGDEAD

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

## Trademarks
CybDyn, PSIO and PSIO System Console are registered(?) trademarks of CybDyn Systems Australia. The author is not affliated with CybDyn Systems Australia.
