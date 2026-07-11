"""
FPClassic for FL Studio modes.
"""

from enum import IntEnum


# ============================================================================
# Fader Modes
# ============================================================================

class FaderMode(IntEnum):
    """Fader synchronization modes."""

    READ = 0
    WRITE = 1
    TOUCH = 2
    OFF = 3


fader_mode = FaderMode.TOUCH


def set_fader_mode(mode):
    """Set the current fader synchronization mode."""

    global fader_mode

    if fader_mode == mode:
        return

    fader_mode = mode


def is_read():
    """Return True if the current fader mode is READ."""
    return fader_mode == FaderMode.READ


def is_write():
    """Return True if the current fader mode is WRITE."""
    return fader_mode == FaderMode.WRITE


def is_touch():
    """Return True if the current fader mode is TOUCH."""
    return fader_mode == FaderMode.TOUCH


def is_off():
    """Return True if the current fader mode is OFF."""
    return fader_mode == FaderMode.OFF

# ============================================================================
# Bank Mode
# ============================================================================

_bank = False


def is_bank():
    """Return True if Bank mode is enabled."""
    return _bank

def toggle_bank():
    """Toggle Bank mode."""
    global _bank
    _bank = not _bank


# ============================================================================
# Shift Mode
# ============================================================================

_shift = False


def is_shift():
    """Return True if Shift is pressed."""
    return _shift

def set_shift(state):
    """Set the Shift state."""
    global _shift
    _shift = state