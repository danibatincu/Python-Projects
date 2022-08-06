import random

class Board:
    def __init__(self):
        self.reset()
        self.generate()

    def __init__(self,code):
        self.reset()
        self.generate_from_code(code)

    def reset(self):
        self.board = [[0 for i in range(1,10)] for j in range(1,10)]

    def generate_from_code(self,code):
        values = [char for char in code]
        for i in range(9):
            for j in range(9):
                self.board[i][j] = int(values[0])
                values = values[1:]
            

    def generate(self):
        self.generate_diagonal_squares()
        self.solve()
        self.remove_squares()

    def remove_squares(self):
        count = 51
        while count > 0:
            while True:
                i = random.randrange(9)
                j = random.randrange(9)
                while self.board[i][j] == 0:
                    i = random.randrange(9)
                    j = random.randrange(9)
                number = self.board[i][j]
                self.board[i][j] = 0
                if self.single_solution():
                    break
                self.board[i][j] = number
            count -= 1
        

    def single_solution(self):
        return self.single_solution_rec(0,0,0) == 1

    def single_solution_rec(self,row,column,count):
        if column == 9:
            row += 1
            column = 0
        if row == 9:
            return 1+count
        if self.board[row][column] != 0:
            return self.single_solution_rec(row,column+1,count)
        for number in range(1,10):
            if count > 2:
                break
            if self.valid(number,row,column):
                self.board[row][column] = number
                count = self.single_solution_rec(row,column+1,count)
        self.board[row][column] = 0
        return count

    def generate_diagonal_squares(self):
        numbers = list(range(1,10))
        random.shuffle(numbers)
        for i in range(3):
            for j in range(3):
                self.board[i][j] = numbers[0]
                numbers = numbers[1:]

        numbers = list(range(1,10))
        random.shuffle(numbers)
        for i in range(3,6):
            for j in range(3,6):
                self.board[i][j] = numbers[0]
                numbers = numbers[1:]

        numbers = list(range(1,10))
        random.shuffle(numbers)
        for i in range(6,9):
            for j in range(6,9):
                self.board[i][j] = numbers[0]
                numbers = numbers[1:]

    def valid_line(self,number,line):
        return number not in self.board[line]

    def valid_column(self,number,column):
        return number not in [self.board[i][column] for i in range(9)]

    def valid_square(self,number,row,column):
        start_row = 3*(row//3)
        start_col = 3*(column//3)
        for i in range(start_row,start_row+3):
            for j in range(start_col,start_col+3):
                if self.board[i][j] == number:
                    return False
        return True

    def valid(self,number,row,column):
        return self.valid_line(number,row) and self.valid_column(number,column) and self.valid_square(number,row,column)

    def solve(self):
        self.solve_rec(0,0)

    def solve_rec(self,row,column):
        if column == 9:
            row += 1
            column = 0
        if row == 9:
            return True
        if self.board[row][column] != 0:
            return self.solve_rec(row,column+1)
        for number in range(1,10):
            if self.valid(number,row,column):
                self.board[row][column] = number
                if self.solve_rec(row,column+1):
                    return True
                self.board[row][column] = 0
        return False 

    def print(self):
        for i in range(0,9):
            row = ""
            for j in range(0,9):
                if self.board[i][j] == 0:
                    tpr = "_"
                else:
                    tpr = str(self.board[i][j])
                row += tpr + " "
            print(row)


board = Board("906050008100000420047080061409070830080060005030000106010007080690013057072594600")
board.print()
board.solve()
print("")
board.print()
