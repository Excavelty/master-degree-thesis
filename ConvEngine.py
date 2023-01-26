from Engine import Engine
from keras.models import load_model
import numpy as np
from BoardUtility import BoardUtility
import chess

class ConvEngine(Engine):
    def __init__(self):
        self.board_utility = BoardUtility()
        self.board_size = 8
        self.piece_to_channel_data_mapping = dict(p=(0, 1),
                                b=(1, 1),
                                r=(2, 1),
                                n=(3, 1),
                                q=(4, 1),
                                k=(5, 1),
                                P=(6, 1),
                                B=(7, 1),
                                R=(8, 1),
                                N=(9, 1),
                                Q=(10, 1),
                                K=(11, 1))
        self.piece_to_channel_data_mapping['.'] = (0, 0)
        self.last_layer = np.zeros((self.board_size, self.board_size))
        self.previous_first = np.zeros((self.board_size, self.board_size))
        self.previous_second = np.zeros((self.board_size, self.board_size))
        self.previous_third = np.zeros((self.board_size, self.board_size))
        
        self.index_to_piece = ['p', 'b', 'r', 'n', 'q', 'k']

    # override method
    def load_models_from_files(self, file_name: str, file_name_piece: str) -> None:
        print(f'Loading CNN model from file: {file_name}')
        self.model_board = load_model(file_name)

        print(f'Loading CNN model from file: {file_name_piece}')
        self.model_piece = load_model(file_name_piece)
  
    # override method
    def predict_next_move(self, fen: str) -> str:
        cnn_channels = self.get_cnn_channels(fen)

        result_squares_list = list(self.model_board.predict(np.array([cnn_channels]))[0])
        result_square = result_squares_list.index(max(result_squares_list))

        square = self.board_utility.square_index_to_pos(result_square)

        result_piece = list(self.model_piece(np.array([cnn_channels]))[0])
        print(max(result_piece))
        piece_index = result_piece.index(max(result_piece))
        piece = self.index_to_piece[piece_index]

        self.previous_third = self.previous_second
        self.previous_second = self.previous_first
        self.previous_first = np.zeros((self.board_size, self.board_size))# str(chess.Board(fen))

        self.last_layer = 0.25 * self.previous_third + 0.5 * self.previous_second + 1. * self.previous_first

        return dict(piece=piece, square=square)

    def from_fen_to_cnn_channels(self, fen):
        ascii_position = self.fen_to_ascii_position(fen)

        ascii_rows = ascii_position.replace(' ', '').split('\n')
        board_channels = np.zeros((8, 8, 13))
        for i in range(8):
            for j in range(8):
                channel_data = self.piece_to_channel_data_mapping[ascii_rows[i][j]]
                board_channels[i][j][channel_data[0]] = channel_data[1]
                board_channels[i][j][6] = self.last_layer[i][j]

        return board_channels

    def fen_to_ascii_position(self, fen):
        parsing_board = chess.Board(fen)

        return str(parsing_board)

    def get_cnn_channels(self, fen):
        cnn_channels = self.from_fen_to_cnn_channels(fen)

        return cnn_channels