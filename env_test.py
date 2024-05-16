import HexagonalChessEnv
import numpy as np
import time
import random

env = HexagonalChessEnv.HexagonalChessEnv()
hexboard = env.hexboard
obs = env.reset()
done = False

while not done:
    action = random.choice(env.hexboard.get_legal_moves(env.current_player)) if env.hexboard.get_legal_moves(env.current_player) != [] else None
    obs, reward, done, info = env.step(action)

    if done:
        print("Game over!")
        print(f"Reward: {reward}")
        env.render()

