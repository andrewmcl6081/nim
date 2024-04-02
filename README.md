# Nim Game Implementation

This project implements the classic game of Nim in Python, featuring two variations: standard and misere. In this game, players take turns removing marbles from two piles, with the goal varying by the game version. The project employs a minmax algorithm with alpha-beta pruning for the computer player's decision-making process, offering a challenging oponent for human players

## Game Variations

- **Standard**: The player to remove the last marble loses.
- **Misere**: The player to remove the last marble wins.

## Features

- Two game modes: standard and misere.
- Play against a computer agent with strategic decision-making
- Specify starting conditions including the number of marbles in each pile, the version wished to play, and who takes the first turn
- Minmax algorithm implementation to decide computer's optimal move
- Alpha-beta pruning to efficiently improve performance of path exploration

## Requirements

- Python 3.x

## How to Run

To play the game, clone this repository and run the script from the command line with Python. The game accepts command-line arguments to set up the initial conditions.

```bash
python red_blue_nim.py <red_marbles> <blue_marbles> [version] [starting_player]
```

## Example
```bash
python red_blue_nim.py 5 5 standard computer
```
