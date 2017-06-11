import alsaseq
from alsamidi import *
from time import sleep
from tkinter import Tk, Label, Button
import threading

patterns = [40 for _ in range(16)]
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

    def key_press(self, event):
        global patterns
        if event.keysym in note_mapping.keys():
            patterns[self.step] = self.base_note + note_mapping[event.keysym]
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
            for note in patterns:
                note_tuple = (0, note, 100)
                alsaseq.output(noteonevent(*note_tuple))
                sleep(0.2)
                alsaseq.output(noteoffevent(*note_tuple))



def closing():
    seq.stop = True
    root.destroy()

root = Tk()
root.protocol('WM_DELETE_WINDOW', closing)
seq = Sequencer()
my_gui = MyFirstGUI(root, seq)
seq.start()
root.mainloop()
seq.join()
