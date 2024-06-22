import random
import multiprocessing
from Evaluate import Evaluate
from CONST import *

class Player():
    def _init_(self, color):
        self.color = color

    def get_move(self):
        pass

class Agent(Player):
    def _init_(self, color, agent_type):
        super()._init_(color)
        self.agent_type = agent_type
        self.nodes_explored = 0
    
    def get_random_move(self, hexboard):
        if self.agent_type == "random":
            legal_moves = hexboard.get_legal_moves(self.color)
            return random.choice(legal_moves)
        else:
            raise ValueError("Invalid agent type")
        
    def min_max_worker(self, args):
        move, hexboard, maximizing, depth, alpha, beta, use_alpha_beta = args
        hexboard.move_piece(move)
        evaluation = self.min_max(hexboard, not maximizing, depth, alpha, beta, use_alpha_beta)
        hexboard.undo_move(move)
        return (move, evaluation)

    def find_min_max_move(self, hexboard, color, use_multiprocessing=True, use_alpha_beta=True):
        if self.agent_type == "min_max":
            moves = hexboard.get_legal_moves(self.color)
            moves = sorted(moves, key=lambda move: (move.enemy_piece is None, move.enemy_piece))
            maximize = True if color == "white" else False

        self.nodes_explored = 0  # Reset node counter

        if use_multiprocessing:
            with multiprocessing.Pool() as pool:
                args = [(move, hexboard, maximize, DEPTH, float("-inf"), float("inf"), use_alpha_beta) for move in moves]
                results = pool.map(self.min_max_worker, args)
        else:
            args = [(move, hexboard, maximize, DEPTH, float("-inf"), float("inf"), use_alpha_beta) for move in moves]
            results = [self.min_max_worker(arg) for arg in args]

        # Find the move with the best evaluation
        best_move = max(results, key=lambda x: x[1]) if maximize else min(results, key=lambda x: x[1])
        
        #print(f"Total nodes explored: {self.nodes_explored}")
        
        return best_move[0]

    def min_max(self, hexboard, maximizing, depth=DEPTH, alpha=float("-inf"), beta=float("inf"), use_alpha_beta=True):
        if self.agent_type == "min_max":
            global next_move

            self.nodes_explored += 1

            if depth == 0:
                color = "white" if maximizing else "black"
                return Evaluate(hexboard).evaluate(color)
            
            if maximizing:
                max_evaluation = float("-inf")
                for move in hexboard.get_legal_moves(self.color):
                    hexboard.move_piece(move)
                    evaluation = self.min_max(hexboard, False, depth-1, alpha, beta, use_alpha_beta)
                    hexboard.undo_move(move)
                    if evaluation > max_evaluation:
                        max_evaluation = evaluation
                        if depth == DEPTH:
                            next_move = move
                    if use_alpha_beta:
                        alpha = max(alpha, evaluation)
                        if beta <= alpha:
                            break
                return max_evaluation
            else:
                min_evaluation = float("inf")
                opponent_color = "white" if self.color == "black" else "black"
                for move in hexboard.get_legal_moves(opponent_color):
                    hexboard.move_piece(move)
                    evaluation = self.min_max(hexboard, True, depth-1, alpha, beta, use_alpha_beta)
                    hexboard.undo_move(move)
                    if evaluation < min_evaluation:
                        min_evaluation = evaluation
                        if depth == DEPTH:
                            next_move = move
                    if use_alpha_beta:
                        beta = min(beta, evaluation)
                        if beta <= alpha:
                            break
                return min_evaluation