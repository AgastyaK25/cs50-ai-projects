"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counter = 0
    o_counter = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_counter += 1
            elif cell == O:
                o_counter += 1
    if x_counter > o_counter: # If more X's on board, then is O's turn, vice versa
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set() # set for possible moves
    for i in range(3): # rows
        for j in range(3): # columns
            if board[i][j] == EMPTY: # Makes sure cell is empty
                moves.add((i, j)) # adds move to list of possible moves

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if i not in range(3) or j not in range(3):
        raise Exception("You can't move beyond the board!")
    elif board[i][j] != EMPTY:
        raise Exception("This cell is occupied!")

    board_copy = deepcopy(board) # deep copy of board
    board_copy[i][j] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        xCount = 0
        oCount = 0
        for cell in row: # checks for 3 X's or 3 O's in a row
            if cell == X:
                xCount += 1
            if cell == O:
                oCount += 1
        if xCount == 3:
            return X
        elif oCount == 3:
            return O
    # check columns
    if board[0][0] == board[1][0] == board[2][0] and board[0][0] is not EMPTY:
        return board[0][0]
    elif board[0][1] == board[1][1] == board[2][1] and board[0][1] is not EMPTY:
        return board[0][1]
    elif board[0][2] == board[1][2] == board[2][2] and board[0][2] is not EMPTY:
        return board[0][2]
    # check diagonals
    elif board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or not actions(board):
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_action(board): # helper function to find best maximizing move
        best_value = -math.inf
        best_action = None
        alpha = -math.inf
        beta = math.inf

        for action in actions(board):
            value = min_value(result(board, action), alpha, beta)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)
            if best_value >= beta:
                break # prune

        return best_action

    def min_action(board): # helper function to find best minimizing move
        best_value = math.inf
        best_action = None
        alpha = -math.inf
        beta = math.inf

        for action in actions(board):
            value = max_value(result(board, action), alpha, beta)
            if value < best_value:
                best_value = value
                best_action = action
            beta = min(beta, best_value)
            if best_value <= alpha:
                break # prune

        return best_action

    def max_value(board, alpha, beta): # helper function to find maximizing value for each possible move
        if terminal(board):
            return utility(board)

        value = -math.inf
        for action in actions(board):
            value = max(value, min_value(result(board, action), alpha, beta))
            alpha = max(alpha, value)
            if value >= beta:
                break # prune (alpha-beta pruning)

        return value

    def min_value(board, alpha, beta): # helper function to find minimizing value for each possible move
        if terminal(board):
            return utility(board)

        value = math.inf
        for action in actions(board):
            value = min(value, max_value(result(board, action), alpha, beta))
            beta = min(beta, value)
            if value <= alpha:
                break # prune (A-B pruning)

        return value

    if terminal(board):
        return None

    else:
        if player(board) == X: # maximizing player
            print("Thinking...")
            best_move = max_action(board)
            print("Move decided!")
            return best_move

        elif player(board) == O: # minimizing player
            print("Thinking...")
            best_move = min_action(board)
            print("Move decided!")
            return best_move
