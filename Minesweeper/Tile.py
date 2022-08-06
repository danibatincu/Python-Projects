class Tile:
    def __init__(self, row, column):
        self.__row = row
        self.__column = column
        self.__has_bomb = False
        self.__pressed = False
        self.__content = " "
        self.__marked = False

    @property
    def marked(self):
        return self.__marked

    def change_mark(self):
        self.__marked = not self.__marked

    @property
    def content(self):
        return self.__content

    def is_pressed(self):
        return self.__pressed

    def press(self):
        self.__pressed = True

    def has_bomb(self):
        return self.__has_bomb

    def set_bomb(self):
        self.__has_bomb = True

    def set_content(self, content):
        self.__content = content

    def __str__(self):
        if not self.__pressed:
            return "o"
        if self.__has_bomb:
            return "x"
        return self.__content
