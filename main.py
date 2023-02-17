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
            '4r1k1/pN3p2/2p2r1p/3n2pq/1P1Rp1bP/P3P1P1/3QPPB1/R5K1 b - - 0 26',
            '1r2k2r/ppp1qppp/2pbbn2/N3p1B1/4P3/3P1N2/PPP2PPP/R2Q1RK1 b k - 9 10',
            '1r2k2r/ppp1q3/2pbbp2/N3B1pp/4P3/3Q1N2/PPP2PPP/R4RK1 b k - 0 16',
            '5rk1/1p6/p3b2q/3N4/4Q3/1P6/P5P1/4R1K1 b - - 2 45',
            'rnbqkb1r/ppp2ppp/4pn2/8/2pPP3/2N2N2/PP3PPP/R1BQKB1R b KQkq - 0 5',
            '1rbq1rk1/p1p1bppp/1n2p3/n3P3/2pP4/P1N1BN2/1PQ1BPPP/R4RK1 b - - 2 13',
            'q4rk1/p1p2ppp/4p1n1/3bP1N1/3PN2P/b7/2QR1PP1/4R1K1 b - - 0 24',
            'r1bqkbnr/pp3ppp/2Npp3/8/4PB2/8/PPP2PPP/RN1QKB1R b KQkq - 0 6',
            '2n4r/p2k1pbp/2p1b1p1/4p1B1/4P3/N7/PP2BPPP/3R2K1 b - - 4 18',
            'rnbqkb1r/ppp2ppp/4pn2/8/Q1p5/5NP1/PP1PPPBP/RNB1K2R b KQkq - 1 5',
            '5rk1/5ppp/1p2pn2/p3N3/P3PP2/2R5/1Pb2P1P/3R1BK1 b - - 0 27'
        ]

        proposed_moves = list()

        for position in tested_positions:
            parser = BoardParser()
            parser.set_position_from_fen(position)
            selected_move = parser.get_engine_move()
            proposed_move = parser.proposed_move

            proposed_moves.append(proposed_move)

        for move in proposed_moves:
            print(move)