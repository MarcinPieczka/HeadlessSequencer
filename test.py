import alsaseq
from alsamidi import *
from time import sleep
from tkinter import Tk, Label, Button
import threading
from time import time
from sortedcontainers import SortedListWithKey

step_mapping = {
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    'q': 8,
    'w': 9,
    'e': 10,
    'r': 11,
    't': 12,
    'y': 13,
    'u': 14,
    'i': 15,
}
note_mapping = {
    'z': 0,
    's': 1,
    'x': 2,
    'd': 3,
    'c': 4,
    'v': 5,
    'g': 6,
    'b': 7,
    'h': 8,
    'n': 9,
    'j': 10,
    'm': 11,
}

class MyFirstGUI:
    def __init__(self, master, seq):
        self.master = master
        master.minsize(width=600, height=400)
        master.title("A simple GUI")
        master.bind('<Key>', self.key_press)

        self.label = Label(master, text="SickSeq")
        self.label.pack()

        self.step = 1
        self.base_note = 24
        self.track = 0 

    def key_press(self, event):
        global patterns
        if event.keysym in note_mapping.keys():
            patterns[self.track].pattern[self.step][0][0] = self.base_note + note_mapping[event.keysym]
            print(patterns[self.track].pattern[self.step])
        if event.keysym == 'less':
            patterns[self.track].pattern[self.step][0][0] = None
        elif event.keysym in step_mapping.keys():
            self.step = step_mapping[event.keysym]
        print(event.keysym)

class Sequencer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False

    def run(self):
        alsaseq.client( 'Simple', 1, 1, False )
        alsaseq.start()
        global patterns

        while True:
            if self.stop:
                alsaseq.stop()
                break
            note_off_player.play_note()
            for pattern in patterns:
                pattern.play_note()


class Pattern():
    def __init__(self, note_off_player):
        self.note_off_player = note_off_player
        self.set_tempo(120)
        self.pattern = [([None], 100, 1) for _ in range(64)]  # notes, velocity, length
        self.length = 16
        self.i = 0
        self.count = 0
        self.start_time = None
        self.is_running = False
        self.channel = 0

    def set_tempo(self, tempo):
        self.tempo = tempo
        self.between = (1/(tempo/60))/4 # time between notes in seconds

    def start(self):
        self.start_time = time()
        self.is_running = True

    def pause(self):
        self.is_running = False

    def stop(self):
        self.is_running = False
        self.start_time = None
        self.count = 0
        self.i = 0

    def play_note(self):
        #for x in self.pattern:
        #    if x[0] != [None]:
        #        print(self.pattern)
        if self.is_running and self.it_is_time_to_play_note():
            #print(self.pattern)
            for note in self.pattern[self.i][0]:
                if note:
                    self.note_on(note, self.pattern[self.i][1])
                    self.note_off_player.add(self.channel, note, self.pattern[self.i][1], self.pattern[self.i][2] *
                            self.between + time() )
            self.i = (self.i + 1) % self.length
            self.count = self.count + 1


    def it_is_time_to_play_note(self):
        #print(self.start_time + self.count * self.between, time())

        return self.start_time + self.count * self.between <= time()

    def note_on(self, note, velocity):
        alsaseq.output(noteonevent(self.channel, note, velocity))

class NoteOffPlayer():
    notes = SortedListWithKey(key=lambda x: x[3])

    def add(self, channel, note, vel, ttplay):
        notes.add((channel, note, vel, ttplay))

    def play_note(self):
        if self.notes and time() >= self.notes[0][3]:
            alsaseq.output(noteoffevent(self.notes[0][:3]))
            del self.notes[0]
            self.play_note()

def closing():
    seq.stop = True
    root.destroy()


#starting program
note_off_player = NoteOffPlayer()
patterns = [Pattern(note_off_player) for _ in range(9)]
for p in patterns:
    p.start()

root = Tk()
root.protocol('WM_DELETE_WINDOW', closing)
seq = Sequencer()
my_gui = MyFirstGUI(root, seq)
seq.start()
root.mainloop()
seq.join()
