<template>
  <div id="app">
    <chess-board
      :board="board"
      :currentPlayer="currentPlayer"
      :validMoves="validMoves"
      :moveHistory="moveHistory"
      :gameOver="gameOver"
      :winner="winner"
      @place-piece="handlePlacePiece"
      @make-move="handleMakeMove"
      @restart-game="restartGame"
      @next-player="nextPlayer"
    />
  </div>
</template>

<script>
import ChessBoard from './components/ChessBoard.vue';
import io from 'socket.io-client';

export default {
  name: 'App',
  components: {
    ChessBoard
  },
  data() {
    return {
      board: [
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
      ],
      currentPlayer: 'Player A',
      selectedPiece: '',
      selectedCell: { row: null, col: null },
      validMoves: [],
      moveHistory: [],
      socket: null,
      gameOver: false,
      winner: '',
      gameStarted: false
    };
  },
  created() {
    this.socket = io('http://localhost:5000');
    this.socket.on('game_state', (data) => {
      this.board = data.board;
      this.currentPlayer = data.current_player;
      this.validMoves = data.valid_moves;
      this.moveHistory = data.move_history;
      this.gameOver = data.game_over;
      this.winner = data.winner;
      this.gameStarted = data.game_started;
    });
    this.socket.on('invalid-move', (data) => {
      alert(data.message);
    });
    this.socket.on('game_over', (data) => {
      this.gameOver = true;
      this.winner = data.winner;
    });
  },
  methods: {
    selectPiece(piece) {
      this.selectedPiece = piece;
    },
    handlePlacePiece({ row, col }) {
      if (!this.gameStarted && this.selectedPiece) {
        this.placePiece(row, col);
      }
    },
    handleMakeMove({ from, to }) {
      if (this.gameStarted) {
        this.socket.emit('make_move', { from, to });
      }
    },
    placePiece(row, col) {
      if (this.board[row][col] === '' && this.selectedPiece) {
        const newBoard = this.board.map(r => r.slice());
        newBoard[row][col] = `${this.currentPlayer[0]}-${this.selectedPiece}`;
        this.board = newBoard;
        this.selectedPiece = '';
        this.socket.emit('initialize_game', { board: this.board });
      } else {
        alert('Cell already occupied!');
      }
    },
    restartGame() {
      this.socket.emit('restart_game');
      this.resetGame();
    },
    nextPlayer() {
      this.currentPlayer = this.currentPlayer === 'Player A' ? 'Player B' : 'Player A';
      this.socket.emit('next_player');
    },
    resetGame() {
      this.board = [
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
        ['', '', '', '', ''],
      ];
      this.currentPlayer = 'Player A';
      this.validMoves = [];
      this.moveHistory = [];
      this.gameOver = false;
      this.winner = '';
      this.gameStarted = false;
    }
  }
};
</script>
