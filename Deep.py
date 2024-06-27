import gym
import HexagonalChessEnv
import numpy as np
from CONST import *
from Agent import DQNAgent
from Player import Agent
import matplotlib.pyplot as plt
import time

env = HexagonalChessEnv.HexagonalChessEnv()
n_games = 6500
agent = DQNAgent(gamma=0.85, epsilon=1, lr=0.001, input_dims=(1092,), batch_size=128, n_actions=1638)
#agent.load_models()
minmax = Agent()
minmax._init_("black", "min_max")

begin_time = time.time()

scores = []
eps_history = []

def get_valid_moves_mask(env, legal_moves):
    """
    Generates a mask indicating the valid moves in the given environment.

    Args:
        env: The environment object representing the game state.
        legal_moves: A list of legal moves in the current game state.

    Returns:
        mask: A numpy array of shape (1638,) representing the mask of valid moves.
              Each index in the mask corresponds to a specific move, and a value of 1
              indicates that the move is valid, while a value of 0 indicates that the
              move is invalid.
    """
    mask = np.zeros(1638, dtype=np.int32)

    if len(legal_moves) != 0:
        for move in legal_moves:
            piece = move.piece.index
            target_row, target_col = move.target
            index = piece * 91 + POS_IDX[(target_row, target_col)]
            mask[index] = 1

    return mask


for i in range(n_games):
    done = False
    score = 0
    move_counter = 0
    state = env.reset()

    while not done:
        if move_counter < MOVE_LIMIT:
            if env.current_player == "white":
                start_time = time.time()
                legal_moves = env.hexboard.get_legal_moves(env.current_player)
                legal_actions = env.hexboard.legal_moves_to_actions(legal_moves)
                valid_moves_mask = get_valid_moves_mask(env, legal_moves)

                actions = agent.choose_action(state, valid_moves_mask)
                if actions is None:
                    done = True
                    score = 0
                    continue

                for action in actions:
                    converted_action = env.hexboard.action_to_tuple(action)
                    if converted_action in legal_actions:
                        original_action = action
                        action = converted_action
                        break

                if type(action) == int:
                    done = True
                    score = 0
                    continue

                action = env.hexboard.action_to_move(action)
                state_, reward, done, info = env.step(action)
                score += reward
                if reward == 100:
                    score = 100
                if reward == -100:
                    score = 0
                agent.store_transition(state, original_action, reward, state_, done)
                agent.learn()
                state = state_
                move_counter += 1
                end_time = time.time()

            else:
                if len(env.hexboard.get_legal_moves(env.current_player)) != 0:
                    action = minmax.find_min_max_move(env.hexboard, env.current_player, False)
                    if action is None:
                        done = True
                        break
                    state_, reward, done, info = env.step(action)
                    state = state_
                    move_counter += 1
        else:
            score = 0
            done = True

    scores.append(score)
    eps_history.append(agent.epsilon)

    if i % 100 == 0:
        avg_score = np.mean(scores[-100:])
        print(f'episode {i}, score {score}, average score {avg_score}, epsilon {agent.epsilon}')

final_time = time.time()
print(f"Elapsed Total time: {final_time - begin_time} seconds")

save = input("Do you want to save the model? (y/n): ")
if save == "y":
    agent.save_models()
