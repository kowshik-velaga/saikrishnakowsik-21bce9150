from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")
CORS(app)

# Initial game state
board = [['' for _ in range(5)] for _ in range(5)]
current_player = 'A'
players = {'A': [], 'B': []}

def initialize_game():
    global board, current_player, players
    board = [['' for _ in range(5)] for _ in range(5)]
    current_player = 'A'
    players = {'A': [], 'B': []}
    emit('game_state', {'board': board, 'current_player': current_player, 'players': players}, broadcast=True)

def validate_move(board, player, from_x, from_y, to_x, to_y):
    if not (0 <= from_x < 5 and 0 <= from_y < 5 and 0 <= to_x < 5 and 0 <= to_y < 5):
        return False

    if board[from_y][from_x] == '' or board[from_y][from_x][0] != player:
        return False

    if board[to_y][to_x] != '' and board[to_y][to_x][0] == player:
        return False

    piece_type = board[from_y][from_x][2:]
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

def move_piece(board, player, from_x, from_y, to_x, to_y):
    piece = board[from_y][from_x]
    board[to_y][to_x] = piece
    board[from_y][from_x] = ''

def check_game_over():
    has_pieces = {'A': any(piece.startswith('A-') for row in board for piece in row),
                  'B': any(piece.startswith('B-') for row in board for piece in row)}

    if not has_pieces['A']:
        emit('game_over', {'winner': 'B'}, broadcast=True)
    elif not has_pieces['B']:
        emit('game_over', {'winner': 'A'}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    emit('game_state', {'board': board, 'current_player': current_player, 'players': players})

@socketio.on('move')
def handle_move(data):
    global current_player
    from_x, from_y, to_x, to_y = data['fromX'], data['fromY'], data['toX'], data['toY']
    if validate_move(board, current_player, from_x, from_y, to_x, to_y):
        move_piece(board, current_player, from_x, from_y, to_x, to_y)
        current_player = 'B' if current_player == 'A' else 'A'
        emit('game_state', {'board': board, 'current_player': current_player, 'players': players}, broadcast=True)
        check_game_over()
    else:
        emit('invalid_move', {'message': 'Invalid move!'})

@socketio.on('initialize_game')
def handle_initialize_game(data):
    # Initialize game with deployment
    initialize_game()
    
    player_a_setup = data.get('playerA', [])
    player_b_setup = data.get('playerB', [])
    
    # Place player A's pieces on the board
    for idx, piece in enumerate(player_a_setup):
        if 0 <= idx < 5:
            x = idx
            y = 0
            board[y][x] = 'A-' + piece
    
    # Place player B's pieces on the board
    for idx, piece in enumerate(player_b_setup):
        if 0 <= idx < 5:
            x = idx
            y = 4
            board[y][x] = 'B-' + piece
    
    players['A'] = player_a_setup
    players['B'] = player_b_setup
    emit('game_state', {'board': board, 'current_player': current_player, 'players': players}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
