import chess

class BoardUtility:
    def __init__(self):
        self.board_size = 8

    def square_index_to_pos(self, index):
        line = chr(ord('a') + index % self.board_size)
        rank = self.board_size - int(index / self.board_size)

        return str(line) + str(rank)

    def row_and_col_to_pos(self, row, col):
        line = chr(ord('a') + col)
        rank = self.board_size - row

        return str(line) + str(rank)