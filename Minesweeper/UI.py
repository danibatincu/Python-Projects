import tkinter
import tkinter.font as font
import tkinter.messagebox as messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from Minesweeper import Minesweeper


class UI:
    def __init__(self):
        self.__root = tkinter.Tk()
        self.__frm = ttk.Frame(self.__root, padding=20)
        self.__frm.grid()
        self.__menu = tkinter.Menu(self.__root)
        self.__root.config(menu=self.__menu)
        self.__menu.add_command(label="New game", command=self.new_game)

        self.__pixel = tkinter.PhotoImage(width=1, height=1)

        self.__buttons = []

        self.__flag_image = self.open_image("./luffy.png")
        self.__bomb_image = self.open_image("./bomb.png")

        self.__game = Minesweeper(15, 15, 15)

        self.__color_dict = {' ': "white", '1': "blue", '2': "green", '3': "red",
                             '4': "#6b0ea8", '5': "#7b490b", '6': "cyan", '7': "black", '8': "#878787"}

        self.create_board()

        self.__root.mainloop()

    def new_game(self):
        self.__game = Minesweeper(15, 15, 15)
        self.create_board()

    @staticmethod
    def open_image(path):
        image = Image.open(path)
        image = image.resize((25, 25))
        return ImageTk.PhotoImage(image)

    def create_board(self):
        self.__buttons = []
        for row in range(self.__game.rows):
            button_rows = []
            for col in range(self.__game.columns):
                button = tkinter.Button(self.__frm, image=self.__pixel, compound="center", bg="#b4ac96")
                # button.config(command=lambda x=row, y=col: [game.press(x, y), update()])
                button.config(height=25, width=25)
                button.grid(column=col, row=row)
                button.bind('<Button-1>', lambda event, x=row, y=col: [self.__game.press(x, y), self.update()])
                button.bind('<Button-3>', lambda event, x=row, y=col: self.mark_for_bomb(x, y))
                button_rows.append(button)
            self.__buttons.append(button_rows)

    def mark_for_bomb(self, r, c):
        if self.__game.board[r][c].marked:
            self.__buttons[r][c].config(image=self.__pixel)
        else:
            self.__buttons[r][c].config(image=self.__flag_image)
        self.__game.board[r][c].change_mark()

    def update(self):
        for r in range(self.__game.rows):
            for c in range(self.__game.columns):
                if self.__game.board[r][c].is_pressed():
                    self.button_to_label(r, c)
        if self.__game.game_over():
            self.press_all_buttons()
            messagebox.showwarning("Game over!", "You clicked on a bomb! Game over!")
            self.__root.destroy()
            return
        if self.__game.check_for_completion():
            messagebox.showinfo("You won!", "Congratulations! You won!")
            self.__root.destroy()

    def button_to_label(self, r, c):
        fnt = font.Font(family='Helvetica', size=20, weight='bold')
        label = tkinter.Label(self.__frm, image=self.__pixel, height=25, width=25, bg="#eeeee4",
                              fg=self.__color_dict[self.__game.board[r][c].content],
                              text=self.__game.board[r][c].content, font=fnt, compound="center",
                              borderwidth=0.2,
                              relief="solid")
        label.grid(column=c, row=r)
        if self.__game.board[r][c].has_bomb():
            label.config(image=self.__bomb_image)

    def press_all_buttons(self):
        for r in range(self.__game.rows):
            for c in range(self.__game.columns):
                if not self.__game.board[r][c].is_pressed():
                    self.button_to_label(r, c)

