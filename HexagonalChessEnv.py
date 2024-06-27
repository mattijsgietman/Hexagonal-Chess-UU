import gym
from gym import spaces
import numpy as np
from HexBoard import HexBoard
from CONST import POSITIONS

class HexagonalChessEnv(gym.Env):
    """
    Environment class for the game of Hexagonal Chess.

    This class implements the OpenAI Gym environment interface and provides methods for interacting with the environment.

    Attributes:
        hexboard (HexBoard): The hexagonal chess board.
        valid_positions (list): List of valid positions on the hexagonal chess board.
        position_to_index (dict): Mapping of positions to their corresponding indices.
        index_to_position (dict): Mapping of indices to their corresponding positions.
        action_space (gym.Space): The action space of the environment.
        observation_space (gym.Space): The observation space of the environment.
        current_player (str): The current player ('white' or 'black').

    Methods:
        __init__(): Initializes the HexagonalChessEnv object.
        reset(): Resets the environment to its initial state.
        step(action): Takes a step in the environment given an action.
        _get_observation(): Returns the current observation of the environment.
        _piece_to_int(piece): Converts a chess piece object to an integer representation.
        render(): Renders the current state of the hexagonal chess board.
    """

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
        """
        Resets the environment to its initial state.

        Returns:
            observation (np.ndarray): The initial observation of the environment.
        """
        self.hexboard = HexBoard()
        self.current_player = 'white'
        observation = self._get_observation()
        return observation

    def step(self, action):
        """
        Takes a step in the environment given an action.

        Args:
            action: The action to take in the environment.

        Returns:
            observation (np.ndarray): The new observation of the environment.
            reward (float): The reward for the current step.
            done (bool): Whether the episode is done or not.
            info (dict): Additional information about the step.
        """
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

    def _get_observation(self):
        """
        Returns the current observation of the environment.

        Returns:
            board_state (np.ndarray): The current state of the hexagonal chess board.
        """
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
        """
        Converts a chess piece object to an integer representation.

        Args:
            piece: The chess piece object.

        Returns:
            int: The integer representation of the chess piece.
        """
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
        """
        Renders the current state of the hexagonal chess board.
        """
        self.hexboard.print_hexboard()
