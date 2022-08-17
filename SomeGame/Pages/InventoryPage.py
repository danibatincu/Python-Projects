import tkinter.ttk

from PIL import ImageTk, Image
from PIL.Image import LANCZOS

from utils import *


class InventoryPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller

        print(self.controller.p1.inventory)
        print(self.controller.p1.gear)

        label = tkinter.ttk.Label(self, text="Inventory", font=("Calibri", 48, "bold"))
        label.place(relx=0.22, rely=0.10, anchor=tkinter.CENTER)

        inventory_frame = tkinter.Frame(self, width=490, height=185, background="#cccccc")
        inventory_frame.place(relx=0.655, rely=0.49, anchor=tkinter.CENTER)
        inventory_frame.lift()

        str_label = tkinter.Label(self, text="Strength", font=("Calibri", 20, "bold"))
        str_label.place(relx=0.45, rely=0.07, anchor=tkinter.W)

        self.str_val_label = tkinter.Label(self, text=str(self.controller.p1.stats["strength"]),
                                           font=("Calibri", 20, "bold"))
        self.str_val_label.place(relx=0.6, rely=0.07, anchor=tkinter.W)

        int_label = tkinter.Label(self, text="Intellect", font=("Calibri", 20, "bold"))
        int_label.place(relx=0.45, rely=0.13, anchor=tkinter.W)

        self.int_val_label = tkinter.Label(self, text=str(self.controller.p1.stats["intellect"]),
                                           font=("Calibri", 20, "bold"))
        self.int_val_label.place(relx=0.6, rely=0.13, anchor=tkinter.W)

        vit_label = tkinter.Label(self, text="Vitality", font=("Calibri", 20, "bold"))
        vit_label.place(relx=0.45, rely=0.19, anchor=tkinter.W)

        self.vit_val_label = tkinter.Label(self, text=str(self.controller.p1.stats["vitality"]),
                                           font=("Calibri", 20, "bold"))
        self.vit_val_label.place(relx=0.6, rely=0.19, anchor=tkinter.W)

        crit_label = tkinter.Label(self, text="Crit. chance", font=("Calibri", 20, "bold"))
        crit_label.place(relx=0.45, rely=0.25, anchor=tkinter.W)

        self.crit_val_label = tkinter.Label(self, text=str(self.controller.p1.stats["crit_chance"]) + "%",
                                            font=("Calibri", 20, "bold"))
        self.crit_val_label.place(relx=0.6, rely=0.25, anchor=tkinter.W)

        phys_def_label = tkinter.Label(self, text="Physical defence", font=("Calibri", 20, "bold"))
        phys_def_label.place(relx=0.7, rely=0.07, anchor=tkinter.W)

        self.phys_def_val_label = tkinter.Label(self, text=str(self.controller.p1.stats["physical_def"]) + "%",
                                                font=("Calibri", 20, "bold"))
        self.phys_def_val_label.place(relx=0.9, rely=0.07, anchor=tkinter.W)

        mag_def_label = tkinter.Label(self, text="Magical defence", font=("Calibri", 20, "bold"))
        mag_def_label.place(relx=0.7, rely=0.13, anchor=tkinter.W)

        self.mag_def_val_label = tkinter.Label(self, text=str(self.controller.p1.stats["magical_def"]) + "%",
                                               font=("Calibri", 20, "bold"))
        self.mag_def_val_label.place(relx=0.9, rely=0.13, anchor=tkinter.W)

        avoid_label = tkinter.Label(self, text="Avoidance", font=("Calibri", 20, "bold"))
        avoid_label.place(relx=0.7, rely=0.19, anchor=tkinter.W)

        self.avoid_val_label = tkinter.Label(self, text=str(self.controller.p1.stats["avoidance"]) + "%",
                                             font=("Calibri", 20, "bold"))
        self.avoid_val_label.place(relx=0.9, rely=0.19, anchor=tkinter.W)

        crit_resist_label = tkinter.Label(self, text="Crit. resistance", font=("Calibri", 20, "bold"))
        crit_resist_label.place(relx=0.7, rely=0.25, anchor=tkinter.W)

        self.crit_resist_val_label = tkinter.Label(self, text=str(self.controller.p1.stats["crit_resist"]) + "%",
                                                   font=("Calibri", 20, "bold"))
        self.crit_resist_val_label.place(relx=0.9, rely=0.25, anchor=tkinter.W)

        button = tkinter.Button(self, text="Back", font=("Calibri", 20, "bold"), width=25,
                                command=lambda: self.controller.show_frame("StartPage"))
        button.place(relx=0.22, rely=0.85, anchor=tkinter.CENTER)

        self.inventory_labels = []

        for i in range(3):
            for j in range(8):
                inv_slot = \
                    InventorySlotFrame(self, width=50, height=50, background="#aaaaaa", inv_row=i, inv_col=j)
                inv_slot.place(x=576 + 60 * j, y=258 + 60 * i, anchor=tkinter.CENTER)
                if self.controller.p1.inventory[i][j]:
                    image = Image.open(self.controller.p1.inventory[i][j].image)
                    image = image.resize((50, 50), LANCZOS)
                    item_image = ImageTk.PhotoImage(image)
                    self.inventory_labels.append(item_image)
                    item = \
                        InventoryItemLabel(self, self.controller, width=50, height=50,
                                           image=item_image, inv_row=i, inv_col=j,
                                           slot=self.controller.p1.inventory[i][j].slot, equipped=False)
                    CreateToolTip(item, str(self.controller.p1.inventory[i][j]))
                    item.place(x=576 + 60 * j, y=258 + 60 * i, anchor=tkinter.CENTER)

        head_slot = GearSlotFrame(self, width=50, height=50, background="#aaaaaa", slot="head")
        shoulders_slot = GearSlotFrame(self, width=50, height=50, background="#aaaaaa", slot="shoulders")
        chest_slot = GearSlotFrame(self, width=50, height=50, background="#aaaaaa", slot="chest")
        hands_slot = GearSlotFrame(self, width=50, height=50, background="#aaaaaa", slot="hands")
        legs_slot = GearSlotFrame(self, width=50, height=50, background="#aaaaaa", slot="legs")
        feet_slot = GearSlotFrame(self, width=50, height=50, background="#aaaaaa", slot="feet")
        main_hand_slot = GearSlotFrame(self, width=50, height=50, background="#aaaaaa", slot="main_hand")
        off_hand_slot = GearSlotFrame(self, width=50, height=50, background="#aaaaaa", slot="off_hand")

        head_slot.place(x=140, y=225, anchor="center")
        shoulders_slot.place(x=140, y=285, anchor="center")
        chest_slot.place(x=140, y=345, anchor="center")
        hands_slot.place(x=360, y=225, anchor="center")
        legs_slot.place(x=360, y=285, anchor="center")
        feet_slot.place(x=360, y=345, anchor="center")
        main_hand_slot.place(x=220, y=405, anchor="center")
        off_hand_slot.place(x=280, y=405, anchor="center")

        gear_positions = {"head": (140, 225), "shoulders": (140, 285), "chest": (140, 345),
                          "hands": (360, 225), "legs": (360, 285), "feet": (360, 345),
                          "main_hand": (220, 405), "off_hand": (280, 405)}

        for slot in self.controller.p1.gear.keys():
            if self.controller.p1.gear[slot]:
                image = Image.open(self.controller.p1.gear[slot].image)
                image = image.resize((50, 50), LANCZOS)
                item_image = ImageTk.PhotoImage(image)
                self.inventory_labels.append(item_image)
                item = \
                    InventoryItemLabel(self, self.controller, width=50, height=50,
                                       image=item_image, inv_row=-1, inv_col=-1,
                                       slot=slot, equipped=True)
                CreateToolTip(item, str(self.controller.p1.gear[slot]))
                item.place(x=gear_positions[slot][0], y=gear_positions[slot][1], anchor="center")

    def update_stats(self):
        self.str_val_label['text'] = str(self.controller.p1.stats["strength"])
        self.int_val_label['text'] = str(self.controller.p1.stats["intellect"])
        self.vit_val_label['text'] = str(self.controller.p1.stats["vitality"])
        self.crit_val_label['text'] = str(self.controller.p1.stats["crit_chance"]) + "%"
        self.phys_def_val_label['text'] = str(self.controller.p1.stats["physical_def"]) + "%"
        self.mag_def_val_label['text'] = str(self.controller.p1.stats["magical_def"]) + "%"
        self.avoid_val_label['text'] = str(self.controller.p1.stats["avoidance"]) + "%"
        self.crit_resist_val_label['text'] = str(self.controller.p1.stats["crit_resist"]) + "%"


class InventorySlotFrame(tkinter.Frame):
    def __init__(self, parent, width, height, background, inv_row, inv_col):
        super().__init__(parent, background=background, height=height, width=width)
        self.inv_row = inv_row
        self.inv_col = inv_col


class GearSlotFrame(tkinter.Frame):
    def __init__(self, parent, width, height, background, slot):
        super().__init__(parent, background=background, height=height, width=width)
        self.slot = slot


class InventoryItemLabel(tkinter.Label):
    def __init__(self, parent, controller, width, height, image, inv_row, inv_col, slot, equipped):
        super().__init__(parent, image=image, height=height, width=width)
        self.parent = parent
        self.controller = controller
        self.inv_row = inv_row
        self.inv_col = inv_col
        self.equipped = equipped
        self.slot = slot

        self.bind("<Button-1>", self.clicked_for_drag)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<ButtonRelease-1>", self.drop)

        self.current_old_x = 0
        self.current_old_y = 0

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
        if isinstance(target, InventorySlotFrame):
            new_x = target.winfo_x() + target.winfo_reqwidth() // 2
            new_y = target.winfo_y() + target.winfo_reqheight() // 2
            self.current_old_x = new_x
            self.current_old_y = new_y
            event.widget.place(x=new_x, y=new_y, anchor="center")
            event.widget.lift()
            target_row = target.inv_row
            target_col = target.inv_col
            if self.equipped:
                self.controller.p1.inventory[target_row][target_col] = self.controller.p1.gear[self.slot]
                self.controller.p1.add_gear(self.slot, None)
                self.inv_row = target_row
                self.inv_col = target_col
                self.equipped = False
                self.parent.update_stats()
                return
            if target_col != self.inv_col or target_row != self.inv_row:
                self.controller.p1.inventory[target_row][target_col] = \
                    self.controller.p1.inventory[self.inv_row][self.inv_col]
                self.controller.p1.inventory[self.inv_row][self.inv_col] = None
                self.inv_row = target_row
                self.inv_col = target_col
            return
        if isinstance(target, GearSlotFrame):
            target_slot = target.slot
            if self.slot == target_slot:
                new_x = target.winfo_x() + target.winfo_reqwidth() // 2
                new_y = target.winfo_y() + target.winfo_reqheight() // 2
                self.current_old_x = new_x
                self.current_old_y = new_y
                event.widget.place(x=new_x, y=new_y, anchor="center")
                event.widget.lift()
                if not self.equipped:
                    old_gear = \
                        self.controller.p1.add_gear(target_slot,
                                                    self.controller.p1.inventory[self.inv_row][self.inv_col])
                    self.controller.p1.inventory[self.inv_row][self.inv_col] = old_gear
                    self.controller.p1.inventory[self.inv_row][self.inv_col] = None
                    self.equipped = True
                    self.parent.update_stats()
                    return
            return
        event.widget.place(x=self.current_old_x, y=self.current_old_y, anchor="nw")
        event.widget.lift()
