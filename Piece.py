from Move import Move

class Piece():
    def __init__(self, color, index=None):
        self.color = color
        self.value = 0
        self.index = index

    def set_color(self, color):
        self.color = color
    
    def get_color(self):
        return self.color

    def __lt__(self, other):
        if isinstance(other, Piece):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Piece):
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Piece):
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Piece):
            return self.value >= other.value
        return NotImplemented

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.en_passant = False
        self.value = 10 if self.color == "white" else -10
        self.name = "p" if self.color == "white" else "P"
        self.total_moves = 0
    
    def _get_legal_moves(self, row, col, hexboard):
        moves = []

        # Check if there is an empty space two rows above (for white) or two rows below (for black)
        target = (row - 2, col) if self.color == "white" else (row + 2, col)
        if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
            piece_on_target = hexboard.get_piece(target[0], target[1])
            if piece_on_target is None:
                move = Move(self, (row, col), target, None)
                moves.append(move)
        
        # Check if it's the first move and there are empty spaces four rows above (for white) or four rows below (for black)
        if self.first_move:
            target_first_move = (row - 4, col) if self.color == "white" else (row + 4, col)
            if 0 <= target_first_move[0] < 21 and 0 <= target_first_move[1] < 11 and hexboard.get_hexagon(target_first_move[0], target_first_move[1]) is not None:
                piece_on_target_first_move = hexboard.get_piece(target_first_move[0], target_first_move[1])
                if piece_on_target is None and piece_on_target_first_move is None:
                    move = Move(self, (row, col), target, None)
                    moves.append(move)
        
        # Check if there is an opponent's piece one row above and one column to the left (for white) or one row below and one column to the right (for black)
        target = (row - 1, col - 1) if self.color == "white" else (row + 1, col + 1)
        if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
            piece_on_target = hexboard.get_piece(target[0], target[1])
            if piece_on_target is not None and piece_on_target.color != self.color:
                move = Move(self, (row, col), target, piece_on_target)
                moves.append(move)
        
        # Check if there is an opponent's piece one row above and one column to the right (for white) or one row below and one column to the left (for black)
        target = (row - 1, col + 1) if self.color == "white" else (row + 1, col - 1)
        if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
            piece_on_target = hexboard.get_piece(target[0], target[1])
            if piece_on_target is not None and piece_on_target.color != self.color:
                move = Move(self, (row, col), target, piece_on_target)
                moves.append(move)

        return moves

    def set_en_passant(self, en_passant):
        self.en_passant = en_passant
    
    def get_en_passant(self):
        return self.en_passant
    
    def set_first_move(self, first_move):
        self.first_move = first_move
    
    def get_first_move(self):
        return self.first_move

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = 30 if self.color == "white" else -30
        self.name = "n" if self.color == "white" else "N"
        self.directions = [
            (-5, -1), (-4, -2), (-5, 1), (-4, 2),
            (-1, 3), (1, 3), (1, -3), (-1, -3),
            (5, -1), (4, -2), (5, 1), (4, 2)
        ]
    
    def _get_legal_moves(self, row, col, hexboard):
        moves = []
        for direction in self.directions:
            target = (row + direction[0], col + direction[1])
            if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                piece_on_target = hexboard.get_piece(target[0], target[1])
                if piece_on_target is None or piece_on_target.color != self.color:
                    move = Move(self, (row, col), target, piece_on_target)
                    moves.append(move)

        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = 30 if self.color == "white" else -30
        self.name = "b" if self.color == "white" else "B"
        self.directions = [(-3, -1), (-3, 1), (3, -1), (3,1), (0,2), (0,-2)]
    
    def _get_legal_moves(self, row, col, hexboard):
        moves = []

        for direction in self.directions:
            counter = 1
            while True:
                target = (row + counter * direction[0], col + counter * direction[1])
                if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                    piece_on_target = hexboard.get_piece(target[0], target[1])
                    if piece_on_target is None:
                        move = Move(self, (row, col), target, piece_on_target)
                        moves.append(move)
                    else:
                        if piece_on_target.color != self.color:
                            move = Move(self, (row, col), target, piece_on_target)
                            moves.append(move)
                        break   
                    counter += 1
                else:
                    break
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = 50 if self.color == "white" else -50
        self.name = "r" if self.color == "white" else "R"
        self.directions = [(-1, -1), (2,0), (1, 1), (-1,1), (-2,0), (1,-1)]
    
    def _get_legal_moves(self, row, col, hexboard):
        moves = []

        for direction in self.directions:
            counter = 1
            while True:
                target = (row + counter * direction[0], col + counter * direction[1])
                if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                    piece_on_target = hexboard.get_piece(target[0], target[1])
                    if piece_on_target is None:
                        move = Move(self, (row, col), target, piece_on_target)
                        moves.append(move)
                    else:
                        if piece_on_target.color != self.color:
                            move = Move(self, (row, col), target, piece_on_target)
                            moves.append(move)
                        break   
                    counter += 1
                else:
                    break

        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = 90 if self.color == "white" else -90
        self.name = "q" if self.color == "white" else "Q"
        self.directions = [(-1, -1), (2,0), (1, 1), (-1,1), (-2,0), (1,-1), (-3, -1), (-3, 1), (3, -1), (3,1), (0,2), (0,-2)]
        
    
    def _get_legal_moves(self, row, col, hexboard):
        moves = []

        for direction in self.directions:
            counter = 1
            while True:
                target = (row + counter * direction[0], col + counter * direction[1])
                if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                    piece_on_target = hexboard.get_piece(target[0], target[1])
                    if piece_on_target is None:
                        move = Move(self, (row, col), target, piece_on_target)
                        moves.append(move)
                    else:
                        if piece_on_target.color != self.color:
                            move = Move(self, (row, col), target, piece_on_target)
                            moves.append(move)
                        break   
                    counter += 1
                else:
                    break
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.first_move = True
        self.value = float("inf") if self.color == "white" else float("-inf")
        self.name = "k" if self.color == "white" else "K"
        self.directions = [(-1, -1), (2,0), (1, 1), (-1,1), (-2,0), (1,-1), (-3, -1), (-3, 1), (3, -1), (3,1), (0,2), (0,-2)]
 
    def _get_legal_moves(self, row, col, hexboard):
        moves = []

        for direction in self.directions:
            target = (row + direction[0], col + direction[1])
            if 0 <= target[0] < 21 and 0 <= target[1] < 11 and hexboard.get_hexagon(target[0], target[1]) is not None:
                piece_on_target = hexboard.get_piece(target[0], target[1])
                if piece_on_target is None or piece_on_target.color != self.color:
                    move = Move(self, (row, col), target, piece_on_target)
                    moves.append(move)

        return moves

