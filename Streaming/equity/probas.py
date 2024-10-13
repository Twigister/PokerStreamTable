from holdem_calc import calculate
from equity.preflop import preflop_eq

def get_eq(cards, board):
    if len(board) == 0:
        return preflop_eq(cards)
    else:
        simu = 15000
    res = calculate(board, True, simu, None, cards, False) # Board, Exact search, Number of monte carlo, file, hands, Verbose

    p1_eq = 0.5 * res[0] + res[1]
    p2_eq = 1 - p1_eq

    return [p1_eq, p2_eq]
