import copy

from Pages.InventoryPage import InventoryPage
from Pages.StartPage import StartPage
from Pages.FirstPage import FirstPage
from Pages.LoadGamePage import LoadGamePage
from Pages.NewGamePage import NewGamePage
from Pages.MatchPage import MatchPage
from utils import *


class MainApp(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.p1 = None
        self.p2 = None

        self.save_name = None

        self.title('Match')
        self.geometry('1200x650+170+100')
        self.resizable(False, False)

        self.container = tkinter.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, FirstPage, NewGamePage, LoadGamePage):
            page_name = F.__name__
            frame = F(self.container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("FirstPage")

    def show_frame(self, cont):
        if cont == "MatchPage":
            self.p2 = copy.deepcopy(player_presets[random.choice(list(player_presets.keys()))])
            frame = MatchPage(self.container, self, copy.deepcopy(self.p1), self.p2)
            self.frames["MatchPage"] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        if cont == "LoadGamePage":
            frame = LoadGamePage(self.container, self)
            self.frames["LoadGamePage"] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        if cont == "InventoryPage":
            frame = InventoryPage(self.container, self)
            self.frames["InventoryPage"] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.frames[cont].tkraise()

    def set_player(self, player):
        self.p1 = player

    def set_save_file(self, save_file):
        self.save_name = save_file

    def set_item_inv_slot(self, row, col, item):
        self.p1.set_item_inv_slot(row, col, item)


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
