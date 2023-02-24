from ConvEngine import ConvEngine
from BoardParser import BoardParser

if __name__ == '__main__':
    option = int(input('Prosze wybrac opcje: 1. Kompletne partie, 2. Odpowiedzi na wybrane pozycje:\n'))

    if option == 1:
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
                file.write(str(parser.evals) + '\n')

            with open(f'illegal_choices.txt', 'a') as file:
                illegal_choices = parser.illegal_choices
                for choice in illegal_choices:
                    file.write(choice['position'] + '\n')
                    file.write(choice['move'] + '\n')
                # game_active = False
    elif option == 2:
        tested_positions=[
            'r1b1r1k1/pp3ppp/n1p2b2/7q/1P2p2P/P1N1P1P1/1BQ1PPB1/R4RK1 b - - 0 16',
            '1r2k2r/ppp1q3/2pbbp2/N3B1pp/4P3/3Q1N2/PPP2PPP/R4RK1 b k - 0 16',
            '5rk1/1p6/p3b2q/3N4/4Q3/1P6/P5P1/4R1K1 b - - 2 45',
            'q4rk1/p1p2ppp/4p1n1/3bP1N1/3PN2P/b7/2QR1PP1/4R1K1 b - - 0 24',
            'r1bqkbnr/pp3ppp/2Npp3/8/4PB2/8/PPP2PPP/RN1QKB1R b KQkq - 0 6',
            'r1bqk2r/bpp2p2/p1np1n1p/4p1p1/PPB1P3/2PP1N2/3N1PPP/R1BQR1K1 b kq - 0 10',
            'r1b2rk1/1p3pq1/p2p3p/2P1n1p1/P2bP3/R5NP/B3RPP1/2B1Q1K1 b - - 0 21',
            'r4r2/3b1p1k/p2p1q1p/2b1nNp1/p3P3/6RP/B1R2PPK/2BQ4 b - - 5 27',
            'r2qk2r/bpp2pp1/p1npBn1p/4p3/PP2P3/2PP1N1P/3N1PP1/R1BQK2R b KQkq - 0 10',
            '4r3/2p2rpk/p1qppnnp/1P2p3/1P2P1NP/R1PPR1P1/5P1N/3Q2K1 b - - 0 32',
            'r2q1rk1/2p2ppp/p1n1b3/1pbpP3/8/2P2N2/PPBN1RPP/R1BQ2K1 b - - 0 12',
            '5rk1/1n3rpp/p2q4/1p1pp3/2p5/2Pb1N2/PP1Q1BPP/3BR1KN b - - 5 25'
        ]

        parser = BoardParser()
        proposed_moves = list()

        for position in tested_positions:
            parser.set_position_from_fen(position)
            selected_move = parser.get_engine_move()
            proposed_move = parser.proposed_move

            proposed_moves.append(proposed_move)

        for move in proposed_moves:
            print(move)