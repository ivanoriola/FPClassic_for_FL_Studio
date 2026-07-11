"""
FPClassic for FLStudio output.

Synchronizes the control objects with the FaderPort hardware.
"""

import time

import device
import mixer
import transport
import ui

import fp_actions
import fp_constants
import fp_input
import fp_modes
from fp_controls import *


# ============================================================================
# Module state
# ============================================================================

_handshake_sent = False

# ============================================================================
# Public API
# ============================================================================

def idle():
    """Periodic output processing."""
    
    # Handle auto-repeat
    for switch in ALL_SWITCHES:
        switch.update()

    global _handshake_sent

    if _handshake_sent:
        return

    for switch in ALL_SWITCHES:
        switch.invalidate()

    # Send handshake once
    _send_handshake()
    _handshake_sent = True

    # Power-on initialization
    self_test()
    refresh()
    sync()
    fp_actions.select_track(mixer.trackNumber())


def sync():
    """Synchronize all modified controls."""
    if not fp_input.is_initialized():
        return

    for switch in ALL_SWITCHES:

        if switch.dirty:
            _send_switch_led(switch)

    for fader in ALL_FADERS:

        if fader.dirty:
            _send_fader_position(fader)


# ============================================================================
# Handshake
# ============================================================================

def _send_handshake():
    """Send the initialization handshake."""

    _send_midi(
        fp_constants.HANDSHAKE_REQUEST_STATUS_CH1,
        fp_constants.HANDSHAKE_REQUEST_DATA1,
        fp_constants.HANDSHAKE_REQUEST_DATA2,
    )

    _send_midi(
        fp_constants.HANDSHAKE_REQUEST_STATUS_CH2,
        fp_constants.HANDSHAKE_REQUEST_DATA1,
        fp_constants.HANDSHAKE_REQUEST_DATA2,
    )


# ============================================================================
# Controls
# ============================================================================

def _send_switch_led(switch):
    """Send the LED state of a switch."""

    value = fp_constants.VALUE_ON if switch.led else fp_constants.VALUE_OFF

    _send_midi(
        fp_constants.POLY_PRESSURE_STATUS,
        switch.led_id,
        value,
    )

    switch.clear_dirty()

# NOTE:
# The FaderPort receives motor positions as standard 14-bit MIDI
# (MSB + LSB), but reports fader movement as a 14-bit value with the
# lower 4 bits always zero. Therefore:
#
# Send:
#     MSB = value >> 7
#     LSB = value & 0x7F
#
# Receive:
#     value = ((MSB << 7) | LSB) >> 4
#
# The effective resolution in both directions is 10 bits (0-1023).
def _send_fader_position(fader):
    """Send the motorized fader position."""


    if not fader.has_position:
        return

    value = max(fp_constants.FADER_MIN, min(fp_constants.FADER_MAX, fader.position))

    data_high = value >> 7
    data_low = value & 0x7F

    _send_midi(
        fp_constants.CONTROL_CHANGE_STATUS,
        fp_constants.FADER_POSITION_MSB_CC,
        data_high,
    )

    _send_midi(
        fp_constants.CONTROL_CHANGE_STATUS,
        fp_constants.FADER_POSITION_LSB_CC,
        data_low,
    )

    fader.clear_dirty()


# ============================================================================
# MIDI
# ============================================================================

def _send_midi(status, data1, data2):
    """Send a raw three-byte MIDI message."""

    message = status | (data1 << 8) | (data2 << 16)
    device.midiOutMsg(message)


# ============================================================================
# FL Studio synchronization
# ============================================================================

def refresh():
    """Update hardware state from FL Studio."""

    # Transport
    playing = transport.isPlaying()
    stop.led = not playing
    play.led = playing
    record.led = transport.isRecording()

    # Fader modes
    read.led = fp_modes.is_read()
    write.led = fp_modes.is_write()
    touch.led = fp_modes.is_touch()
    off.led = fp_modes.is_off()

    # FL Studio windows
    mix.led = ui.getVisible(fp_constants.WID_MIXER)
    proj.led = ui.getVisible(fp_constants.WID_CHANNEL_RACK)
    trns.led = ui.getVisible(fp_constants.WID_PLAYLIST)

    # Mixer track
    mute.led = mixer.isTrackMuted(mixer.trackNumber())
    solo.led = mixer.isTrackSolo(mixer.trackNumber())
    rec.led = mixer.isTrackArmed(mixer.trackNumber())

    #Utility
    bank.led = fp_modes.is_bank()
    user.led = ui.isMetronomeEnabled()

    if (
        fp_modes.is_read()
        or (fp_modes.is_touch() and not fader.is_touched)
    ):
        volume = mixer.getTrackVolume(mixer.trackNumber())
        fader.position = int(volume * fp_constants.FADER_RESOLUTION)


# ============================================================================
# Animations
# ============================================================================

def move_fader(position):
    """Move the motorized fader to a position."""
    fader.position = position
    sync()

def light_switches(switches, state=True):
    """Set the LEDs of the specified switches."""
    for switch in switches:
        switch.led = state

    sync()

def light_switches_in_order(switches, keep=True, inorder=True, delay=0, state=True):
    """Light the specified switches one by one."""
    if not inorder:
        switches = tuple(reversed(switches))

    for switch in switches:
        switch.led = state
        sync()
        time.sleep(delay)
        if not keep:
            switch.led = not state
            sync()

def self_test():
    """Run the FaderPort power-on self-test."""
    light_switches(ALL_SWITCHES, False)
    move_fader(fp_constants.FADER_MIN)
    time.sleep(0.75)
    
    move_fader(fp_constants.FADER_MAX)
    light_switches_in_order(ALL_SWITCHES, keep=True, inorder=False, delay=0.02, state=True)
    time.sleep(0.5)
    light_switches_in_order(ALL_SWITCHES, keep=True, inorder=False, delay=0.01, state=False)

def exit():
    """Run the shutdown animation."""
    light_switches(ALL_SWITCHES, True)
    time.sleep(0.75)
    light_switches_in_order(ALL_SWITCHES, keep=True, inorder=True, delay=0.01, state=False)