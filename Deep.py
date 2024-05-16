import gym
import HexagonalChessEnv
import numpy as np
from Agent import DQNAgent

env = HexagonalChessEnv.HexagonalChessEnv()
n_games = 1000
agent = DQNAgent(gamma=0.99, epsilon=1, lr=0.001, input_dims=(91,), batch_size=1638, n_actions=1638)

scores = []
eps_history = []

for i in range(n_games):
    done = False
    score = 0
    state = env.reset()

    while not done:
        if env.current_player == "white":
            legal_moves = env.hexboard.get_legal_moves(env.current_player)
            legal_actions = env.hexboard.legal_moves_to_actions(legal_moves)

            actions = agent.choose_action(state)
            if actions == None:
                print("Actions is None")

            for action in actions:
                converted_action = env.hexboard.action_to_tuple(action)
                if converted_action in legal_actions:
                    action = converted_action
                    break 
            
            if type(action) == int:
                done = True
                break

            action = env.hexboard.action_to_move(action) 
            state_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(state, actions[0], reward, state_, done)
            agent.learn()
            state = state_
        else:
            action = env.hexboard.random_black_move()
            state_, reward, done, info = env.step(action)
            state = state_

    scores.append(score)
    eps_history.append(agent.epsilon)

    if i % 10 == 0:
        avg_score = np.mean(scores[-10:])
        print(f'episode {i}, score {score}, average score {avg_score}, epsilon {agent.epsilon}')
