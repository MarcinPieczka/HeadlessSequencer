import rtmidi
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, PROGRAM_CHANGE


class MidiOutWrapper:
    def __init__(self):
        self.channel = 1
        self.midi = rtmidi.MidiOut()
        self.midi.open_virtual_port()

    def channel_message(self, command, *data, ch=None):
        """Send a MIDI channel mode message."""
        command = (command & 0xf0) | ((ch if ch else self.channel) - 1 & 0xf)
        msg = [command] + [value & 0x7f for value in data]
        self.midi.send_message(msg)

    def note_off(self, note, velocity=0, ch=None):
        """Send a 'Note Off' message."""
        self.channel_message(NOTE_OFF, note, velocity, ch=ch)

    def note_on(self, note, velocity=127, ch=None):
        """Send a 'Note On' message."""
        self.channel_message(NOTE_ON, note, velocity, ch=ch)

    def program_change(self, program, ch=None):
        """Send a 'Program Change' message."""
        self.channel_message(PROGRAM_CHANGE, program, ch=ch)

