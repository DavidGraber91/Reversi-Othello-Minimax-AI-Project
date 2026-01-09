"""
Name: David Graber
Email: D3217453@gmail.com
Date: 14/12/2025

This module implements core game logic for a two-player board game
similar to Reversi (Othello).

The board is represented as a 2D NumPy array.
Each cell can be:
    0  -> EMPTY
    1  -> PLAYER_RED
   -1  -> PLAYER_WHITE

Players place a piece on the board, and opponent pieces are flipped
in all valid directions according to the game rules.
"""
import numpy as np


# Cell states
EMPTY = 0
PLAYER_RED = 1
PLAYER_WHITE = -1

ROW = 0
COL = 1

# Console display symbols for each cell type
DISPLAY_PLAYERS = [''] * 3
DISPLAY_PLAYERS[PLAYER_RED] = "\033[41m" + 'x' +'\033[0m'
DISPLAY_PLAYERS[PLAYER_WHITE] = "\033[47m" + "o"+ '\033[0m'
DISPLAY_PLAYERS[EMPTY] = '-'


# Direction vectors (row, column)
STEP_UP = [-1, 0]
STEP_DOWN = [1, 0]
STEP_LEFT = [0, -1]
STEP_RIGHT = [0, 1]
STEP_UP_RIGHT = [-1, 1]
STEP_DOWN_RIGHT = [1, 1]
STEP_UP_LEFT = [-1, -1]
STEP_DOWN_LEFT = [1, -1]

"""
Attempts to place a piece for the given player at the specified position.

The move is valid only if at least one opponent piece is flipped
in any direction.

:param state: 2D NumPy array representing the board
:param player: current player (PLAYER_RED or PLAYER_WHITE)
:param action: (row, col) tuple of the target position
:return: True if the move is valid and applied, False otherwise
"""
def step(state , player, action):

    i = action[ROW]
    j = action[COL]

    if state[i][j] != EMPTY:
        return False

    done = step_direction(state, player, STEP_UP, action) \
           | step_direction(state, player, STEP_DOWN, action) \
           | step_direction(state, player, STEP_LEFT, action) \
           | step_direction(state, player, STEP_RIGHT, action) \
           | step_direction(state, player, STEP_UP_RIGHT, action) \
           | step_direction(state, player, STEP_DOWN_RIGHT, action) \
           | step_direction(state, player, STEP_DOWN_LEFT, action) \
           | step_direction(state, player, STEP_UP_LEFT, action)

    return done

"""
Applies a move in a single direction and flips opponent pieces
if the move is valid in that direction.

:param state: game board
:param player: current player
:param dire: direction vector (row, col)
:param action: starting position
:return: True if pieces were flipped, False otherwise
"""
def step_direction(state: np, player, dire, action):

    i = action[ROW]
    j = action[COL]

    if(count_flips(state, player, dire, action) == 0):
        return False

    row = dire[ROW]
    col = dire[COL]

    state[i][j] = player

    i += row
    j += col

    inindex = 0 <= i < len(state) and 0 <= j < len(state[i])

    while inindex and state[i][j] != player:
        state[i][j] = player
        i += row
        j += col
        inindex = 0 <= i < len(state) and 0 <= j < len(state[i])

    return True

"""
Counts how many pieces would be flipped if a move is played.

:return: total number of flippable opponent pieces
"""
def total_flips(state, player, action):
    if state[action[ROW]][action[COL]]:
        return 0
    num = count_flips(state, player, STEP_UP, action) + \
          count_flips(state, player, STEP_DOWN, action) + \
          count_flips(state, player, STEP_LEFT, action) + \
          count_flips(state, player, STEP_RIGHT, action) + \
          count_flips(state, player, STEP_UP_RIGHT, action) + \
          count_flips(state, player, STEP_DOWN_RIGHT, action) + \
          count_flips(state, player, STEP_DOWN_LEFT, action) + \
          count_flips(state, player, STEP_UP_LEFT, action)

    return num

"""
Checks how many opponent pieces can be flipped in a given direction.

:return: number of flippable pieces (0 if move is invalid)
"""
def count_flips(state: np, player, dire, action):

    count = 0

    i = action[ROW]
    j = action[COL]

    other_player = ~player + 1
    row = dire[0]
    col = dire[1]

    i += row
    j += col

    inindex = 0 <= i < len(state) and 0 <= j < len(state[i])

    while inindex and state[i][j] == other_player:
        i += row
        j += col
        count += 1

        inindex = 0 <= i < len(state) and 0 <= j < len(state[i])
    if not inindex or state[i][j] != player:
        return 0

    return count

"""
Prints the board state to the console using colored symbols.
"""
def display (state):
    for row in state:
        for cell in row:
            print(DISPLAY_PLAYERS[cell], end=' ')
        print()

"""
Checks whether a piece at position (i, j) is blocked in all directions.
"""
def is_blocked(state, i, j):
    return blocked(state,STEP_UP, STEP_DOWN,  i, j) and \
            blocked(state,STEP_LEFT, STEP_RIGHT, i, j) and \
            blocked(state,STEP_UP_RIGHT, STEP_DOWN_LEFT, i, j) and \
            blocked(state, STEP_DOWN_RIGHT, STEP_UP_LEFT, i, j)

"""
Checks whether a piece is blocked along a pair of opposite directions.

:return: True if blocked, False otherwise
"""
def blocked(state,dire1, dire2, k, t):

    i = k
    j = t

    player = state[i][j]

    row = dire1[0]
    col = dire1[1]

    i += row
    j += col

    inindex = 0 <= i < len(state) and 0 <= j < len(state[i])
    while inindex and state[i][j] != player:
        i += row
        j += col

        inindex = 0 <= i < len(state) and 0 <= j < len(state[i])

    if not inindex:
        return True

    if state[i][j] == EMPTY:
        return False

    i = k
    j = t

    player = state[i][j]

    row = dire2[0]
    col = dire2[1]

    i += row
    j += col

    inindex = 0 <= i < len(state) and 0 <= j < len(state[i])
    while inindex and state[i][j] != player:
        i += row
        j += col

        inindex = 0 <= i < len(state) and 0 <= j < len(state[i])

    if not inindex:
        return True

    if state[i][j] == EMPTY:
        return False

    return True