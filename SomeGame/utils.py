from Player.Player import *
from Player.PlayerClasses import *
import tkinter
import os
import random
import pickle
import copy


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
        self.widget.bind("<B1-Motion>", self.leave, add="+")
        self.widget.bind("<ButtonRelease-1>", self.enter, add='+')
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

gear_presets = [Gear("Default helmet", "head", 1, {"strength": 1}, "./ItemPortraits/default_helmet.jpg"),
                Gear("Default shoulder piece", "shoulder", 1, {"strength": 1}, "./ItemPortraits/default_shoulder.jpg"),
                Gear("Default chest piece", "chest", 1, {"strength": 1}, "./ItemPortraits/default_chest.jpg"),
                Gear("Default gloves", "hands", 1, {"strength": 1}, "./ItemPortraits/default_gloves.jpg"),
                Gear("Default pants", "legs", 1, {"strength": 1}, "./ItemPortraits/default_legs.jpg"),
                Gear("Default boots", "feet", 1, {"strength": 1}, "./ItemPortraits/default_boots.jpg"),
                Gear("Default 1-handed sword", "main_hand", 1, {"strength": 1}, "./ItemPortraits/default_sword.jpg"),
                Gear("Default 1-handed sword", "off_hand", 1, {"strength": 1}, "./ItemPortraits/default_sword.jpg")]

