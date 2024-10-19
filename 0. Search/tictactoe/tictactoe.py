"""
Tic Tac Toe Player
"""

import math

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
    if board == initial_state():
        return X
    if len(actions(board))%2 == 0:
        return O
    else:
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible.add((i,j))
    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new = board
    i, j = action
    if i>=3 or i<0 or j>=3 or j<0: #out of bounds
        raise NameError('Action is out of bounds')
    if board[i][j] != EMPTY:
        raise NameError('Spot is taken')

    new[i][j] = player(board)
    return new



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
