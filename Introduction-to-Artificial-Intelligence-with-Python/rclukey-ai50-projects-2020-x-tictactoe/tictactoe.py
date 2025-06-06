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
    x_counter = 0
    o_counter = 0
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                x_counter += 1
            if board[i][j] == O:
                o_counter += 1
    
    if x_counter == o_counter:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    actions_list = set()
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions_list.add((i,j))
    
    return actions_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    new_board = initial_state()
    current_player = player(board)
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                new_board[i][j] = X
            elif board[i][j] == O:
                new_board[i][j] = O
    
    if board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = current_player
        return new_board
    else:
        raise Exception("Not a possible move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = None
    end = terminal(board)
    x_counter = 0
    
    if end:
        # Horizontals
        if board[0][0] == X and board[0][1] == X and board[0][2] == X or board[1][0] == X and board[1][1] == X and board[1][2] == X or board[2][0] == X and board[2][1] == X and board[2][2] == X:
            win = X
        elif board[0][0] == O and board[0][1] == O and board[0][2] == O or board[1][0] == O and board[1][1] == O and board[1][2] == O or board[2][0] == O and board[2][1] == O and board[2][2] == O:
            win = O
        
        # Verticals
        elif board[0][0] == X and board[1][0] == X and board[2][0] == X or board[0][1] == X and board[1][1] == X and board[2][1] == X or board[0][2] == X and board[1][2] == X and board[2][2] == X:
            end = X
        elif board[0][0] == O and board[1][0] == O and board[2][0] == O or board[0][1] == O and board[1][1] == O and board[2][1] == O or board[0][2] == O and board[1][2] == O and board[2][2] == O:
            end = O
        
        # Diagonals
        elif board[0][0] == X and board[1][1] == X and board[2][2] == X or board[0][2] == X and board[1][1] == X and board[2][0] == X:
            win = X
        elif board[0][0] == O and board[1][1] == O and board[2][2] == O or board[0][2] == O and board[1][1] == O and board[2][0] == O:
            win = O
    
        # Check if there is a tie
        elif empty_actions(board) == 0:
            win = None

    return win


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    x_counter = 0
    end = False
    
    # Check if there is a tie
    if empty_actions(board) == 0:
        end = True
    
    # Horizontals
    elif board[0][0] == X and board[0][1] == X and board[0][2] == X or board[0][0] == O and board[0][1] == O and board[0][2] == O:
        end = True
    elif board[1][0] == X and board[1][1] == X and board[1][2] == X or board[1][0] == O and board[1][1] == O and board[1][2] == O:
        end = True
    elif board[2][0] == X and board[2][1] == X and board[2][2] == X or board[2][0] == O and board[2][1] == O and board[2][2] == O:
        end = True
    
    # Verticals
    elif board[0][0] == X and board[1][0] == X and board[2][0] == X or board[0][0] == O and board[1][0] == O and board[2][0] == O:
        end = True
    elif board[0][1] == X and board[1][1] == X and board[2][1] == X or board[0][1] == O and board[1][1] == O and board[2][1] == O:
        end = True
    elif board[0][2] == X and board[1][2] == X and board[2][2] == X or board[0][2] == O and board[1][2] == O and board[2][2] == O:
        end = True
    
    # Diagonals
    elif board[0][0] == X and board[1][1] == X and board[2][2] == X or board[0][0] == O and board[1][1] == O and board[2][2] == O:
        end = True
    elif board[2][0] == X and board[1][1] == X and board[2][0] == X or board[0][2] == O and board[1][1] == O and board[2][0] == O:
        end = True
    
    return end


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    elif winner(board) == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    move = ()
    
    if player(board) == X:
        v = -math.inf
        for action in actions(board):
            score = min_value(result(board, action))
            if score > v:
                v = score
                move = action
            
    elif player(board) == O:
        v = math.inf
        for action in actions(board):
            score = max_value(result(board, action))
            if score < v:
                v = score
                move = action
    
    return move


def max_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
    return v


def empty_actions(board):
    counter = 0
    
    for i in board:
        for j in i:
            if j is EMPTY:
                counter += 1
    
    return counter























