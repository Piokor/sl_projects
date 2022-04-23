class Board:
    def __init__(self, size: tuple[int, int]):
        self.__size = size
        width, height = size
        self.__board = [[0] * width for _ in range(height)]
        self.gen = 0

    def get_size(self):
        return self.__size

    def get_board(self):
        return self.__board

    def get_field_value(self, cords: tuple[int, int]) -> int:
        x, y = cords
        return self.__board[y][x]

    def set_field_value(self, cords: tuple[int, int], value: int):
        x, y = cords
        self.__board[y][x] = value

    def swap_field(self, cords: tuple[int, int]):
        x, y = cords
        value = self.get_field_value(cords)
        self.__board[y][x] = int(not value)

    def next_gen(self):
        width, height = self.__size
        new_board = [[0] * width for _ in range(height)]

        for i in range(height):
            for j in range(width):
                new_board[i][j] = self.__next_gen_field((j, i))

        self.__board = new_board
        self.gen += 1

    def reset_board(self):
        self.__board = [[0] * self.__size[0] for _ in range(self.__size[1])]

    def __field_neighbors(self, cords: tuple[int, int]) -> int:
        x, y = cords
        result = 0
        for i in range(-1, 2):
            i_mod = (y + i) % self.__size[1]
            for j in range(-1, 2):
                j_mod = (x + j) % self.__size[0]
                result += self.get_field_value((j_mod, i_mod))

        return result - self.get_field_value((x, y))

    def __next_gen_field(self, cords: tuple[int, int]) -> int:
        neighbors = self.__field_neighbors(cords)
        if self.get_field_value(cords):
            return 1 if neighbors in (2, 3) else 0
        else:
            return 1 if neighbors == 3 else 0

    def __str__(self):
        result = ""
        for i, row in enumerate(self.__board):
            result += "".join(map(str, self.__board[i]))
            result += "\n"
        return result
