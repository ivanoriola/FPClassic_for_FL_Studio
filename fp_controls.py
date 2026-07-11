"""
FPClassic for FLStudio controls.

Hardware objects representing the physical controls of the FaderPort Classic.
"""

import time
import mixer

import fp_actions
import fp_constants
import fp_modes

# ============================================================================
# Base Control
# ============================================================================

class Control:
    """Base class for all FaderPort controls."""

    def __init__(self, control_id, name):
        self.control_id = control_id
        self.name = name

        self._dirty = False

    @property
    def id(self):
        """Hardware identifier."""
        return self.control_id

    @property
    def dirty(self):
        """True if the control state has changed."""
        return self._dirty

    def _set_dirty(self):
        """Mark the control as modified."""
        self._dirty = True

    def clear_dirty(self):
        """Mark the control as synchronized."""
        self._dirty = False


# ============================================================================
# Switch
# ============================================================================

class Switch(Control):
    """A physical switch on the FaderPort."""

    def __init__(
        self,
        control_id,
        led_id,
        name,
        on_press=None,
        on_release=None,
        auto_repeat=False,
        repeat_delay=0.4,
        repeat_interval=0.1,
    ):
        super().__init__(control_id, name)

        self.led_id = led_id
        self.on_press = on_press
        self.on_release = on_release
        self.auto_repeat = auto_repeat
        self.repeat_delay = repeat_delay
        self.repeat_interval = repeat_interval


        self.is_pressed = False
        self.press_time = 0.0
        self.last_repeat = 0.0
        self._led = False

    def press(self):
        """Update the switch state to pressed."""

        self.is_pressed = True
        self.press_time = time.time()
        self.last_repeat = self.press_time

        if self.on_press is not None:
            self.on_press()

    def release(self):
        """Update the switch state to released."""

        self.is_pressed = False

        if self.on_release is not None:
            self.on_release()

    def update(self):
        """Handle automatic button repeat."""

        if not self.auto_repeat or not self.is_pressed:
            return

        now = time.time()

        if now - self.press_time < self.repeat_delay:
            return

        if now - self.last_repeat >= self.repeat_interval:
            self.last_repeat = now

            if self.on_press is not None:
                self.on_press()

    def led_on(self):
        """Turn the LED on."""
        self.led = True

    def led_off(self):
        """Turn the LED off."""
        self.led = False

    @property
    def is_released(self):
        """True if the switch is not currently pressed."""
        return not self.is_pressed

    @property
    def led(self):
        """Current LED state."""
        return self._led

    @led.setter
    def led(self, state):
        """Set the LED state."""

        state = bool(state)

        if self._led == state:
            return

        self._led = state
        self._set_dirty()

    def invalidate(self):
        """Force the LED to be synchronized."""
        self._set_dirty()

# ============================================================================
# Encoder
# ============================================================================

class Encoder(Control):
    """An incremental rotary encoder."""

    def __init__(self, control_id, name):
        super().__init__(control_id, name)

        self.delta = 0

    @property
    def cw(self):
        """True if the last rotation was clockwise."""
        return self.delta > 0

    @property
    def ccw(self):
        """True if the last rotation was counter-clockwise."""
        return self.delta < 0

    def rotate(self, delta):
        """Update the last encoder movement."""
        self.delta = delta

    def reset(self):
        """Reset the encoder movement."""
        self.delta = 0


# ============================================================================
# Fader
# ============================================================================

class Fader(Control):
    """A motorized, touch-sensitive fader."""

    def __init__(self, control_id, name):
        super().__init__(control_id, name)

        self._pending_msb = None
        self._position = None
        self.is_touched = False

    @property
    def has_position(self):
        """True if the current fader position is known."""
        return self._position is not None

    @property
    def position(self):
        """Current fader position."""
        return self._position

    @position.setter
    def position(self, value):
        """Move the fader to a new position."""

        if self._position == value:
            return

        self._position = value
        self._set_dirty()

    def update_position(self, value):
        """Update the stored position without marking it dirty."""
        self._position = value

    def touch(self):
        """Update the touch state to touched."""
        self.is_touched = True

    def release(self):
        """Update the touch state to released."""
        self.is_touched = False
        self.invalidate()

    def invalidate(self):
        """Force the FADER to be synchronized."""
        self._set_dirty()

    def handle_msb(self, value):
        """Store the most significant byte of an incoming fader position."""
        self._pending_msb = value

    def handle_lsb(self, value):
        """Complete the incoming fader position update."""
        # NOTE:
        # The FaderPort reports fader movement as a 14-bit MIDI value where the
        # lower 4 bits are always zero. The original 10-bit position is recovered
        # by combining MSB and LSB, then shifting right by 4 bits:
        #
        #     value = ((MSB << 7) | LSB) >> 4
        if self._pending_msb is None:
            return

        self.update_position((self._pending_msb << 3) | (value >> 4))
        self._pending_msb = None


# ============================================================================
# Hardware
# ============================================================================

#Fader
fader = Fader(0x00, "FADER")

#Encoder
pan = Encoder(0x00, "PAN")

#Transport
rew = Switch(0x03, 0x04, "REWIND", on_press=fp_actions.rewind_start, on_release=fp_actions.rewind_stop)
ffwd = Switch(0x04, 0x03, "FAST_FORWARD", on_press=fp_actions.fast_forward_start, on_release=fp_actions.fast_forward_stop)
stop = Switch(0x05, 0x02, "STOP", on_press=fp_actions.stop)
play = Switch(0x06, 0x01, "PLAY", on_press=fp_actions.play)
record = Switch(0x07, 0x00, "RECORD", on_press=fp_actions.record)

#Automation
read = Switch(0x0A, 0x0D, "READ", on_press=fp_actions.read)
write = Switch(0x09, 0x0E, "WRITE", on_press=fp_actions.write)
touch = Switch(0x08, 0x0F, "TOUCH", on_press=fp_actions.touch)
off = Switch(0x17, 0x10, "OFF", on_press=fp_actions.off)

#Windows
mix = Switch(0x0B, 0x0C, "MIX", on_press=lambda: fp_actions.show_window(fp_constants.WID_MIXER))
proj = Switch(0x0C, 0x0B, "PROJ", on_press=lambda: fp_actions.show_window(fp_constants.WID_CHANNEL_RACK))
trns = Switch(0x0D, 0x0A, "TRNS", on_press=lambda: fp_actions.show_window(fp_constants.WID_PLAYLIST))

#Mixer
mute = Switch(0x12, 0x15, "MUTE", on_press=lambda: fp_actions.mute_track(mixer.trackNumber()))
solo = Switch(0x11, 0x16, "SOLO", on_press=lambda: fp_actions.solo_track(mixer.trackNumber()))
rec = Switch(0x10, 0x17, "REC", on_press=lambda: fp_actions.arm_track(mixer.trackNumber()))
output = Switch(0x16, 0x11, "OUTPUT", on_press=fp_actions.select_output)
left = Switch(0x13, 0x14, "LEFT", on_press=fp_actions.left, auto_repeat=True)
bank = Switch(0x14, 0x13, "BANK", on_press=fp_actions.bank)
right = Switch(0x15, 0x12, "RIGHT", on_press=fp_actions.right, auto_repeat=True)

#Utility
undo = Switch(0x0E, 0x09, "UNDO", on_press=fp_actions.undo)
shift = Switch(0x02, 0x05, "SHIFT", on_press=lambda: fp_modes.set_shift(True), on_release=lambda: fp_modes.set_shift(False))
user = Switch(0x00, 0x07, "USER", on_press=fp_actions.user)
punch = Switch(0x01, 0x06, "PUNCH", on_press=fp_actions.punch_in)
loop = Switch(0x0F, 0x08, "LOOP", on_press=fp_actions.loop)

#Footswith (NO LED)
footswitch = Switch(0x7E, 0x7E, "FOOTSWITCH")


# ============================================================================
# Control collections
# ============================================================================

ALL_SWITCHES = (
    mute,
    solo,
    rec,
    output,
    right,
    bank,
    left,
    read,
    write,
    touch,
    off,
    undo,
    trns,
    proj,
    mix,
    shift,
    punch,
    user,
    loop,
    record,
    play,
    stop,
    ffwd,
    rew,
)

ALL_ENCODERS = (
    pan,
)

ALL_FADERS = (
    fader,
)

SWITCHES = {
    switch.id: switch
    for switch in ALL_SWITCHES
}

ENCODERS = {
    encoder.id: encoder
    for encoder in ALL_ENCODERS
}

FADERS = {
    fader.id: fader
    for fader in ALL_FADERS
}