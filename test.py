import alsaseq
from alsamidi import *
from time import sleep
from tkinter import Tk, Label, Button
import threading

patterns = [0 for _ in range(8)]

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

class Sequencer(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        alsaseq.client( 'Simple', 1, 1, False )
        alsaseq.start()

        while True:
            for note in patterns:
                note_tuple = (1, note, 100)
                alsaseq.output(noteonevent(*note_tuple))
                sleep(0.2)
                alsaseq.output(noteoffevent(*note_tuple))


root = Tk()
my_gui = MyFirstGUI(root)
seq = Sequencer('seq')
seq.start()
root.mainloop()
seq.join()
