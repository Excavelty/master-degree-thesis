import numpy as np
import chess
from ConvEngine import ConvEngine
from stockfish import Stockfish
from BoardUtility import BoardUtility

class BoardParser:
    def __init__(self):
        self.board_utility = BoardUtility()
        self.board = chess.Board()
        self.board_size = 8
        self.move_counter = 1
        self.engine = ConvEngine()
        self.engine.load_models_from_files('./ready_models/board_model.h5', './ready_models/piece_model.h5')
        self.stockfish = Stockfish(path="../stockfish/stockfish-windows-2022-x86-64-avx2.exe")
        self.legal_moves = 0
        self.illegal_moves = 0
        self.game_history = list()
        self.evals = list()

    def update_move(self, san: str) -> None:
        self.board.push_san(san)
        self.move_counter += 1

        print(self.stockfish.get_evaluation())
        self.print_board()

    def get_engine_move(self) -> str:
        piece_and_square = self.engine.predict_next_move(self.get_position_as_fen())
        # find where piece is now
        piece_possible_positions = self.find_piece_type_positions(piece_and_square['piece'])
        
        # print(self.board.legal_moves)

        print(f'{self.legal_moves} vs {self.illegal_moves}')

        for piece_possible_position in piece_possible_positions:
        # concat starting and ending position to form san
            san_move = piece_possible_position + piece_and_square['square']

            print(san_move)

            if piece_possible_position != piece_and_square['square'] and chess.Move.from_uci(san_move) in self.board.legal_moves:
                self.legal_moves += 1
                self.game_history.append(1)

                self.stockfish.set_fen_position(self.get_position_as_fen())
                eval_dict = self.stockfish.get_evaluation()
                if eval_dict['type'] == 'cp':
                    self.evals.append(eval_dict['value'])
                else:
                    self.evals.append(10000)

                return san_move

        # here return stockfish substitution move
        print('No legal moves generated, Stockfish will play substitution')

        self.illegal_moves += 1

        self.stockfish.set_fen_position(self.get_position_as_fen())
        best_move_by_stockfish = self.stockfish.get_best_move()

        self.game_history.append(2)

        eval_dict = self.stockfish.get_evaluation()
        if eval_dict['type'] == 'cp':
            self.evals.append(eval_dict['value'])
        else:
            print(eval_dict)
            self.evals.append(10000)

        return best_move_by_stockfish

    def get_stockfish_move(self) -> str:
        self.stockfish.set_fen_position(self.get_position_as_fen())
        best_move_by_stockfish = self.stockfish.get_best_move()

        self.game_history.append(0)                
        eval_dict = self.stockfish.get_evaluation()
        if eval_dict['type'] == 'cp':
            self.evals.append(eval_dict['value'])
        else:
            self.evals.append(10000)

        return best_move_by_stockfish

    def find_piece_type_positions(self, piece: str) -> str:
        board_ascii = str(self.board).strip().replace(" ", "").split("\n")

        print(board_ascii)

        positions = []

        for row in range(self.board_size):
            for col in range(self.board_size):
                if board_ascii[row][col] == piece:
                    position = self.board_utility.row_and_col_to_pos(row, col)
                    positions.append(position)        

        return positions

    def print_board(self) -> None:
        print(self.board)
        print('\n')

    def set_position_from_fen(self, fen: str) -> None:
        self.board = chess.Board(fen)

    def get_position_as_fen(self) -> str:
        return self.board.fen()

    def is_end_of_game(self) -> bool:
        return self.board.is_checkmate()