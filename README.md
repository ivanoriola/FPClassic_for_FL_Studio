# FPClassic for FLStudio

Motorized FaderPort Classic support for FL Studio using the native MIDI Scripting API.

---

## Project Goals

FPClassic aims to provide native, lightweight and reliable support for the original PreSonus FaderPort Classic in FL Studio using only the official MIDI Scripting API.

The project intentionally avoids external drivers, helper applications or custom background services.

---

## Features

- Motorized fader synchronization
- Mixer volume control
- Pan encoder
- Shift + Pan = Tempo
- Mixer track selection
- Mixer highlight rectangle
- Mixer Mute / Solo / Arm
- Transport controls
- Undo / Redo history
- Window management
- Pattern navigation
- Output (Master) selection
- Metronome toggle
- Automatic LED synchronization
- Power-on self-test
- Auto-repeat navigation

---

## Requirements

- FL Studio 20.7 or higher version
- FaderPort Classic V.1.0
- MIDI Scripting enabled

---

## Installation

1. Download or clone this repository.

2. Copy the `FPClassic_for_FLStudio` folder to:
 \Documents\Image-Line\FL Studio\Settings\Hardware\


3. Connect the FaderPort Classic to your computer.

4. Start FL Studio.

5. Open:
 Options → MIDI Settings

6. In the **Input** section:
- Select **FaderPort**.
- Enable the device.
- Choose **FPClassic for FLStudio** as the controller type.

7. Click **Refresh device list** if the script does not appear immediately.

8. The FaderPort will perform its startup self-test and will be ready to use.

> [!NOTE]
> The script has been developed and tested with the original PreSonus FaderPort Classic using FL Studio's native MIDI Scripting API.
---

## Hardware Mapping

| FaderPort | FL Studio |
|-----------|-----------|
| Fader | Track Volume |
| Pan | Track Pan |
| Shift + Pan | Tempo |
| Left / Right | Previous / Next Mixer Track |
| Bank + Left / Right | Previous / Next Pattern |
| Output | Master Track |
| Mix | Mixer |
| Proj | Channel Rack |
| Trns | Playlist |
| Mute | Track Mute |
| Solo | Track Solo |
| Rec | Track Arm |
| Play | Play |
| Stop | Stop |
| Record | Record |
| Undo | Undo History |
| Shift + Undo | Redo |
| User | Metronome |
| Shift + User | Next Marker |
| Punch | TBD |
| Shift + Punch | Previous Marker |
| Loop | TBD |
| Shift + Loop | Add Marker |

---

## Customization

Most user settings can be modified in:

fp_constants.py

Examples:

- PAN_STEP
- FL Studio window assignments
- Timing constants
- ...

---

## Architecture

device_FaderPort.py
↓
fp_input.py
↓
fp_actions.py
↓
FL Studio API

fp_output.py
↑
fp_controls.py
↑
FL Studio state

---

## Known Limitations (TBD)

Current FL Studio MIDI Scripting API limitations:

- Punch In/Out marker creation
- Loop marker creation
- Shift + Rewind → Start
- Shift + Fast Forward → End

---

## Changelog

### Version 1.0.0

Initial public release.

Added

- Motorized fader support
- Mixer synchronization
- Pan encoder
- Mixer selection rectangle
- Pattern navigation
- Window management
- Transport controls
- Undo / Redo
- Automatic LED synchronization
- Power-on self-test
- Tempo encoder (Shift + Pan encoder )
- Metronome (User Switch)

---

## Credits

FPClassic for FLStudio

Developed by Iván Oriola.

Built using the FLStudio MIDI Scripting API.

---

## License

MIT License