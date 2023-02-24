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
        self.stockfish_evaluating = Stockfish(path="../stockfish/stockfish-windows-2022-x86-64-avx2.exe")
        self.legal_moves = 0
        self.illegal_moves = 0
        self.last_move_type = 0
        self.proposed_move = None
        self.evals = list()
        self.illegal_choices = list()
        
        self.stockfish.set_elo_rating(600)
        self.stockfish_evaluating.set_elo_rating(2800)

    def update_move(self, san: str) -> None:
        print(f'{self.legal_moves} vs {self.illegal_moves}')
        self.board.push_san(san)
        self.move_counter += 1

        self.stockfish.set_fen_position(self.get_position_as_fen())
        self.stockfish_evaluating.set_fen_position(self.get_position_as_fen())
        evaluation = self.stockfish.get_evaluation()

        if evaluation['type'] == 'cp': 
            self.evals.append(dict(type=self.last_move_type, evaluation=evaluation['value'], notes='normal_move'))
        else:
            self.evals.append(dict(type=self.last_move_type, evaluation=1000, notes='mate'))

        print(evaluation)
        self.print_board()

    def get_engine_move(self) -> str:
        pieces_and_squares = self.engine.predict_next_move(self.get_position_as_fen())

        for piece in pieces_and_squares['pieces']:
            for square in pieces_and_squares['squares']:
                piece_and_square = dict(piece=piece, square=square)
                # find where piece is now
                piece_possible_positions = self.find_piece_type_positions(piece_and_square['piece'])
                
                local_illegal_choices = list()

                for piece_possible_position in piece_possible_positions:
                    # concat starting and ending position to form san
                    san_move = piece_possible_position + piece_and_square['square']

                    if piece_possible_position != piece_and_square['square'] and chess.Move.from_uci(san_move) in self.board.legal_moves:
                        self.legal_moves += 1
                        self.last_move_type = 1
                        self.proposed_move = san_move
                        return san_move
                    else:
                        self.proposed_move = san_move
                        local_illegal_choices.append(dict(position=self.get_position_as_fen(), move=san_move))

        # here return stockfish substitution move
        print('No legal moves generated, Stockfish will play substitution')

        self.illegal_choices += local_illegal_choices

        self.illegal_moves += 1
        self.last_move_type = 2

        self.stockfish.set_fen_position(self.get_position_as_fen())
        best_move_by_stockfish = self.stockfish.get_best_move()

        return best_move_by_stockfish

    def get_stockfish_move(self) -> str:
        self.stockfish.set_fen_position(self.get_position_as_fen())
        best_move_by_stockfish = self.stockfish.get_best_move()

        self.last_move_type=0

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
        print(self.stockfish.get_board_visual())

    def set_position_from_fen(self, fen: str) -> None:
        self.board = chess.Board(fen)

    def get_position_as_fen(self) -> str:
        return self.board.fen()

    def is_end_of_game(self) -> bool:
        return self.board.is_checkmate()