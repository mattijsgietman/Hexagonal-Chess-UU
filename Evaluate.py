class Evaluate():
    def __init__(self, hexboard):
        self.hexboard = hexboard
        self.evaluation = 0
        
        self.pawn_scores = []
        self.knight_scores = []
        self.bishop_scores = []
        self.rook_scores = []
        self.queen_scores = []
        self.knight_scores = []

    def evaluate(self, color):
        score = 0
        checkmate = False
        color = 'white' if color == 'black' else 'white'
        checkmate, winner = self.hexboard.is_game_over(color)

        if checkmate:
            if winner == "white":
                return float("inf")
            elif winner == "black":
                return float("-inf")
            else:
                return 0

        for row in self.hexboard.hexboard:
            for col in row:
                if col != None:
                    if col.get_piece() != None:
                        score += col.piece.value
        self.evaluate = score
        return score