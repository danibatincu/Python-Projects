from Player.Player import *
from Player.PlayerClasses import *
import tkinter
import random
import pickle


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self.wait_time = 100  # milliseconds
        self.wrap_length = 175  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter, add='+')
        self.widget.bind("<Leave>", self.leave, add='+')
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.wait_time, self.showtip)

    def unschedule(self):
        idd = self.id
        self.id = None
        if idd:
            self.widget.after_cancel(idd)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 37
        y += self.widget.winfo_rooty() + 30
        # creates a toplevel window
        self.tw = tkinter.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.tw, text=self.text, justify='left',
                              background="#ffffff", relief='solid', borderwidth=1,
                              wraplength=self.wrap_length, font=("Calibri", 12, "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


player_presets = {"Gregory": Player("Gregory", Assassin(), "./Portraits/gregory.png"),
                  "Billy": Player("Billy", Bruiser(), "./Portraits/billy.png"),
                  "Presto": Player("Presto", Priest(), "./Portraits/presto.png"),
                  "Mez": Player("Mez", Mage(), "./Portraits/mez.png")}
player_presets["Gregory"].add_ability("Vanish")
player_presets["Gregory"].add_ability("Crippling Poison")
player_presets["Billy"].add_ability("Adrenaline")
player_presets["Billy"].add_ability("Aim")
player_presets["Presto"].add_ability("Heal")
player_presets["Presto"].add_ability("Curse of Weakness")
player_presets["Mez"].add_ability("Mana Shield")
player_presets["Mez"].add_ability("Life-stealing Firebolt")

