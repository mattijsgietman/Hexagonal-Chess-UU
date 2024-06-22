from HexBoard import HexBoard
from Player import Player, Agent
import time

class Main():
    def __init__(self):
        self.hexboard = HexBoard()
        self.hexboard.load_puzzle("5")
        self.player1 = Agent()
        self.player1._init_("white", "min_max")
        self.player2 = Agent()
        self.player2._init_("black", "random")
        self.current_player = self.player1
        self.game_over = False
        self.winner = ""
        puzzels = ["1", "2", "3", "4", "5", "6"]
        stats = []

    def play(self):
        """
        Plays the game.
        """
        dictionary = {'white': 0, 'black': 0, 'remise': 0}
        total_games = 1
        start_time = time.time()

        for i in range(total_games):
            self.hexboard.print_hexboard()
            while not self.game_over:

                if self.current_player.agent_type == "random":
                    move = self.current_player.get_random_move(self.hexboard)
                    self.hexboard.move_piece(move, final=True)

                elif self.current_player.agent_type == "min_max":
                    move_timer_start = time.time()
                    move = self.current_player.find_min_max_move(self.hexboard, self.current_player.color, use_multiprocessing=True, use_alpha_beta=False)
                    self.hexboard.move_piece(move, final=True)
                    move_timer_end = time.time()
                    print(f"Move time: {move_timer_end - move_timer_start} seconds")

                opponent = self.player1 if self.current_player == self.player2 else self.player2
                self.game_over, self.winner = self.hexboard.is_game_over(opponent.color)

                if self.game_over:
                    dictionary[self.winner] += 1
                
                self.current_player = self.player1 if self.current_player == self.player2 else self.player2

                print(move)
                self.hexboard.print_hexboard()
            self.__init__()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed Total time: {elapsed_time} seconds")
        print(dictionary)

if __name__ == "__main__":
    main = Main() 
    main.play()