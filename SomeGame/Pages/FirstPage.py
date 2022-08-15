import tkinter
import tkinter.ttk


class FirstPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        label = tkinter.ttk.Label(self, text="SomeGame", font=("Calibri", 48, "bold"))
        label.place(x=600, y=175, anchor=tkinter.CENTER)

        button1 = tkinter.Button(self, text="New Game", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: controller.show_frame("NewGamePage"))
        button1.place(x=600, y=325, anchor=tkinter.CENTER)

        button2 = tkinter.Button(self, text="Load Game", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: controller.show_frame("LoadGamePage"))
        button2.place(x=600, y=400, anchor=tkinter.CENTER)
