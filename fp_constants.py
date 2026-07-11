"""
FPClassic for FLStudio constants.

Protocol and hardware constants for the FaderPort Classic.
"""


# ============================================================================
# Script Information
# ============================================================================

SCRIPT_NAME = "FPClassic for FLStudio"

SCRIPT_VERSION = "1.0.0"


# ============================================================================
# MIDI message types
# ============================================================================

POLY_PRESSURE_STATUS = 0xA0
"""Polyphonic Key Pressure."""

CONTROL_CHANGE_STATUS = 0xB0
"""Control Change."""

PITCH_BEND_STATUS = 0xE0
"""Pitch Bend."""


# ============================================================================
# Handshake (Script → FaderPort)
# ============================================================================

HANDSHAKE_REQUEST_STATUS_CH1 = 0x90
HANDSHAKE_REQUEST_STATUS_CH2 = 0x91

HANDSHAKE_REQUEST_DATA1 = 0x00
HANDSHAKE_REQUEST_DATA2 = 0x64


# ============================================================================
# Handshake (FaderPort → Script)
# ============================================================================

HANDSHAKE_ACK_STATUS = 0x91

HANDSHAKE_ACK_DATA1 = 0x00
HANDSHAKE_ACK_DATA2 = 0x02


# ============================================================================
# Switch protocol
# ============================================================================

SWITCH_GROUP_CC = 0x0F
"""Control Change message containing the switch group."""

SWITCH_DOWN_MASK = 0x40
"""Switch pressed bit."""


# ============================================================================
# Polyphonic Key Pressure protocol
# ============================================================================

VALUE_OFF = 0x00
"""Released / LED off."""

VALUE_ON = 0x01
"""Pressed / LED on."""


# ============================================================================
# Fader
# ============================================================================

FADER_MIN = 0
FADER_CENTER = 512
FADER_MAX = 1023
FADER_RESOLUTION = 1023

FADER_TOUCH_ID = 0x7F

FADER_POSITION_MSB_CC = 0x00
"""Most significant 7 bits."""

FADER_POSITION_LSB_CC = 0x20
"""Least significant 3 bits (stored in the upper nibble)."""


# ============================================================================
# Pan encoder
# ============================================================================

PAN_VALUE_CW = 0x01
"""Clockwise."""

PAN_VALUE_CCW = 0x7E
"""Counter-clockwise."""


# ============================================================================
# Device identification
# ============================================================================

MANUFACTURERS = {
    (0x00, 0x01, 0x06): "PreSonus",
}

FAMILIES = {
    0x0002: "FaderPort",
}

MODELS = {
    0x0001: "Classic (V1.0)",
}

# ============================================================================
# FL Studio windows
# ============================================================================

WID_MIXER = 0
"""Mixer."""

WID_CHANNEL_RACK = 1
"""Channel Rack."""

WID_PLAYLIST = 2
"""Playlist."""

WID_PIANO_ROLL = 3
"""Piano Roll."""

WID_BROWSER = 4
"""Browser."""

WID_PLUGIN = 5
"""Plugin window."""

WID_PLUGIN_EFFECT = 6
"""Effect plugin window."""

WID_PLUGIN_GENERATOR = 7
"""Generator plugin window."""

WID_PLUGIN_PICKER = 8
"""Plugin Picker."""


# ============================================================================
# Script settings
# ============================================================================

PAN_STEP = 0.02