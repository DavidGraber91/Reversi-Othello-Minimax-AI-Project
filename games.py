"""

This module provides utility functions for running and visualizing
Reversi (Othello) games using different strategies.

It supports:
- Displaying all possible actions from a given state
- Running a game with naive move selection
- Running a game controlled by the Minimax algorithm
"""
from Game import Game
import State
from minimax import minimax

def display_all_actins(num=7):
    """
    Advances the game a fixed number of moves and then displays
    all possible legal actions from the resulting state.

    :param num: total number of moves to advance before displaying actions
    """

    g = Game()
    for i in range(num - 4):
        g.first_step()

    g.displayAllActions()


def methodical(n=5):
    """
    Plays the game step-by-step using the first legal move found.

    The board is displayed after each move until the game ends.

    :param n: number of initial moves to display before auto-playing
    """


    g = Game()
    for i in range(n):
        State.display(g.state)
        print('-----------------------------------------------')
        g.first_step()

    while(not g.state_terminal()):
        g.first_step()

    State.display(g.state)

def H(num):
    """
    Runs a full game where moves are selected using the Minimax algorithm.

    After final game, the board state is displayed.
    """

    g = Game()

    while(not g.state_terminal()):
        g.step(minimax(g, num))


    State.display(g.state)
