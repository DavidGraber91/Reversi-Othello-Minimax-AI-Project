"""

This module implements the Minimax algorithm with Alpha-Beta pruning
for the Reversi (Othello) game.

It evaluates game states using:
- Terminal utility values
- A heuristic evaluation for non-terminal states
"""
from copy import copy\

from Game import Game, SIZE
from State import EMPTY, PLAYER_RED, PLAYER_WHITE

MAX_UTILITY = 1
MIN_UTILITY = -1

def minimax(geme : Game, depth):
    """
    Selects the best move for the current player using Minimax
    with Alpha-Beta pruning.

    :param game: current game state
    :param depth: search depth
    :return: best action [row, col]
    """

    if geme.turn == PLAYER_RED:
        value ,action = max_value(geme, depth, MIN_UTILITY, MAX_UTILITY)
    else: value ,action = min_value(geme, depth, MIN_UTILITY, MAX_UTILITY)
    return action

def max_value(geme : Game, depth, a, b):
    """
    Maximizing player (PLAYER_RED).

    Returns the maximum achievable value from the current state,
    while pruning branches using alpha-beta bounds.
    """

    # Terminal state
    if geme.state_terminal():
        return geme.utility(), None

    # Depth limit reached
    if depth == 0:
        return geme.heuristics(), None

    move = []
    tempstate: Game
    value = MIN_UTILITY
    temp_value: float

    tempstate = copy(geme)
    for i in range(SIZE):
        for j in range(SIZE):
            if tempstate.step([i , j]):
                temp_value, temp = min_value(tempstate, depth - 1, a, b)

                if temp_value >= value:
                    value = temp_value
                    move = [i, j]
                    a = max(a, value)

                    # Alpha-Beta pruning
                    if value >= b:
                        return value, move
                tempstate = copy(geme)

    return value , move


def min_value(geme : Game, depth, a, b):
    """
    Minimizing player (PLAYER_WHITE).

    Returns the minimum achievable value from the current state,
    while pruning branches using alpha-beta bounds.
    """

    # Terminal state
    if geme.state_terminal():
        return geme.utility(), None


    # Depth limit reached
    if depth == 0:
        return geme.heuristics(), None

    move = []
    tempstate: Game
    value = MAX_UTILITY
    temp_value: float

    tempstate = copy(geme)
    for i in range(SIZE):
        for j in range(SIZE):
            if tempstate.step([i, j]):
                temp_value, temp = max_value(tempstate, depth - 1, a, b)

                if temp_value <= value:
                    value = temp_value
                    move = [i, j]
                    b = min(b, value)

                    if value <= a:
                        return value, move
                tempstate = copy(geme)

    return value , move


