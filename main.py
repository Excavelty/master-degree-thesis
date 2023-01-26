from ConvEngine import ConvEngine
from BoardParser import BoardParser

if __name__ == '__main__':
    forced_beginnings = ['a2a4', 'b2b4', 'c2c4', 'd2d4', 'e2e4', 'f2f4', 'g2g4', 'h2h4',
                         'b1c3', 'g1f3']

            
    for beginning in forced_beginnings:
        parser = BoardParser()

        game_active = True

        iter = 1

        while(game_active):
            if iter == 1:
                next_white_move = beginning
            else:
                next_white_move = parser.get_stockfish_move()# input("Next move for white:\n") 
            
            parser.update_move(next_white_move)

            if parser.is_end_of_game():
                break

            # next_black_move = parser.get_stockfish_move()
            next_black_move = parser.get_engine_move()
            parser.update_move(next_black_move)

            if parser.is_end_of_game():
                break

            iter += 1

        with open(f'results{beginning}.txt', 'w') as file:
            file.write(f'legal_moves={parser.legal_moves}, illegal_moves={parser.illegal_moves}\n')
            file.write(str(parser.game_history) + '\n')
            file.write(str(parser.evals) + '\n')

            # game_active = False