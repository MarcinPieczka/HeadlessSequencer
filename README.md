# HeadlessSequencer
main goall, create MIDI sequencer that will be operated only via keyboard
it will operate similarly to 303 sequencer, but will be 8 or 9 track, 
keys 1-8 and q-i will be 16 steps, 
keys z-m will be whithe keyboard keys, black keys s, d, g, h, j
square of keys of side length 3 starting with key 9 in upper left corner will be track selectors.

Basic functionality: pick track, pick step, select note.
then chords, note length, maybe volume and length set by trackpad.

Extra:
create cc send with trackpad as knob, and cc type choosing via keyboard

lounching patterns once

possibility of inserting pattern in place of note, it will play once and with speed determined by note length, and maybe transposed by note

Libraries considered for midi support:
- alsaseq
