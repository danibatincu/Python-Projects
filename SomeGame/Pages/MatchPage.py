import tkinter.ttk
import tkinter.messagebox
from PIL import ImageTk, Image
from PIL.Image import LANCZOS
from Player.Match import Match
from utils import *


class MatchPage(tkinter.Frame):
    def __init__(self, parent, controller, player1, player2):
        super().__init__(parent)
        self.root = self

        self.controller = controller
        # self.root.title('Match')
        # self.root.geometry('1200x600+170+150')
        # self.root.resizable(False, False)
        self.img = tkinter.PhotoImage()

        s = tkinter.ttk.Style()
        s.theme_use('alt')

        self.p1 = player1
        self.p2 = player2

        self.match = Match(self.p1, self.p2)

        # define the hp bar and text on top for player 1
        self.p1_hp_canvas = tkinter.Canvas(self.root, width=450, height=37, relief='flat')
        self.p1_red_bar = self.p1_hp_canvas.create_rectangle(0, 0, 450, 37, fill='red')
        self.p1_green_bar = self.p1_hp_canvas.create_rectangle(0, 0, 450, 37, fill='green')
        self.p1_cyan_bar = self.p1_hp_canvas.create_rectangle(0, 0, 0, 37, fill='#26bfed')
        self.p1_hp_text = \
            self.p1_hp_canvas.create_text(
                225, 18.5, justify=tkinter.CENTER, width=150,
                text=str(self.p1.stats['current_hp']) + " / " + str(self.p1.stats['max_hp']),
                font=("Arial", "16", "bold"), fill='white')
        self.p1_hp_canvas.grid(column=0, row=2, padx=7, pady=7)

        # define the hp bar and text on top for player 2
        self.p2_hp_canvas = tkinter.Canvas(self.root, width=450, height=37, relief='flat')
        self.p2_red_bar = self.p2_hp_canvas.create_rectangle(0, 0, 450, 37, fill='red')
        self.p2_green_bar = self.p2_hp_canvas.create_rectangle(0, 0, 450, 37, fill='green')
        self.p2_cyan_bar = self.p2_hp_canvas.create_rectangle(0, 0, 0, 37, fill='#26bfed')
        self.p2_hp_text = \
            self.p2_hp_canvas.create_text(
                225, 18.5, justify=tkinter.CENTER, width=150,
                text=str(self.p2.stats['current_hp']) + " / " + str(self.p2.stats['max_hp']),
                font=("Arial", "16", "bold"), fill='white')
        self.p2_hp_canvas.grid(column=2, row=2, padx=7, pady=7)

        # create the ability bar for player 1
        self.p1_frame = tkinter.Frame(self.root, width=450, height=150, background="#dddddd")
        self.p1_ability_bar = tkinter.Frame(self.p1_frame, width=225, height=150, background="#cccccc")
        self.p1_frame.pack_propagate(False)

        image1 = Image.open(self.match.player1.photo)
        image1 = image1.resize((150, 150), LANCZOS)
        self.photo1 = ImageTk.PhotoImage(image1)
        self.player1_photo = tkinter.Label(self.p1_frame, image=self.photo1, width=150, height=150)

        self.p1_frame.grid(row=0, column=0, sticky=tkinter.S, pady=(0, 7))
        self.player1_photo.pack(side="left")
        self.p1_ability_bar.pack(side="right")

        self.p1_ability_buttons = [
            tkinter.Button(self.p1_ability_bar, image=self.img, compound=tkinter.CENTER,
                           foreground="white",
                           width=45, height=45, font=("Arial", "22", "bold"), command=lambda slot=i: self.step(slot)
                           ) for i in range(len(self.p1.abilities))]

        # add description of the hovered ability button on the ability description canvas
        i = 0
        for label in self.p1_ability_buttons:
            label.bind("<Enter>", lambda event, slot=i: self.set_ability_desc(self.p1, slot))
            label.bind("<Leave>", lambda event: self.empty_ability_desc())
            label.grid(row=i // 4, column=i % 4, padx=7, pady=7)
            i += 1

        # create the ability bar for player 2
        self.p2_frame = tkinter.Frame(self.root, width=450, height=150, background="#dddddd")
        self.p2_ability_bar = tkinter.Frame(self.p2_frame, width=225, height=150, background="#cccccc")
        self.p2_frame.pack_propagate(False)

        image2 = Image.open(self.match.player2.photo)
        image2 = image2.resize((150, 150), LANCZOS)
        self.photo2 = ImageTk.PhotoImage(image2)
        self.player2_photo = tkinter.Label(self.p2_frame, image=self.photo2, width=150, height=150)

        self.p2_frame.grid(row=0, column=2, sticky=tkinter.S, pady=(0, 7))
        self.player2_photo.pack(side="right")
        self.p2_ability_bar.pack(side="left")

        self.p2_ability_buttons = [
            tkinter.Button(self.p2_ability_bar, image=self.img, compound=tkinter.CENTER,
                           foreground="white",
                           width=40, height=40, font=("Arial", "22", "bold"), command=lambda slot=i: self.step(slot)
                           ) for i in range(len(self.p2.abilities))]

        # add description of the hovered ability button on the ability description canvas
        i = 0
        for label in self.p2_ability_buttons:
            label.bind("<Enter>", lambda event, slot=i: self.set_ability_desc(self.p2, slot))
            label.bind("<Leave>", lambda event: self.empty_ability_desc())
            label.grid(row=i // 4, column=i % 4, padx=7, pady=7)
            i += 1

        self.names_frame = tkinter.Frame(self.root, height=30, width=1158)
        self.p1_name = tkinter.Label(self.names_frame, text=str(self.match.player1), font=("Calibri", 18, "bold"))
        self.p2_name = tkinter.Label(self.names_frame, text=str(self.match.player2), font=("Calibri", 18, "bold"))
        self.names_frame.pack_propagate(False)

        self.names_frame.grid(row=1, columnspan=3)
        self.p1_name.pack(side=tkinter.LEFT, padx=15, anchor="nw")
        self.p2_name.pack(side=tkinter.RIGHT, padx=15, anchor="ne")

        # create the ability description canvas with 2 Text items, a name and a description
        self.desc_canvas = tkinter.Canvas(self.root, width=258, height=187, background='#cccccc')
        self.desc_canvas.grid(column=1, row=0)
        self.ability_name = self.desc_canvas.create_text(7, 7, text="", width=243, anchor="nw",
                                                         font=("Calibri", 15, "bold"))
        self.ability_desc = self.desc_canvas.create_text(7, 30, text="", width=243, anchor='nw',
                                                         font=("Calibri", 13, "normal"))

        self.manage_ability_buttons()

        # an area between the 2 health bars that shows after every turn the health gained/lost
        self.hp_change_canvas = tkinter.Canvas(self.root, width=258, height=60, background='#cccccc')
        self.hp_change_canvas.grid(column=1, row=2)
        self.p1_hp_change_text = self.hp_change_canvas.create_text(18, 30, text="", width=243, anchor="w",
                                                                   font=("Calibri", 18, "normal"), fill="red")
        self.p2_hp_change_text = self.hp_change_canvas.create_text(243, 30, text="", width=243, anchor='e',
                                                                   font=("Calibri", 18, "normal"), fill="green")

        # a frame that contains the buffs of player 1, underneath the hp bar
        self.p1_buff_frame = tkinter.Frame(self.root, background='#cccccc', width=450, height=52)
        self.p1_buff_frame.grid(row=3, column=0)
        self.p1_buff_frame.pack_propagate(False)
        self.p1_buff_labels = []

        # a frame that contains the buffs of player 2, underneath the hp bar
        self.p2_buff_frame = tkinter.Frame(self.root, background='#cccccc', width=450, height=52)
        self.p2_buff_frame.grid(row=3, column=2)
        self.p2_buff_frame.pack_propagate(False)
        self.p2_buff_labels = []

        # a frame that contains the debuffs of player 1, underneath the buffs frame
        self.p1_debuff_frame = tkinter.Frame(self.root, background='#cccccc', width=450, height=52)
        self.p1_debuff_frame.grid(row=4, column=0)
        self.p1_debuff_frame.pack_propagate(False)
        self.p1_debuff_labels = []

        # a frame that contains the debuffs of player 2, underneath the buffs frame
        self.p2_debuff_frame = tkinter.Frame(self.root, background='#cccccc', width=450, height=52)
        self.p2_debuff_frame.grid(row=4, column=2)
        self.p2_debuff_frame.pack_propagate(False)
        self.p2_debuff_labels = []

        self.history = tkinter.Frame(self.root, width=450, height=97, background='#cccccc')
        self.history.grid(row=5, columnspan=3, padx=22, pady=22, ipady=22)

        self.history_scrollbar = tkinter.Scrollbar(self.history, orient="vertical")
        self.history_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.history_text = tkinter.Canvas(self.history, width=375, height=97, background='#cccccc')
        self.history_text.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.history_text.config(yscrollcommand=self.history_scrollbar.set)
        self.history_scrollbar.config(command=self.history_text.yview)
        self.history_text.config(scrollregion=self.history_text.bbox("all"))

        self.count = 15

        self.back_button = tkinter.Button(self.root, text="Back", font=("Calibri", 15, "normal"),
                                          command=lambda: self.controller.show_frame("StartPage"))
        self.back_button.grid(row=6, column=0)

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

    def update_player1_hp(self, current_hp, current_shield, message=""):
        x0, y0, x1, y1 = self.p1_hp_canvas.coords(self.p1_green_bar)
        x1 -= 450 * min(1,
                        ((current_hp - self.match.player1.stats['current_hp']) / self.match.player1.stats['max_hp']))
        self.p1_hp_canvas.coords(self.p1_green_bar, x0, y0, x1, y1)
        hp_difference = current_hp - self.match.player1.stats['current_hp']
        shield_difference = current_shield - self.match.player1.stats['shield']
        if hp_difference > 0:
            to_print = "-" + str(hp_difference)
            color = "red"
        elif hp_difference == 0:
            print(str(shield_difference))
            to_print = str(abs(hp_difference))
            if shield_difference == 0:
                color = "gray"
            elif shield_difference > 0:
                to_print = "-" + str(shield_difference)
                color = "#26bfed"
            else:
                to_print = "+" + str(abs(shield_difference))
                color = "#26bfed"
        else:
            to_print = "+" + str(abs(hp_difference))
            color = "green"
        to_print += " " + message
        if hp_difference != 0 or shield_difference != 0 or message:
            self.hp_change_canvas.itemconfigure(self.p1_hp_change_text, text=to_print, fill=color)
        return x1

    '''
        set the size of the shield bar on the hp bar for player 1
    '''

    def update_player1_shield(self, hp_x1):
        sx0, sy0, sx1, sy1 = self.p1_hp_canvas.coords(self.p1_cyan_bar)
        shield_length = \
            450 * (self.match.player1.stats['shield'] / self.match.player1.stats['max_hp'])
        sx0 = min(hp_x1, 450 - shield_length)
        sx1 = min(sx0 + shield_length, 450)
        self.p1_hp_canvas.coords(self.p1_cyan_bar, sx0, sy0, sx1, sy1)

    '''
        called after every turn, changes the green hp bar and value in the hp change canvas for player 2
    '''

    def update_player2_hp(self, current_hp, current_shield, message=""):
        x0, y0, x1, y1 = self.p2_hp_canvas.coords(self.p2_green_bar)
        x0 += 450 * min(1,
                        ((current_hp - self.match.player2.stats['current_hp']) / self.match.player2.stats['max_hp']))
        self.p2_hp_canvas.coords(self.p2_green_bar, x0, y0, x1, y1)
        hp_difference = current_hp - self.match.player2.stats['current_hp']
        shield_difference = current_shield - self.match.player2.stats['shield']
        if hp_difference > 0:
            to_print = "-" + str(hp_difference)
            color = "red"
        elif hp_difference == 0:
            to_print = str(abs(hp_difference))
            if shield_difference == 0:
                color = "gray"
            elif shield_difference > 0:
                to_print = "-" + str(shield_difference)
                color = "#26bfed"
            else:
                to_print = "+" + str(abs(shield_difference))
                color = "#26bfed"
        else:
            to_print = "+" + str(abs(hp_difference))
            color = "green"
        to_print = message + " " + to_print
        if hp_difference != 0 or shield_difference != 0 or message:
            self.hp_change_canvas.itemconfigure(self.p2_hp_change_text, text=to_print, fill=color)
        return x0

    '''
        set the size of the shield bar on the hp bar for player 2
    '''

    def update_player2_shield(self, hp_x0):
        sx0, sy0, sx1, sy1 = self.p2_hp_canvas.coords(self.p2_cyan_bar)
        shield_length = \
            450 * (self.match.player2.stats['shield'] / self.match.player2.stats['max_hp'])
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
            tkinter.Label(frame, image=self.img, compound=tkinter.CENTER, background='black', width=37,
                          height=37) for _ in range(len(effects))]
        i = 0
        for label in buff_labels:
            CreateToolTip(label, str(effects[i]))
            label.pack(side=side, padx=7, pady=7, anchor=tkinter.N)
            label.configure(text=str(effects[i].duration), foreground="white")
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

    def add_to_history(self, slot):
        to_show = "-  " + self.match.turn[self.match.tp].name + " has used "
        ability_to_show = self.match.turn[self.match.tp].abilities[slot].name
        self.history_text.create_text(15, self.count, text=to_show + ability_to_show, anchor=tkinter.NW,
                                      font=("Calibri", 15, "normal"))
        self.count += 30
        self.history_text.config(scrollregion=self.history_text.bbox("all"))
        self.history_text.yview_moveto(1)

    def update_hp_shields(self, message, p1_current_hp, p2_current_hp, p1_current_shield, p2_current_shield):
        if self.match.tp:
            if not message:
                m1 = ""
                m2 = ""
            else:
                split_message1 = message[0]
                split_message2 = message[1] if len(message) == 2 else ["", ""]
                m1 = split_message1[1] if split_message1[0] == "+" else ""
                m1 = split_message2[1] if split_message2[0] == "+" else m1
                m2 = split_message1[1] if split_message1[0] == "-" else ""
                m2 = split_message2[1] if split_message2[0] == "-" else m2
            x1 = self.update_player1_hp(p1_current_hp, p1_current_shield, m1)
            self.update_player1_shield(x1)
            x0 = self.update_player2_hp(p2_current_hp, p2_current_shield, m2)
            self.update_player2_shield(x0)
        else:
            if not message:
                m1 = ""
                m2 = ""
            else:
                split_message1 = message[0]
                split_message2 = message[1] if len(message) == 2 else ["", ""]
                m1 = split_message1[1] if split_message1[0] == "+" else ""
                m1 = split_message2[1] if split_message2[0] == "+" else m1
                m2 = split_message1[1] if split_message1[0] == "-" else ""
                m2 = split_message2[1] if split_message2[0] == "-" else m2
            x1 = self.update_player1_hp(p1_current_hp, p1_current_shield, m2)
            self.update_player1_shield(x1)
            x0 = self.update_player2_hp(p2_current_hp, p2_current_shield, m1)
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

    '''
        a turn/round of the game
    '''

    def step(self, slot):
        if self.match.game_over():
            self.game_over()
            return

        p1_current_hp = self.match.player1.stats['current_hp']
        p2_current_hp = self.match.player2.stats['current_hp']
        p1_current_shield = self.match.player1.stats['shield']
        p2_current_shield = self.match.player2.stats['shield']

        self.add_to_history(slot)
        self.empty_hp_change_canvas()

        message = self.match.play_round_manual(slot)

        self.manage_ability_buttons()

        self.update_hp_shields(message, p1_current_hp, p2_current_hp, p1_current_shield, p2_current_shield)

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

        if self.match.game_over():
            self.game_over()
            return

    def game_over(self):
        tkinter.messagebox.showinfo("Game over!", "Game over!")
        gear = copy.deepcopy(random.choice(gear_presets))
        self.controller.p1.add_to_inventory(gear)
        self.controller.show_frame("StartPage")


if __name__ == '__main__':
    sample = random.sample(list(player_presets.keys()), 2)
    p1 = player_presets[sample[0]]
    p2 = player_presets[sample[1]]
    ui = MatchPage(None, None, p1, p2)
