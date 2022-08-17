import os
import tkinter.ttk
from utils import *


class NewGamePage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        label = tkinter.ttk.Label(self, text="Select a class", font=("Calibri", 48, "bold"))
        label.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        back_button = tkinter.Button(self, text="Back", font=("Calibri", 20, "bold"), width=20,
                                     command=lambda: controller.show_frame("FirstPage"))
        back_button.place(relx=0.5, rely=0.85, anchor="center")

        self.canvas = tkinter.Canvas(self, width=label.winfo_reqwidth(), height=275, background="#cccccc")
        self.canvas.place(relx=0.52, y=360, anchor=tkinter.W)
        self.text = self.canvas.create_text(10, 10, text="", anchor="nw",
                                            width=label.winfo_reqwidth() - 20, font=("Calibri", 16, "normal"))

        button1 = tkinter.Button(self, text="Assassin", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: self.set_player(Assassin))
        button1.place(relx=0.48, y=250, anchor=tkinter.E)
        button1.bind("<Enter>", lambda event: self.update_text(Assassin.description()))
        button1.bind("<Leave>", lambda event: self.update_text(""))

        button2 = tkinter.Button(self, text="Bruiser", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: self.set_player(Bruiser))
        button2.place(relx=0.48, y=325, anchor=tkinter.E)
        button2.bind("<Enter>", lambda event: self.update_text(Bruiser.description()))
        button2.bind("<Leave>", lambda event: self.update_text(""))

        button3 = tkinter.Button(self, text="Priest", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: self.set_player(Priest))
        button3.place(relx=0.48, y=400, anchor=tkinter.E)
        button3.bind("<Enter>", lambda event: self.update_text(Priest.description()))
        button3.bind("<Leave>", lambda event: self.update_text(""))

        button4 = tkinter.Button(self, text="Mage", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: self.set_player(Mage))
        button4.place(relx=0.48, y=475, anchor=tkinter.E)
        button4.bind("<Enter>", lambda event: self.update_text(Mage.description()))
        button4.bind("<Leave>", lambda event: self.update_text(""))

    def update_text(self, text):
        self.canvas.itemconfigure(self.text, text=text)

    def set_player(self, player_class):
        p = PlayableCharacter("Roger", player_class(), "./Portraits/roger.jpg")
        self.controller.set_player(p)
        self.create_save()
        self.controller.show_frame("StartPage")

    def create_save(self):
        if len(os.listdir("./Saves/")) == 0:
            save_file = "0.pickle"
        else:
            print(os.listdir("./Saves/")[-1].split(".")[0])
            save_file = str(int(os.listdir("./Saves/")[-1].split(".")[0][-1]) + 1) + ".pickle"
        self.controller.set_save_file(save_file)
        with open("./Saves/save" + save_file, "wb") as f:
            pickle.dump(self.controller.p1, f)
