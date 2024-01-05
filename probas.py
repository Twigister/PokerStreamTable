from holdem_calc import calculate

def get_eq(cards, board):
    print(board)
    if len(board) == 0:
            simu = 1500
    else:
        simu = 15000
    res = calculate(board, False, simu, None, cards, False) # Board, Exact search, Number of monte carlo, file, hands, Verbose

    p1_eq = 0.5 * res[0] + res[1]
    p2_eq = 1 - p1_eq

    return [p1_eq, p2_eq]
