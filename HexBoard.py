from openpyxl import load_workbook
import random

from Hex import Hex
from CONST import *
from Piece import *

class HexBoard():
    def __init__(self):
        self.hexboard = [[None for _ in range(11)] for _ in range(21)]
        self._create_board()
        self._setup_pieces()
        self.load_puzzle("2")

    def _create_board(self):
        for position in POSITIONS:
            row, col = position
            hexagon = Hex(row, col, None)
            self.hexboard[row][col] = hexagon
    
    def _setup_pieces(self):
        # Setting up the black pieces

        self.hexboard[0][5].piece = Bishop('black')
        self.hexboard[1][4].piece = Queen('black')
        self.hexboard[1][6].piece = King('black')
        self.hexboard[2][3].piece = Knight('black')
        self.hexboard[2][5].piece = Bishop('black')
        self.hexboard[2][7].piece = Knight('black')
        self.hexboard[3][2].piece = Rook('black')
        self.hexboard[3][8].piece = Rook('black')
        self.hexboard[4][1].piece = Pawn('black')
        self.hexboard[4][5].piece = Bishop('black')
        self.hexboard[4][9].piece = Pawn('black')
        self.hexboard[5][2].piece = Pawn('black')
        self.hexboard[5][8].piece = Pawn('black')
        self.hexboard[6][3].piece = Pawn('black')
        self.hexboard[6][7].piece = Pawn('black')
        self.hexboard[7][4].piece = Pawn('black')
        self.hexboard[7][6].piece = Pawn('black')
        self.hexboard[8][5].piece = Pawn('black')

        # Setting up the white pieces
        self.hexboard[20][5].piece = Bishop('white')
        self.hexboard[19][4].piece = Queen('white')
        self.hexboard[19][6].piece = King('white')
        self.hexboard[18][3].piece = Knight('white')
        self.hexboard[18][5].piece = Bishop('white')
        self.hexboard[18][7].piece = Knight('white')
        self.hexboard[17][2].piece = Rook('white')
        self.hexboard[17][8].piece = Rook('white')
        self.hexboard[16][1].piece = Pawn('white')
        self.hexboard[16][5].piece = Bishop('white')
        self.hexboard[16][9].piece = Pawn('white')
        self.hexboard[15][2].piece = Pawn('white')
        self.hexboard[15][8].piece = Pawn('white')
        self.hexboard[14][3].piece = Pawn('white')
        self.hexboard[14][7].piece = Pawn('white')
        self.hexboard[13][4].piece = Pawn('white')
        self.hexboard[13][6].piece = Pawn('white')
        self.hexboard[12][5].piece = Pawn('white')

        #Puzzle 1  
        self.hexboard[2][5].piece = King('black')
        self.hexboard[4][5].piece = Knight('black')
        self.hexboard[5][2].piece = Pawn('black')
        self.hexboard[16][7].piece = Queen('black')
        self.hexboard[9][6].piece = Rook('black')

        self.hexboard[5][0].piece = Rook('white')
        self.hexboard[6][5].piece = Queen('white')
        self.hexboard[13][8].piece = Pawn('white')
        self.hexboard[10][9].piece = King('white')

    def get_piece(self, row, col):
        # Check if the given position is valid
        if row < 0 or row > 20 or col < 0 or col > 10:
            raise ValueError("Invalid position")
        else:
            # Check if there is a piece at the given position
            if self.hexboard[row][col] is not None:
                return self.hexboard[row][col].piece
            else:
                return None

    def set_piece(self, row, col, piece):
        # Check if the given position is valid
        if row < 0 or row > 20 or col < 0 or col > 10:
            raise ValueError("Invalid position")
        else:
            # Set the piece at the given position
            self.hexboard[row][col].piece = piece
    
    def get_hexagon(self, row, col):
        # Check if the given position is valid
        if row < 0 or row > 20 or col < 0 or col > 10:
            raise ValueError("Invalid position")
        elif self.hexboard[row][col] is not None:
            return self.hexboard[row][col]
        return None
    
    def get_pieces_locations(self, color):
        # Get the locations of pieces
        locations = []
        for row in self.hexboard:
            for hexagon in row:
                if hexagon is not None:
                    if hexagon.piece is not None:
                        if hexagon.piece.color == color:
                            locations.append((hexagon.row, hexagon.col))
        return locations
    
    def get_king_location(self, color):
        for row in self.hexboard:
            for hexagon in row:
                if hexagon is not None:
                    if hexagon.piece is not None:
                        if hexagon.piece.color == color and isinstance(hexagon.piece, King):
                            return (hexagon.row, hexagon.col)

    def get_pseudo_legal_moves(self, color):
        legal_moves = []
        locations = self.get_pieces_locations(color) 

        for location in locations:
            row, col = location
            piece = self.get_piece(row, col)
            legal_moves += piece._get_legal_moves(row, col, self)
        return legal_moves
    
    def get_legal_moves(self, color):
        legal_moves = []
        moves = self.get_pseudo_legal_moves(color)
        for move in moves:
            self.move_piece(move)
            if not self.in_check(color):
                legal_moves.append(move)
            self.undo_move(move)
        return legal_moves
                
    def move_piece(self, move, final=False):
        initial = move.initial
        target = move.target
        piece = move.piece
        enemy_piece = move.enemy_piece
        initial_row, initial_col = initial
        target_row, target_col = target

        # Remove the piece from the initial position and place it at the target position
        self.hexboard[initial_row][initial_col].piece = None
        self.hexboard[target_row][target_col].piece = piece


        # Update the has_moved attribute for pawns and promote pawns to queens if they reach the last row
        if piece.name == 'p' or piece.name == 'P':
            if final:
                piece.has_moved = True
            if target in PAWN_PROMOTION_HEXAGONS:
                self.hexboard[target_row][target_col].piece = Queen(piece.color)
            piece.total_moves += 1

    def undo_move(self, move):
        initial = move.initial
        target = move.target
        piece = move.piece
        enemy_piece = move.enemy_piece
        initial_row, initial_col = initial
        target_row, target_col = target

        # Place the piece back at the initial position and remove it from the target position
        self.hexboard[initial_row][initial_col].piece = piece
        self.hexboard[target_row][target_col].piece = None

        # Place the enemy piece back at the target position (if any)
        if enemy_piece is not None:
            self.hexboard[target_row][target_col].piece = enemy_piece

        # Update the has_moved attribute for pawns and demote queens to pawns if they were promoted during the move
        if piece.name == 'p' or piece.name == 'P':
            if target_row == 0 or target_row == 20:
                self.hexboard[initial_row][initial_col].piece = Pawn(piece.color)
            piece.total_moves -= 1

            if piece.total_moves == 0:
                piece.has_moved = False

    def in_check(self, color):
        # Get the location of the king of the specified color
        king_location = self.get_king_location(color)

        # Check if any of the opponent's pieces can attack the king's position
        opponent_color = 'black' if color == 'white' else 'white'
        opponent_locations = self.get_pieces_locations(opponent_color)

        for location in opponent_locations:
            piece = self.get_piece(*location)
            if piece is not None:
                legal_moves = piece._get_legal_moves(*location, self)
                for move in legal_moves:
                    if move.target == king_location:
                        return True

        return False
 
    def is_game_over(self, color):
        # Check if the white king is in checkmate
        if self.in_check('white'):
            legal_moves = self.get_legal_moves('white')
            if len(legal_moves) == 0:
                return (True, 'black')

        # Check if the black king is in checkmate
        if self.in_check('black'):
            legal_moves = self.get_legal_moves('black')
            if len(legal_moves) == 0:
                return (True, 'white')
        
        if len(self.get_legal_moves(color)) == 0:
            return (True, 'remise')

        return (False, "")

    def print_hexboard(self):
        for row in self.hexboard:
            for hexagon in row:
                if hexagon is None:
                    print(" ", end="")
                else:
                    if hexagon.piece is not None:
                        print(hexagon.piece.name, end="")
                    else:
                        print("-", end="")
            print()

    def load_puzzle(self, puzzle):
        class_mapping = {
        'King': King,
        'Knight': Knight,
        'Bishop': Bishop,
        'Pawn': Pawn,
        'Queen': Queen,
        'Rook': Rook
        }
        self._create_board()
        filepath = f"puzzles/{puzzle}.xlsx"
        workbook = load_workbook(filepath, data_only=True)
        data = []
        pawn_counter = 0
        knight_counter = 9
        bishop_counter = 11
        rook_counter = 14
        queen_counter = 16
        i=0
        for row in workbook.active.iter_rows(values_only=True):
            if i != 0:
                data.append(row)
            i+=1
        for row in data:
            piece, color, row, col, first_move = row
            self.hexboard[row][col].piece = class_mapping[piece](color)
            if piece == 'Pawn':
                if first_move == 'True':
                    self.hexboard[row][col].piece.has_moved = False
                    self.hexboard[row][col].piece.index = pawn_counter
                    pawn_counter += 1
                else:
                    self.hexboard[row][col].piece.has_moved = True
                    self.hexboard[row][col].piece.index = pawn_counter
                    pawn_counter += 1
            elif piece == 'Knight':
                self.hexboard[row][col].piece.index = knight_counter
                knight_counter += 1
            elif piece == 'Bishop':
                self.hexboard[row][col].piece.index = bishop_counter
                bishop_counter += 1
            elif piece == 'Rook':
                self.hexboard[row][col].piece.index = rook_counter
                rook_counter += 1
            elif piece == 'Queen':
                self.hexboard[row][col].piece.index = queen_counter
                queen_counter += 1

    def action_to_tuple(self, output):
        piece = output // 91
        hexagon = output % 91
        return (piece, POSITIONS[hexagon])
    
    def index_to_piece(self, index):
        locations = self.get_pieces_locations('white') 
        for location in locations:
            row, col = location
            piece = self.get_piece(row, col)
            if piece != None:
                if piece.index == index:
                    return piece
    
    def legal_moves_to_actions(self, legal_moves):
        actions = []
        for move in legal_moves:
            index = move.piece.index
            target = move.target
            actions.append((index, target))
        return actions
    
    def action_to_move(self, action):
        index, target = action
        locations = self.get_pieces_locations("white") 

        for location in locations:
            row, col = location
            piece = self.get_piece(row, col)
            if piece != None:
                if piece.index == index:
                    return Move(piece, location, target)
                
    def random_black_move(self):
        legal_moves = self.get_legal_moves("black")
        move = random.choice(legal_moves)
        return move