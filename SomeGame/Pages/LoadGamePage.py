import tkinter.ttk
import os
from utils import *


class LoadGamePage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        label = tkinter.ttk.Label(self, text="Select a character", font=("Calibri", 48, "bold"))
        label.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.saves = []

        for filename in os.listdir("./Saves/"):
            with open("./Saves/" + filename, "rb") as f:
                p = pickle.load(f)
                if isinstance(p, PlayableCharacter):
                    self.saves.append(p)

        i = 0
        for i in range(len(self.saves)):
            button = tkinter.Button(self, text=str(self.saves[i]), font=("Calibri", 20, "bold"), width=25,
                                    command=lambda slot=i: self.set_player(slot))
            button.place(relx=0.5, y=250 + i * 75, anchor=tkinter.CENTER)

    def set_player(self, slot):
        self.controller.set_player(self.saves[slot])
        self.controller.show_frame("StartPage")
