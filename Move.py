class Move:
    """
    Represents a move in a game.

    Attributes:
        piece (Piece): The piece involved in the move.
        initial (Hexagon): The initial hexagon from which the piece is moved.
        target (Hexagon): The target hexagon to which the piece is moved.
        enemy_piece (Piece): The enemy piece that may be captured during the move.
    """

    def __init__(self, piece, initial, target, enemy_piece):
        """
        Initialize a Move object.

        Args:
            piece: The piece being moved.
            initial: The initial position of the piece.
            target: The target position of the piece.
            enemy_piece: The enemy piece at the target position (if any).

        Returns:
            None
        """
        self.piece = piece
        self.initial = initial
        self.target = target
        self.enemy_piece = enemy_piece

    def __eq__(self, other):
        """
        Check if two Move objects are equal.

        Args:
            other (Move): The other Move object to compare with.

        Returns:
            bool: True if the initial and target positions of both Move objects are equal, False otherwise.
        """
        return self.initial == other.initial and self.target == other.target
    
    def __str__(self):
        """
        Returns a string representation of the Move object.

        The string includes information about the piece, initial hexagon, target hexagon, and enemy piece (if applicable).

        Returns:
            str: A string representation of the Move object.
        """
        piece_str = f"Piece: {self.piece.color} {self.piece.name}" if self.piece else "Piece: None"
        initial_str = f"Initial hexagon: {self.initial}" if self.initial else "Initial hexagon: None"
        target_str = f"Target hexagon: {self.target}" if self.target else "Target hexagon: None"
        enemy_piece_str = f"Enemy piece: {self.enemy_piece.color} {self.enemy_piece.name}" if self.enemy_piece else "Enemy piece: None"
        
        return f"{piece_str}, {initial_str}, {target_str}, {enemy_piece_str}"
