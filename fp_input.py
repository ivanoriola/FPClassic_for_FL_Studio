"""
FPClassic for FLStudio input.

Receives MIDI messages from the FaderPort and updates the control objects.
"""

import fp_actions
import fp_constants
from fp_controls import (
    FADERS,
    SWITCHES,
    fader,
)
import fp_modes
import device
import midi
import transport

# ============================================================================
# Module state
# ============================================================================

_initialized = False


# ============================================================================
# Public API
# ============================================================================

def get_device_info():
    """Return information about the connected FaderPort."""

    data = device.getDeviceID()

    return {
        "manufacturer": tuple(data[:3]),
        "family": int.from_bytes(data[3:5], "little"),
        "model": int.from_bytes(data[5:7], "little"),
        "firmware": data[7:].decode("ascii"),
    }

def initialize():
    """Initialize the input module."""

    info = get_device_info()

    _print_banner()

    if info["manufacturer"] not in fp_constants.MANUFACTURERS:
        print("WARNING: Unsupported manufacturer.")
        return

    if info["family"] not in fp_constants.FAMILIES:
        print("WARNING: Unsupported device family.")
        return

    if info["model"] not in fp_constants.MODELS:
        print("WARNING: Unsupported device model.")
        return

    _print_device_info(info)

    bypass_handshake()

    return info


def _print_banner():
    """Print the script banner."""

    print()
    print("#" * 50)
    print(f"{fp_constants.SCRIPT_NAME} v{fp_constants.SCRIPT_VERSION} started")
    print("#" * 50)


def _print_device_info(info):
    """Print information about the connected device."""

    manufacturer = fp_constants.MANUFACTURERS[info["manufacturer"]]
    family = fp_constants.FAMILIES[info["family"]]
    model = fp_constants.MODELS[info["model"]]

    print()
    print("Device:")
    print(f"  Manufacturer : {manufacturer}")
    print(f"  Family       : {family}")
    print(f"  Model        : {model}")
    print(f"  Firmware     : {info['firmware']}")
    print()
    print("#" * 50)


def handle_midi_message(event):
    """Handle an incoming MIDI message."""

    if _handle_handshake(event):
        return

    if event.status == fp_constants.POLY_PRESSURE_STATUS:
        _handle_poly_pressure(event)

    elif event.status == fp_constants.CONTROL_CHANGE_STATUS:
        _handle_control_change(event)

    elif event.status == fp_constants.PITCH_BEND_STATUS:
        _handle_pan_encoder(event)


def is_initialized():
    """Return True if the handshake has completed."""

    return _initialized


def bypass_handshake():
    """Temporarily force the protocol to the initialized state."""

    global _initialized

    _initialized = True

# ============================================================================
# Handshake
# ============================================================================

def _handle_handshake(event):
    """Handle handshake acknowledgement."""

    global _initialized

    if (
        event.status == fp_constants.HANDSHAKE_ACK_STATUS
        and event.data1 == fp_constants.HANDSHAKE_ACK_DATA1
        and event.data2 == fp_constants.HANDSHAKE_ACK_DATA2
    ):
        _initialized = True
        print("Handshake confirmed")
        return True

    return False


# ============================================================================
# MIDI input
# ============================================================================

def _handle_poly_pressure(event):
    """Handle Polyphonic Key Pressure messages."""

    if event.data1 == fp_constants.FADER_TOUCH_ID:
        if event.data2 == fp_constants.VALUE_ON:
            fader.touch()
        else:
            fader.release()
        return

    switch = SWITCHES.get(event.data1)
    if switch is None:
        return

    if event.data2 == fp_constants.VALUE_ON:
        switch.press()
    else:
        switch.release()


def _handle_control_change(event):
    """Handle Control Change messages."""

    if event.data1 == fp_constants.FADER_POSITION_MSB_CC:
        fader.handle_msb(event.data2)

    elif event.data1 == fp_constants.FADER_POSITION_LSB_CC:
        fader.handle_lsb(event.data2)
        fp_actions.fader_moved(fader)


def _handle_pan_encoder(event):
    """Handle encoder rotation."""

    if event.data2 == fp_constants.PAN_VALUE_CW:
        if fp_modes.is_shift():
            transport.globalTransport(midi.FPT_TempoJog, 10)
        else:
            fp_actions.pan(1)

    elif event.data2 == fp_constants.PAN_VALUE_CCW:
        if fp_modes.is_shift():
            transport.globalTransport(midi.FPT_TempoJog, -10)
        else:
            fp_actions.pan(-1)