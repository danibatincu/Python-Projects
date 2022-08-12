import tkinter
import tkinter.ttk
from main import *


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self.wait_time = 100  # milliseconds
        self.wrap_length = 180  # pixels
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
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tkinter.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.tw, text=self.text, justify='left',
                              background="#ffffff", relief='solid', borderwidth=1,
                              wraplength=self.wrap_length)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class MatchUI:
    def __init__(self, player1, player2):
        self.root = tkinter.Tk()
        self.root.title('Match')
        self.root.geometry('800x250+400+300')
        self.root.resizable(False, False)
        self.img = tkinter.PhotoImage()

        s = tkinter.ttk.Style()
        s.theme_use('alt')

        self.p1 = player1
        self.p2 = player2

        self.match = Match(self.p1, self.p2)

        # define the hp bar and text on top for player 1
        self.p1_hp_canvas = tkinter.Canvas(self.root, width=300, height=25, relief='flat')
        self.p1_red_bar = self.p1_hp_canvas.create_rectangle(0, 0, 300, 25, fill='red')
        self.p1_green_bar = self.p1_hp_canvas.create_rectangle(0, 0, 300, 25, fill='green')
        self.p1_cyan_bar = self.p1_hp_canvas.create_rectangle(0, 0, 0, 25, fill='#26bfed')
        self.p1_hp_text = \
            self.p1_hp_canvas.create_text(
                150, 12.5, justify=tkinter.CENTER, width=100,
                text=str(self.p1.stats['current_hp']) + " / " + str(self.p1.stats['max_hp']),
                font=("Arial", "11", "bold"), fill='white')
        self.p1_hp_canvas.grid(column=0, row=1, padx=5, pady=5)

        # define the hp bar and text on top for player 2
        self.p2_hp_canvas = tkinter.Canvas(self.root, width=300, height=25, relief='flat')
        self.p2_red_bar = self.p2_hp_canvas.create_rectangle(0, 0, 300, 25, fill='red')
        self.p2_green_bar = self.p2_hp_canvas.create_rectangle(0, 0, 300, 25, fill='green')
        self.p2_cyan_bar = self.p2_hp_canvas.create_rectangle(0, 0, 0, 25, fill='#26bfed')
        self.p2_hp_text = \
            self.p2_hp_canvas.create_text(
                150, 12.5, justify=tkinter.CENTER, width=100,
                text=str(self.p2.stats['current_hp']) + " / " + str(self.p2.stats['max_hp']),
                font=("Arial", "11", "bold"), fill='white')
        self.p2_hp_canvas.grid(column=2, row=1, padx=5, pady=5)

        # create the ability bar for player 1
        self.p1_ability_bar = tkinter.Frame(self.root, width=300, height=100, background="#cccccc")
        self.p1_ability_bar.grid(row=0, column=0, sticky='e', padx=5)
        self.p1_ability_buttons = [
            tkinter.Button(self.p1_ability_bar, image=self.img, compound=tkinter.CENTER,
                           foreground="white",
                           width=30, height=30, font=("Arial", "15", "bold"), command=lambda slot=i: self.step(slot)
                           ) for i in range(len(self.p1.abilities))]

        # add description of the hovered ability button on the ability description canvas
        i = 0
        for label in self.p1_ability_buttons:
            label.bind("<Enter>", lambda event, slot=i: self.set_ability_desc(self.p1, slot))
            label.bind("<Leave>", lambda event: self.empty_ability_desc())
            label.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            i += 1

        # create the ability bar for player 2
        self.p2_ability_bar = tkinter.Frame(self.root, width=300, height=100, background="#cccccc")
        self.p2_ability_bar.grid(row=0, column=2, sticky='w', padx=5)
        self.p2_ability_buttons = [
            tkinter.Button(self.p2_ability_bar, image=self.img, compound=tkinter.CENTER,
                           foreground="white",
                           width=30, height=30, font=("Arial", "15", "bold"), command=lambda slot=i: self.step(slot)
                           ) for i in range(len(self.p2.abilities))]

        # add description of the hovered ability button on the ability description canvas
        i = 0
        for label in self.p2_ability_buttons:
            label.bind("<Enter>", lambda event, slot=i: self.set_ability_desc(self.p2, slot))
            label.bind("<Leave>", lambda event: self.empty_ability_desc())
            label.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            i += 1

        # create the ability description canvas with 2 Text items, a name and a description
        self.desc_canvas = tkinter.Canvas(self.root, width=172, height=80, background='#cccccc')
        self.desc_canvas.grid(column=1, row=0)
        self.ability_name = self.desc_canvas.create_text(5, 5, text="", width=162, anchor="nw",
                                                         font=("Calibri", 10, "bold"))
        self.ability_desc = self.desc_canvas.create_text(5, 20, text="", width=162, anchor='nw',
                                                         font=("Calibri", 10, "normal"))

        self.manage_ability_buttons()

        # an area between the 2 health bars that shows after every turn the health gained/lost
        self.hp_change_canvas = tkinter.Canvas(self.root, width=172, height=40, background='#cccccc')
        self.hp_change_canvas.grid(column=1, row=1)
        self.p1_hp_change_text = self.hp_change_canvas.create_text(12, 20, text="", width=162, anchor="w",
                                                                   font=("Calibri", 12, "normal"), fill="red")
        self.p2_hp_change_text = self.hp_change_canvas.create_text(162, 20, text="", width=162, anchor='e',
                                                                   font=("Calibri", 12, "normal"), fill="green")

        # a frame that contains the buffs of player 1, underneath the hp bar
        self.p1_buff_frame = tkinter.Frame(self.root, background='#cccccc', width=300, height=26)
        self.p1_buff_frame.grid(row=2, column=0)
        self.p1_buff_frame.pack_propagate(False)
        self.p1_buff_labels = []

        # a frame that contains the buffs of player 2, underneath the hp bar
        self.p2_buff_frame = tkinter.Frame(self.root, background='#cccccc', width=300, height=26)
        self.p2_buff_frame.grid(row=2, column=2)
        self.p2_buff_frame.pack_propagate(False)
        self.p2_buff_labels = []

        # a frame that contains the debuffs of player 1, underneath the buffs frame
        self.p1_debuff_frame = tkinter.Frame(self.root, background='#cccccc', width=300, height=26)
        self.p1_debuff_frame.grid(row=3, column=0)
        self.p1_debuff_frame.pack_propagate(False)
        self.p1_debuff_labels = []

        # a frame that contains the debuffs of player 2, underneath the buffs frame
        self.p2_debuff_frame = tkinter.Frame(self.root, background='#cccccc', width=300, height=26)
        self.p2_debuff_frame.grid(row=3, column=2)
        self.p2_debuff_frame.pack_propagate(False)
        self.p2_debuff_labels = []

        self.root.mainloop()

    '''
        set hovered ability name and description in the description canvas
    '''
    def set_ability_desc(self, player, slot):

        self.desc_canvas.itemconfigure(self.ability_name,
                                       text=player.abilities[slot].name)
        self.desc_canvas.itemconfigure(self.ability_desc,
                                       text=player.abilities[slot].desc)

    '''
        empty the description canvas
    '''
    def empty_ability_desc(self):
        self.desc_canvas.itemconfigure(self.ability_desc, text="")
        self.desc_canvas.itemconfigure(self.ability_name, text="")

    '''
        empty the hp change canvas
    '''
    def empty_hp_change_canvas(self):
        self.hp_change_canvas.itemconfigure(self.p1_hp_change_text, text="")
        self.hp_change_canvas.itemconfigure(self.p2_hp_change_text, text="")

    '''
        called after every turn, changes the green hp bar and value in the hp change canvas for player 1
    '''
    def update_player1_hp(self, current_hp, message=""):
        x0, y0, x1, y1 = self.p1_hp_canvas.coords(self.p1_green_bar)
        x1 -= 300 * min(1,
                        ((current_hp - self.match.player1.stats['current_hp']) / self.match.player1.stats['max_hp']))
        self.p1_hp_canvas.coords(self.p1_green_bar, x0, y0, x1, y1)
        hp_difference = current_hp - self.match.player1.stats['current_hp']
        if hp_difference > 0:
            to_print = "-" + str(hp_difference)
            color = "red"
        elif hp_difference == 0:
            to_print = str(abs(hp_difference))
            color = "gray"
        else:
            to_print = "+" + str(abs(hp_difference))
            color = "green"
        to_print += " " + message
        if hp_difference != 0 or message:
            self.hp_change_canvas.itemconfigure(self.p1_hp_change_text, text=to_print, fill=color)
        return x1

    '''
        set the size of the shield bar on the hp bar for player 1
    '''
    def update_player1_shield(self, hp_x1):
        sx0, sy0, sx1, sy1 = self.p1_hp_canvas.coords(self.p1_cyan_bar)
        shield_length = \
            300 * (self.match.player1.stats['shield'] / self.match.player1.stats['max_hp'])
        sx0 = min(hp_x1, 300 - shield_length)
        sx1 = min(sx0 + shield_length, 300)
        self.p1_hp_canvas.coords(self.p1_cyan_bar, sx0, sy0, sx1, sy1)

    '''
        called after every turn, changes the green hp bar and value in the hp change canvas for player 2
    '''
    def update_player2_hp(self, current_hp, message=""):
        x0, y0, x1, y1 = self.p2_hp_canvas.coords(self.p2_green_bar)
        x0 += 300 * min(1,
                        ((current_hp - self.match.player2.stats['current_hp']) / self.match.player2.stats['max_hp']))
        self.p2_hp_canvas.coords(self.p2_green_bar, x0, y0, x1, y1)
        hp_difference = current_hp - self.match.player2.stats['current_hp']
        if hp_difference > 0:
            to_print = "-" + str(hp_difference)
            color = "red"
        elif hp_difference == 0:
            to_print = str(abs(hp_difference))
            color = "gray"
        else:
            to_print = "+" + str(abs(hp_difference))
            color = "green"
        to_print = message + " " + to_print
        if hp_difference != 0 or message:
            self.hp_change_canvas.itemconfigure(self.p2_hp_change_text, text=to_print, fill=color)
        return x0

    '''
        set the size of the shield bar on the hp bar for player 2
    '''
    def update_player2_shield(self, hp_x0):
        sx0, sy0, sx1, sy1 = self.p2_hp_canvas.coords(self.p2_cyan_bar)
        shield_length = \
            300 * (self.match.player2.stats['shield'] / self.match.player2.stats['max_hp'])
        sx1 = max(hp_x0, shield_length)
        sx0 = max(sx1 - shield_length, 0)
        self.p2_hp_canvas.coords(self.p2_cyan_bar, sx0, sy0, sx1, sy1)

    '''
        updates a player's buff frame
    '''
    def handle_player_effects(self, frame, buff_labels, effects, side):
        for label in buff_labels:
            label.destroy()
        buff_labels = [
            tkinter.Label(frame, image=self.img, compound=tkinter.CENTER, background='black', width=20,
                          height=20) for _ in range(len(effects))]
        i = 0
        for label in buff_labels:
            CreateToolTip(label, str(effects[i]))
            label.pack(side=side, padx=3, pady=3, anchor=tkinter.N)
            i += 1
        return buff_labels

    '''
        manage active/inactive/on cooldown buttons and cooldowns
    '''
    def manage_ability_buttons(self):
        if not self.match.tp:
            i = 0
            for button in self.p2_ability_buttons:
                button['state'] = tkinter.DISABLED
                button['background'] = 'gray'
                ability_current_cooldown = self.match.player2.abilities[i].current_cooldown
                to_print = str(ability_current_cooldown) if ability_current_cooldown > 0 else ""
                button.configure(text=to_print)
                i += 1
            i = 0
            for button in self.p1_ability_buttons:
                if not self.match.player1.abilities[i].active:
                    button['state'] = tkinter.DISABLED
                    button['background'] = 'red'
                    ability_current_cooldown = self.match.player1.abilities[i].current_cooldown
                    to_print = str(ability_current_cooldown) if ability_current_cooldown > 0 else ""
                    button.configure(text=to_print)
                else:
                    button['state'] = tkinter.NORMAL
                    button['background'] = 'green'
                i += 1
        else:
            i = 0
            for button in self.p1_ability_buttons:
                button['state'] = tkinter.DISABLED
                button['background'] = 'gray'
                ability_current_cooldown = self.match.player1.abilities[i].current_cooldown
                to_print = str(ability_current_cooldown) if ability_current_cooldown > 0 else ""
                button.configure(text=to_print)
                i += 1
            i = 0
            for button in self.p2_ability_buttons:
                if not self.match.player2.abilities[i].active:
                    button['state'] = tkinter.DISABLED
                    button['background'] = 'red'
                    ability_current_cooldown = self.match.player2.abilities[i].current_cooldown
                    to_print = str(ability_current_cooldown) if ability_current_cooldown > 0 else ""
                    button.configure(text=to_print)
                else:
                    button['state'] = tkinter.NORMAL
                    button['background'] = 'green'
                i += 1

    '''
        a turn/round of the game
    '''
    def step(self, slot):
        if self.match.game_over():
            return
        p1_current_hp = self.match.player1.stats['current_hp']
        p2_current_hp = self.match.player2.stats['current_hp']

        self.empty_hp_change_canvas()
        message = self.match.play_round_manual(slot)
        self.manage_ability_buttons()

        if self.match.tp:
            if not message:
                split_message = ["", ""]
                m = ""
            else:
                split_message = message.split(" ")
                m = split_message[1] if split_message[0] == "+" else ""
            x1 = self.update_player1_hp(p1_current_hp, m)
            self.update_player1_shield(x1)
            x0 = self.update_player2_hp(p2_current_hp, split_message[1])
            self.update_player2_shield(x0)
        else:
            if not message:
                split_message = ["", ""]
                m = ""
            else:
                split_message = message.split(" ")
                m = split_message[1] if split_message[0] == "+" else ""
            x1 = self.update_player1_hp(p1_current_hp, split_message[1])
            self.update_player1_shield(x1)
            x0 = self.update_player2_hp(p2_current_hp, m)
            self.update_player2_shield(x0)

        hp_to_show = str(self.p1.stats['current_hp']) + " / " + str(self.p1.stats['max_hp'])
        if self.p1.stats['shield'] != 0:
            hp_to_show += " (+" + str(self.p1.stats['shield']) + ")"
        self.p1_hp_canvas.itemconfigure(
            self.p1_hp_text, text=hp_to_show)

        hp_to_show = str(self.p2.stats['current_hp']) + " / " + str(self.p2.stats['max_hp'])
        if self.p2.stats['shield'] != 0:
            hp_to_show += " (+" + str(self.p2.stats['shield']) + ")"
        self.p2_hp_canvas.itemconfigure(
            self.p2_hp_text, text=hp_to_show)

        self.p1_buff_labels = \
            self.handle_player_effects(self.p1_buff_frame, self.p1_buff_labels, self.match.player1.buffs, tkinter.LEFT)
        self.p2_buff_labels = \
            self.handle_player_effects(self.p2_buff_frame, self.p2_buff_labels, self.match.player2.buffs, tkinter.RIGHT)

        self.p1_debuff_labels = \
            self.handle_player_effects(
                self.p1_debuff_frame, self.p1_debuff_labels, self.match.player1.debuffs, tkinter.LEFT)
        self.p2_debuff_labels = \
            self.handle_player_effects(
                self.p2_debuff_frame, self.p2_debuff_labels, self.match.player2.debuffs, tkinter.RIGHT)

        self.root.update_idletasks()


if __name__ == '__main__':
    p1 = Player("GregorOP", Mage())
    p1.add_ability("Mana Shield")

    p2 = Player("Billy", Bruiser())
    p2.add_ability("Adrenaline")

    ui = MatchUI(p1, p2)
