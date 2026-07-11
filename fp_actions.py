"""
FPClassic for FLStudio actions.

High-level actions executed in FL Studio in response to FaderPort controls.
"""

import arrangement
import general
import mixer
import midi
import patterns
import transport
import ui

import fp_modes
import fp_constants

# ============================================================================
# Transport
# ============================================================================

def play():
    """Start or pause playback."""
    transport.globalTransport(midi.FPT_Play, 1)

def stop():
    """Stop playback."""
    transport.globalTransport(midi.FPT_Stop, 1)

def record():
    """Toggle recording."""
    transport.globalTransport(midi.FPT_Record, 1)

def rewind_start():
    """Start rewinding."""
    transport.globalTransport(midi.FPT_Rewind, midi.SS_Start)

def rewind_stop():
    """Stop rewinding."""
    transport.globalTransport(midi.FPT_Rewind, midi.SS_Stop)

def fast_forward_start():
    """Start fast-forwarding."""
    transport.globalTransport(midi.FPT_FastForward, midi.SS_Start)

def fast_forward_stop():
    """Stop fast-forwarding."""
    transport.globalTransport(midi.FPT_FastForward, midi.SS_Stop)

# ============================================================================
# Mixer
# ============================================================================

def mute_track(track):
    """Toggle the mute state of a mixer track."""
    mixer.muteTrack(track)

def solo_track(track):
    """Toggle the solo state of a mixer track."""
    mixer.soloTrack(track)

def arm_track(track):
    """Toggle the armed state of a mixer track."""
    mixer.armTrack(track)

# ============================================================================
# Navigation
# ============================================================================

def select_track(track):
    """Select a mixer track."""

    mixer.setTrackNumber(
        track,
        midi.curfxScrollToMakeVisible,
    )
    update_track_rectangle()

def select_output():
    """Select the Master track."""
    select_track(0)

def update_track_rectangle():
    """Move the mixer selection rectangle to the current track."""
    ui.miDisplayRect(
        mixer.trackNumber(),
        mixer.trackNumber(),
        midi.MaxInt,
        2,
    )

def left():
    """Select the previous mixer track."""
    if fp_modes.is_bank():
        previous_pattern()
    else:
        select_track(mixer.trackNumber() - 1)

def right():
    """Select the next mixer track."""
    if fp_modes.is_bank():
        next_pattern()
    else:
        select_track(mixer.trackNumber() + 1)


# ============================================================================
# Patterns
# ============================================================================

def previous_pattern():
    """Select the previous pattern."""
    patterns.jumpToPattern(patterns.patternNumber() - 1)


def next_pattern():
    """Select the next pattern."""
    patterns.jumpToPattern(patterns.patternNumber() + 1)


# ============================================================================
# Windows
# ============================================================================

def show_window(window):
    """Toggle an FL Studio window."""

    if ui.getVisible(window):
        ui.hideWindow(window)
    else:
        ui.showWindow(window)





# ============================================================================
# Fader modes
# ============================================================================

def read():
    """Select READ mode."""
    fp_modes.set_fader_mode(fp_modes.FaderMode.READ)

def write():
    """Select WRITE mode."""
    fp_modes.set_fader_mode(fp_modes.FaderMode.WRITE)

def touch():
    """Select TOUCH mode."""
    fp_modes.set_fader_mode(fp_modes.FaderMode.TOUCH)

def off():
    """Select OFF mode."""
    fp_modes.set_fader_mode(fp_modes.FaderMode.OFF)


# ============================================================================
# Fader
# ============================================================================

def _write_fader(fader):
    """Write the current FaderPort fader position to FL Studio."""

    volume = fader.position / fp_constants.FADER_RESOLUTION

    mixer.setTrackVolume(
        mixer.trackNumber(),
        volume,
    )

def fader_moved(fader):
    """Handle a new FaderPort fader position."""

    if fp_modes.is_read():
        return

    if fp_modes.is_write():
        _write_fader(fader)
        return

    if fp_modes.is_touch():
        if fader.is_touched:
            _write_fader(fader)
        return

    if fp_modes.is_off():
        # No synchronization
        return

# ============================================================================
# Pan Encoder
# ============================================================================

def pan(delta):
    """Adjust the pan of the selected mixer track."""

    track = mixer.trackNumber()

    value = mixer.getTrackPan(track)
    value += delta * fp_constants.PAN_STEP

    value = max(-1.0, min(1.0, value))

    mixer.setTrackPan(track, value)

# ============================================================================
# Undo History
# ============================================================================

def undo():
    """Move one step back/forward in the undo history."""
    if fp_modes.is_shift():
        general.undoDown()
        return
    general.undoUp()


# ============================================================================
# Bank Mode
# ============================================================================

def bank():
    """Toggle bank mode."""
    fp_modes.toggle_bank()


# ============================================================================
# Markers
# ============================================================================

def punch_in():
    """Create a Punch In marker (TBD).
    Currently jumps to the previous marker when Shift is pressed."""
    if fp_modes.is_shift():
        arrangement.jumpToMarker(-1, True)
        return

def loop():
    """Create a Loop marker (TBD).
    Currently adds a standard marker when Shift is pressed."""
    if fp_modes.is_shift():
        transport.globalTransport(midi.FPT_AddMarker, 1)
        return


# ============================================================================
# USER: Metronome
# ============================================================================

def user():
    """Toggle the metronome or jump to the next marker with Shift."""
    if fp_modes.is_shift():
        arrangement.jumpToMarker(1, True)
        return
    metronome()

def metronome():
    """Toggle the metronome."""
    transport.globalTransport(midi.FPT_Metronome, 1)
