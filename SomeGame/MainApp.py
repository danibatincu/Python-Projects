import copy
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
        self.frames[cont].tkraise()

    def set_player(self, player):
        self.p1 = player


if __name__ == '__main__':

    p1 = PlayableCharacter("Bulliette", Bruiser(), "./Portraits/billy.png")
    p1.add_ability("Aim")
    with open("./Saves/save1.pickle", "wb") as f:
        pickle.dump(p1, f)

    p2 = PlayableCharacter("Merlin", Mage(), "./Portraits/mez.png")
    p2.add_ability("Life-stealing Firebolt")
    with open("./Saves/save2.pickle", "wb") as f:
        pickle.dump(p2, f)

    app = MainApp()
    app.mainloop()
