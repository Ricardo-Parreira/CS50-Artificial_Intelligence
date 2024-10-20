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

def new_copy(board):
    new_board = []
    for i in range(3):
        new_board.append([])
        for j in range(3):
            new_board[i].append(board[i][j])
    return new_board

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
    new_board = new_copy(board)
    (i, j) = action
    if i>=3 or i<0 or j>=3 or j<0: #out of bounds
        raise NameError('Action is out of bounds')
    if board[i][j] == O or board[i][j] == X:
        raise NameError('Spot is taken')

    new_board[i][j] = player(new_board)
    return new_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    aux_set = set()

    # horizontally
    for i in range(3):
        for j in range(3):
            aux_set.add(board[i][j])
        if len(aux_set) == 1:
            element = aux_set.pop()
            if element != EMPTY:
                return element
        aux_set.clear()

    #vertically
    for j in range(3):
        for i in range(3):
            aux_set.add(board[i][j])
        if len(aux_set) == 1:
            element = aux_set.pop()
            if element != EMPTY:
                return element
        aux_set.clear()

    #diagonally
    for i in range(3):
       aux_set.add(board[i][i])
    if len(aux_set) == 1:
        element = aux_set.pop()
        if element != EMPTY:
            return element
    aux_set.clear()

    for i in range(3):
       aux_set.add(board[2-i][i])
    if len(aux_set) == 1:
        element = aux_set.pop()
        if element != EMPTY:
            return element
    aux_set.clear()


    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win = winner(board)
    if win == O or win == X:
        return True
    if len(actions(board)) == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == O:
        return -1
    if win == X:
        return 1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    acoes = actions(board)
    if terminal(board):
        return None
    if len(acoes) == 1:
        return acoes.pop()


    best = None

    new_board = new_copy(board)
    if player(new_board) == X:
        maximo = float('-inf')
        for action in acoes:

            new_board = result(board, action)
            if terminal(new_board):     #se o move causar o fim do jogo significa que ganhámos
                return action
            score = minimizer(new_board, maximo)
            if score > maximo:
                best = action
                maximo = score


    if player(board) == O:
        minimo = float('inf')
        for action in acoes:
            new_board = result(board, action)
            if terminal(new_board):
                return action
            score = maximizer(new_board, minimo)
            if score < minimo:
                best = action

                (x,y) = best

                minimo = score

    return best


def maximizer(board, maximo):
    if terminal(board):

        return utility(board)

    maximo = float('-inf')
    for action in actions(board):
        (x,y) = action
        new_board = new_copy(board)
        new_board = result(board,action)
        maximo = max(maximo, minimizer(new_board, maximo))

    return maximo

def minimizer(board, minimo):
    if terminal(board):
        return utility(board)

    minimo = float('inf')
    for action in actions(board):
        new_board = new_copy(board)
        new_board = result(board,action)
        minimo = min(minimo, maximizer(new_board, minimo))

    return minimo







