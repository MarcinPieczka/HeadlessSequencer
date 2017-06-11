import alsaseq
from alsamidi import *
from time import sleep
from tkinter import Tk, Label, Button
import threading

patterns = [40 for _ in range(8)]

class MyFirstGUI:
    def __init__(self, master, seq):
        self.master = master
        master.minsize(width=600, height=400)
        master.title("A simple GUI")
        master.bind('<Key>', self.key_press)

        self.label = Label(master, text="SickSeq")
        self.label.pack()

    def key_press(self, event):
        global patterns
        patterns = [x - 1 for x in patterns]
        print(event)

class Sequencer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False

    def run(self):
        alsaseq.client( 'Simple', 1, 1, False )
        alsaseq.start()
        global patterns

        while True:
            print('jestem')
            if self.stop:
                alsaseq.stop()
                break
            for note in patterns:
                note_tuple = (0, note, 100)
                print(noteonevent(*note_tuple))
                #alsaseq.output((6, 1, 0, 1, (5, 0), (0, 0), (0, 0), (0, 60, 127, 0, 100)))
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
