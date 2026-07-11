# name=FPClassic for FLStudio
# url=https://github.com/ivanoriola/FPClassic_for_FL_Studio.git
# supportedDevices=FaderPort Classic

"""
FPClassic for FLStudio.

Main device script.
"""

import fp_actions
import fp_input
import fp_output
import midi


def OnInit():
    """Called when the script is initialized."""
    fp_input.initialize()


def OnDeInit():
    """Called when the script is unloaded."""
    fp_output.exit()


def OnMidiMsg(event):
    """Called for every incoming MIDI message."""
    fp_input.handle_midi_message(event)
    event.handled = True


def OnRefresh(flags):
    """Called when FL Studio requests a hardware refresh."""

    fp_output.refresh()
    fp_output.sync()
    if flags & midi.HW_Dirty_Mixer_Sel:
        fp_actions.update_track_rectangle()


def OnIdle():
    """Called repeatedly by FL Studio."""
    # Keep the hardware synchronized.
    fp_output.idle()
    fp_output.refresh()
    fp_output.sync()


def OnControlChange(event):
    """Unused."""
    pass