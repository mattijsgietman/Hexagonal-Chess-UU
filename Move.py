class Move:
    def __init__(self, piece, initial, target, enemy_piece):
        self.piece = piece
        self.initial = initial
        self.target = target
        self.enemy_piece = enemy_piece

    def __eq__(self, other):
        return self.initial == other.initial and self.target == other.target
    
    def __str__(self):
        piece_str = f"Piece: {self.piece.color} {self.piece.name}" if self.piece else "Piece: None"
        initial_str = f"Initial hexagon: {self.initial}" if self.initial else "Initial hexagon: None"
        target_str = f"Target hexagon: {self.target}" if self.target else "Target hexagon: None"
        enemy_piece_str = f"Enemy piece: {self.enemy_piece.color} {self.enemy_piece.name}" if self.enemy_piece else "Enemy piece: None"
        
        return f"{piece_str}, {initial_str}, {target_str}, {enemy_piece_str}"
