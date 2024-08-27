class Game:
    def __init__(self):
        self.board = [['' for _ in range(5)] for _ in range(5)]
        self.current_player = 'A'
        self.players = {'A': [], 'B': []}

    def initialize_game(self):
        self.board = [['' for _ in range(5)] for _ in range(5)]
        self.current_player = 'A'
        self.players = {'A': [], 'B': []}
    
    def validate_move(self, player, from_x, from_y, to_x, to_y):
        if not (0 <= from_x < 5 and 0 <= from_y < 5 and 0 <= to_x < 5 and 0 <= to_y < 5):
            return False

        if self.board[from_y][from_x] == '' or self.board[from_y][from_x][0] != player:
            return False

        if self.board[to_y][to_x] != '' and self.board[to_y][to_x][0] == player:
            return False

        piece_type = self.board[from_y][from_x][2:]
        if piece_type == 'P':
            if (abs(to_x - from_x) == 1 and to_y - from_y == 1) or (to_x == from_x and to_y - from_y == 1):
                return True
        elif piece_type == 'H1':
            if (abs(to_x - from_x) == 2 and to_y == from_y) or (abs(to_y - from_y) == 2 and to_x == from_x):
                return True
        elif piece_type == 'H2':
            if abs(to_x - from_x) == 2 and abs(to_y - from_y) == 2:
                return True

        return False

    def move_piece(self, player, from_x, from_y, to_x, to_y):
        piece = self.board[from_y][from_x]
        self.board[to_y][to_x] = piece
        self.board[from_y][from_x] = ''

    def check_game_over(self):
        has_pieces = {'A': any(piece.startswith('A-') for row in self.board for piece in row),
                      'B': any(piece.startswith('B-') for row in self.board for piece in row)}

        if not has_pieces['A']:
            return 'B'
        elif not has_pieces['B']:
            return 'A'
        return None

    def setup_pieces(self, player_a_setup, player_b_setup):
        # Place player A's pieces on the board
        for idx, piece in enumerate(player_a_setup):
            if 0 <= idx < 5:
                x = idx
                y = 0
                self.board[y][x] = 'A-' + piece

        # Place player B's pieces on the board
        for idx, piece in enumerate(player_b_setup):
            if 0 <= idx < 5:
                x = idx
                y = 4
                self.board[y][x] = 'B-' + piece

        self.players['A'] = player_a_setup
        self.players['B'] = player_b_setup
