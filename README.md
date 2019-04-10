# Cue2cu2
Cue2cu2 is a Python program to create a CU2 sheet from an existing bin/cue set. As in a cue sheet with a single accompanying bin file.

## Status of this program
Cue2cu2 is experimental, especially in non-compatibility mode (see below).
There is hardly any error catching, so Python itself will likely throw an error if Cue2cu2 is surprised by something unusual in a cue sheet.
Thus, use at your own risk. Feel free to report any bugs; The author might try to fix one or two. ;-)

## Installing
Once you have Python installed, you just download cue2cu2.py and run it. Maybe put it somewhere within $PATH if you use it often...?

## Usage
```
cue2cu2.py [options] cuesheet

Options:	-h	--help		Show help
			--compat	Use compatibility mode (default)
			--nocompat	Don't use compatibility mode
			--stdout	Don't write a CU2 sheet, echo to stdout instead
```
### Multi-bin images
Multi-bin images, a cue sheet referencing multiple bin files or even Wave, FLAC or other formats, are not supported at this time. These need to be converted to single-bin images (one cue sheet with one bin file) first. This can be done with a combination of cdemu and cdrdao. Please refer to the documentation of those programs for more information.

### Compatibility mode
By default, Cue2cu2 uses the compatibility mode, and thus, aims to create a CU2 sheet that is identical to what the PSIO System Console would output.
While the resulting CU2 sheets seem to work fine with the PSIO, they appear to be inconsistent. Each track's starting position is 2 seconds behind the position noted in the original cue sheet, and "trk end" is 6 seconds beyond the bin file's end. Disabling compatibility mode uses the timecodes from the original cue sheet as well as seemingly correct values for size, data1 and trk end. However, as of writing this, it is unconfirmed if/what is the reason behind the timings per PSIO System Console. Thus, the non-compatibility mode is to be treated as experimental and subject to change.

There are two switches to toggle compatibility mode either on or off in case somebody wants to use Cue2cu2 within a script or workflow. Use no switch to get the default behavior - which might change in the future.

## License
Copyright 2019 NRGDEAD

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Trademarks
CybDyn, PSIO and PSIO System Console are registered(?) trademarks of CybDyn Systems Australia. The author is not affliated with CybDyn Systems Australia.
