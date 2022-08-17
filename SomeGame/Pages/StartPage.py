import tkinter.ttk
from utils import *


class StartPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.controller = controller

        label = tkinter.ttk.Label(self, text="SomeGame", font=("Calibri", 48, "bold"))
        label2 = tkinter.ttk.Label(self, text="GameSome", font=("Calibri", 48, "bold"))

        button1 = tkinter.Button(self, text="Match", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: controller.show_frame("MatchPage"))
        button1.place(x=600, y=300, anchor=tkinter.CENTER)

        inventory_button = tkinter.Button(self, text="Inventory", font=("Calibri", 20, "bold"), width=20,
                                          command=lambda: controller.show_frame("InventoryPage"))
        inventory_button.place(x=600, y=375, anchor=tkinter.CENTER)

        button2 = tkinter.Button(self, text="Save Game", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: self.save_game())
        button2.place(x=600, y=450, anchor=tkinter.CENTER)

        button3 = tkinter.Button(self, text="Delete Save", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: self.delete_save())
        button3.place(x=600, y=525, anchor=tkinter.CENTER)

        button4 = tkinter.Button(self, text="Back", font=("Calibri", 20, "bold"), width=20,
                                 command=lambda: controller.show_frame("FirstPage"))
        button4.place(x=600, y=600, anchor=tkinter.CENTER)

        frame_width = label.winfo_reqwidth()
        frame_height = label.winfo_reqheight()

        for i in range(3):
            frame = tkinter.Frame(self, width=frame_width,
                                  height=frame_height, borderwidth=1, relief="solid")
            frame.place(x=250 + i * 350, y=175, anchor="center")

        label.place(x=600, y=175, anchor=tkinter.CENTER)
        label.lift()
        label2.place(x=250, y=175, anchor=tkinter.CENTER)
        label2.lift()

        self.current_old_x = 0
        self.current_old_y = 0

        label.bind("<Button-1>", self.clicked_for_drag)
        label.bind("<B1-Motion>", self.drag)
        label.bind("<ButtonRelease-1>", self.drop)

        label2.bind("<Button-1>", self.clicked_for_drag)
        label2.bind("<B1-Motion>", self.drag)
        label2.bind("<ButtonRelease-1>", self.drop)

    def save_game(self):
        with open("./Saves/" + self.controller.save_name, "wb") as f:
            pickle.dump(self.controller.p1, f)

    def delete_save(self):
        os.remove("./Saves/" + self.controller.save_name)
        self.controller.save_name = None
        self.controller.show_frame("FirstPage")

    def clicked_for_drag(self, event):
        self.current_old_x = event.widget.winfo_x()
        self.current_old_y = event.widget.winfo_y()

    @staticmethod
    def drag(event):
        event.widget.lower()
        x = event.x + event.widget.winfo_x()
        y = event.y + event.widget.winfo_y()
        event.widget.place(x=x, y=y, anchor="center")
        event.widget.lift()

    def drop(self, event):
        event.widget.lower()
        x, y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x, y)
        if isinstance(target, tkinter.Frame):
            new_x = target.winfo_x() + target.winfo_reqwidth() // 2
            new_y = target.winfo_y() + target.winfo_reqheight() // 2
            self.current_old_x = new_x
            self.current_old_y = new_y
            event.widget.place(x=new_x, y=new_y, anchor="center")
            event.widget.lift()
            return
        event.widget.place(x=self.current_old_x, y=self.current_old_y, anchor="nw")
        event.widget.lift()
