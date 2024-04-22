class Hex():
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
