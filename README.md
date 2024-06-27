# Hexagon Chess Puzzles Solver

Welcome to the Hexagon Chess Puzzles Solver repository! This project focuses on solving hexagon chess puzzles posed by Glinski using a Min-Max algorithm with alpha-beta pruning and a Deep-Q-Learning agent.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithms](#algorithms)

## Introduction

This project aims to solve hexagon chess puzzles using two different approaches:
1. **Min-Max Algorithm with Alpha-Beta Pruning:** A classic AI technique to explore the game tree efficiently.
2. **Deep-Q-Learning Agent:** A machine learning approach that utilizes reinforcement learning.

## Features

- Implementation of Glinski's hexagonal chess rules.
- Solving puzzles using Min-Max algorithm with alpha-beta pruning.
- Solving puzzles using a Deep-Q-Learning agent.
- Comparison of results between the two approaches.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mattijsgietman/Hexagonal-Chess-UU.git
2. Change your directory to the location of the download:
   ```bash
   cd Hexagonal-Chess-UU
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Usage
To run the Min-Max solver, you'll just need to run 'Main.py' file. In this file, you'll also be able to select which of the 12 puzzles you'd like the agent to solve.

To run the Deep Q-Learning agent. You can run the 'Deep.py' file. This will automatically train an agent. If you'd like to load a pre-trained model, you'll have to uncomment the following line from the 'Deep.py' file: '#agent.load_models()'. Furthermore, it is important to specify what model to load in the 'load_models' file 'Agent.py'

## Algorithms
### Min-Max Algorithm with Alpha-Beta Pruning

The Min-Max algorithm is a decision-making algorithm used in game theory. Alpha-beta pruning is an optimization technique for the Min-Max algorithm that reduces the number of nodes evaluated in the search tree.

### Deep-Q-Learning Agent

Deep-Q-Learning is a reinforcement learning algorithm that combines Q-Learning with deep neural networks to solve problems that require decision making.
