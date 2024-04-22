class Hex():
    """
    Represents a hexagon on a game board.

    Attributes:
        row (int): The row index of the hexagon.
        col (int): The column index of the hexagon.
        piece (str): The piece placed on the hexagon.

    Methods:
        set_row(row): Sets the row index of the hexagon.
        get_row(): Returns the row index of the hexagon.
        set_col(col): Sets the column index of the hexagon.
        get_col(): Returns the column index of the hexagon.
        set_piece(piece): Sets the piece placed on the hexagon.
        get_piece(): Returns the piece placed on the hexagon.
    """
    def __init__(self, row, col, piece):
        self.row = row
        self.col = col
        self.piece = piece

    def set_row(self, row):
        self.row = row
    
    def get_row(self):
        return self.row

    def set_col(self, col):
        self.col = col

    def get_col(self):
        return self.col

    def set_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece
