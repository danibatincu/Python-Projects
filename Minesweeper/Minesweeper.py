import random
from Tile import Tile


class Minesweeper:
    def __init__(self, rows, columns, bombs):
        self.__rows = rows
        self.__columns = columns
        self.__bombs = bombs
        self.__board = [[Tile(r, c) for c in range(self.__columns)] for r in range(self.__rows)]
        self.set_bombs()
        self.set_tile_contents()
        self.__game_over = False

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def board(self):
        return self.__board

    def game_over(self):
        return self.__game_over

    def set_tile_contents(self):
        for r in range(self.__rows):
            for c in range(self.__columns):
                if not self.__board[r][c].has_bomb() and self.bombs_around(r, c) != 0:
                    self.__board[r][c].set_content(str(self.bombs_around(r, c)))

    def set_bombs(self):
        bombs = self.__bombs
        while bombs > 0:
            row = random.randrange(self.__rows)
            col = random.randrange(self.__columns)
            while self.__board[row][col].has_bomb():
                row = random.randrange(self.__rows)
                col = random.randrange(self.__columns)
            self.__board[row][col].set_bomb()
            bombs -= 1

    def bombs_around(self, row, col):
        start_row = max(0, row - 1)
        end_row = min(self.__rows - 1, row + 1)
        start_col = max(0, col - 1)
        end_col = min(self.__columns - 1, col + 1)
        bombs = 0
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                if self.__board[r][c].has_bomb():
                    bombs += 1
        return bombs

    def press(self, row, col):
        if row >= self.__rows or col >= self.__columns:
            print("Invalid coordinates")
            return
        if self.__board[row][col].is_pressed():
            print("Tile is pressed. Try another one.")
            return
        self.__board[row][col].press()
        if self.__board[row][col].has_bomb():
            print("You hit a bomb! Game over!")
            self.__game_over = True
            return
        bombs_around = self.bombs_around(row, col)
        if bombs_around > 0:
            return
        self.press_rec(row, col)

    def press_rec(self, row, col):
        if self.bombs_around(row, col) > 0:
            return
        start_row = max(0, row - 1)
        end_row = min(self.__rows - 1, row + 1)
        start_col = max(0, col - 1)
        end_col = min(self.__columns - 1, col + 1)
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                if not self.__board[r][c].has_bomb() and not self.__board[r][c].is_pressed():
                    self.press(r, c)

    def check_for_completion(self):
        unpressed = 0
        for r in range(self.__rows):
            for c in range(self.__columns):
                if not self.__board[r][c].is_pressed():
                    unpressed += 1
                    if unpressed > self.__bombs:
                        return False
        return True

    def print(self):
        for r in range(self.__rows):
            tpr = ""
            for c in range(self.__columns):
                tpr += str(self.__board[r][c]) + " "
            print(tpr)


