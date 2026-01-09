"""
Name: David Graber
Email: D3217453@gmail.com
Date: 14/12/2025

This module defines the Game class, which manages the state and flow
of a Reversi (Othello) game.

Responsibilities:
- Hold the current board state
- Track the current player's turn
- Apply moves and switch turns
- Detect terminal game states
- Evaluate game utility and heuristics
"""

from copy import copy
import State
from State import EMPTY, PLAYER_RED, PLAYER_WHITE
import numpy as np

SIZE = 8

class Game:
    """
    Represents a single Reversi game instance.
    """

    def __init__(self):
        """
        Initializes a new game with an empty board,
        sets the starting player, and places the initial disks.
        """

        self.state = np.full((SIZE, SIZE), EMPTY)
        self.turn = PLAYER_RED
        self.num_states = 0
        self.initial_state()

    def __copy__(self):
        """
        Creates a shallow copy of the game instance.
        Used for simulations without modifying the original game.
        """

        temp = Game()
        temp.state = copy(self.state)
        temp.turn = self.turn
        temp.num_states = self.num_states
        return temp

    def initial_state(self):
        """
        Sets the initial four disks in the center of the board.
        """

        center = (int)(SIZE / 2)
        self.state[center][center] = self.state[center - 1][center - 1] = PLAYER_WHITE
        self.state[center][center - 1] = self.state[center - 1][center] = PLAYER_RED

    def step(self, action):
        """
        Applies a move for the current player.

        If the move is valid:
        - Updates the board
        - Switches the current turn
        - Increments the number of applied states

        :param action: [row, col] position
        :return: True if the move was applied, False otherwise
        """

        if State.step(self.state, self.turn, action):
            self.turn = ~self.turn + 1
            self.num_states += 1
            if self.no_move():
                self.turn = ~self.turn + 1
            return True
        return False

    def state_terminal(self):
        """
        Determines whether the game has reached a terminal state.

        A game ends when:
        - The board is full (except initial 4 cells), or
        - No legal moves are available for the current player
        """

        if self.num_states == SIZE * SIZE - 4:
            return True
        if self.no_move():
            return True
        return False

    def no_move(self):
        for i in range(SIZE):
            for j in range(SIZE):
                num = State.total_flips(self.state, self.turn, [i , j])
                if num > 0:
                    return False
        return True

    def count_disks(self):
        """
        Counts the number of disks for each player.

        :return: (red_count, white_count)
        """

        playerred = playerwhite = 0
        for row in self.state:
            for cell in row:
                if cell == PLAYER_RED:
                    playerred += 1
                if cell == PLAYER_WHITE:
                    playerwhite += 1

        return playerred, playerwhite

    def utility(self):
        """
        Computes the utility value of the current state.

        :return:
            1  if red wins
           -1  if white wins
            0  if draw
        """

        playerred, playerwhite = self.count_disks()

        if playerred > playerwhite:
            return 1
        if playerred < playerwhite:
            return -1
        if playerred == playerwhite:
            return 0

    def heuristics (self):
        """
        Computes a heuristic evaluation of the board state.

        The heuristic is based on:
        - Disk difference
        - Blocked disks
        - Average number of possible flips per move
        """

        heuristic = 0
        for i in range(SIZE):
            for j in range(SIZE):
                heuristic += self.state[i][j]
                if State.is_blocked(self.state, i, j):
                    heuristic += 1 * self.state[i][j]
        heuristic += self.average_steps()
        return heuristic / (SIZE * SIZE * 2)

    def average_steps(self):
        """
        Computes an estimate of move quality for both players,
        based on the average number of disks flipped per valid move.
        """

        player_red_steps = 0
        player_white_steps = 0
        player_red_disks = 0
        player_white_disks = 0

        for i in range(SIZE):
            for j in range(SIZE):
                temp = State.total_flips(self.state, PLAYER_RED, [i, j])
                if temp > 0:
                        player_red_steps += 1
                        player_red_disks += temp

                temp = State.total_flips(self.state, PLAYER_WHITE, [i, j])
                if temp > 0:
                    player_white_steps += 1
                    player_white_disks += temp

        if player_red_steps == 0:
            player_red_steps = 1
        if player_white_steps == 0:
            player_white_steps = 1

        return (player_red_disks / player_red_steps) + (player_white_disks / player_white_steps) * -1


    def first_step(self):
        """
        Checks whether at least one legal move exists
        for the current player.
        """

        for i in range(SIZE):
            for j in range(SIZE):
                if self.step([i, j]):
                    return True
        return False

    def displayAllActions(self):
        """
        Debugging utility that displays all possible legal moves
        from the current state and their resulting boards.
        """

        #State.display(self.state)
        strings = ['', 'red', 'white']
        temp  = copy(self)
        #State.display(temp.state)
        for i in range(SIZE):
            for j in range(SIZE):
                if temp.step([i,j]):
                    red, white = temp.count_disks()
                    print(f"State {self.num_states}")
                    State.display(self.state)
                    print(f"\nState {temp.num_states}, "
                          f"Player {strings[self.turn]} moved, "
                          f"Action in sell ({i}, {j})")
                    State.display(temp.state)
                    print(f"Result - Player red: {red}"
                          f", Player white: {white}, "
                          f"Total: {red + white}")
                    print("\n====================================================================\n")
                    temp  = copy(self)

