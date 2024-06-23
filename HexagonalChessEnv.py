import gym
from gym import spaces
import numpy as np
from HexBoard import HexBoard
from CONST import POSITIONS

class HexagonalChessEnv(gym.Env):
    def __init__(self):
        super(HexagonalChessEnv, self).__init__()

        self.hexboard = HexBoard()
        
        self.valid_positions = POSITIONS
        self.position_to_index = {pos: idx for idx, pos in enumerate(self.valid_positions)}
        self.index_to_position = {idx: pos for pos, idx in self.position_to_index.items()}

        num_positions = len(self.valid_positions)
        
        self.action_space = spaces.Discrete(num_positions * num_positions)
        self.observation_space = spaces.Box(low=0, high=12, shape=(num_positions,), dtype=np.int32)

        self.current_player = 'white'

    def reset(self):
        self.hexboard = HexBoard()
        self.current_player = 'white'
        observation = self._get_observation()
        return observation

    def step(self, action):
        if action is not None:
            self.hexboard.move_piece(action, final=True)
            
            if self.hexboard.is_game_over(self.current_player)[0]:
                reward = 100
                done = True
            elif self.hexboard.is_game_over('black')[0]:
                reward = 0
                done = True
            else:
                reward = 0
                done = False
            
            self.current_player = 'black' if self.current_player == 'white' else 'white'
        else:
            reward = 0
            done = True

        observation = self._get_observation()
        info = {}
        
        return observation, reward, done, info
    '''
    def _get_observation(self):
        board_state = np.zeros(len(self.valid_positions), dtype=np.int32)
        for idx, (row, col) in enumerate(self.valid_positions):
            piece = self.hexboard.get_piece(row, col)
            if piece is not None:
                board_state[idx] = self._piece_to_int(piece)
        return board_state
    '''
    def _get_observation(self):
        board_state = np.zeros(1092)
        pieces = ["p", "k", "b", "r", "q", "k", "P", "K", "B", "R", "Q", "K"]
        for piece in pieces:
            for row in self.hexboard.hexboard:
                for hexagon in row:
                    if hexagon is not None:
                        if hexagon.piece is not None:
                            if hexagon.piece.name == piece:
                                board_state[self.position_to_index[(hexagon.row, hexagon.col)]] = 1
        return board_state

    def _piece_to_int(self, piece):
        piece_dict = {
            'Pawn': 1,
            'Knight': 2,
            'Bishop': 3,
            'Rook': 4,
            'Queen': 5,
            'King': 6
        }
        return piece_dict.get(piece.__class__.__name__, 0) * (1 if piece.color == 'white' else -1)

    def render(self):
        self.hexboard.print_hexboard()
