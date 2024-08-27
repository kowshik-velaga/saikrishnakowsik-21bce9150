<template>
  <div class="layout-container">
    <!-- Chess Board and Side Panel -->
    <div class="chess-board-wrapper">
      <!-- Display Current Player -->
      <div class="current-player">
        <h2>Current Player: {{ currentPlayer }}</h2>
      </div>

      <!-- Piece Selection -->
      <div class="piece-selection" v-if="!gameStarted">
        <button @click="selectPiece('P1')">Select P1</button>
        <button @click="selectPiece('P2')">Select P2</button>
        <button @click="selectPiece('P3')">Select P3</button>
        <button @click="selectPiece('H1')">Select H1</button>
        <button @click="selectPiece('H2')">Select H2</button>
      </div>

      <!-- Game Board -->
      <div class="chess-board">
        <div
          v-for="(row, rowIndex) in board"
          :key="'row-' + rowIndex"
          class="row"
        >
          <div
            v-for="(cell, colIndex) in row"
            :key="'cell-' + colIndex"
            :class="['cell', getCellClass(rowIndex, colIndex), getPieceClass(cell)]"
            @click="handleClick(rowIndex, colIndex)"
          >
            {{ getPieceLabel(cell) }}
          </div>
        </div>
      </div>

      <!-- Move History -->
      <div class="move-history">
        <h3>Move History</h3>
        <ul>
          <li v-for="(move, index) in moveHistory" :key="index">{{ move }}</li>
        </ul>
      </div>

      <!-- Game Over Screen -->
      <div v-if="gameOver" class="game-over">
        <h2>Game Over!</h2>
        <p>Winner: {{ winner }}</p>
        <button @click="restartGame">Start New Game</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    board: Array,
    currentPlayer: String,
    validMoves: Array,
    moveHistory: Array,
    gameOver: Boolean,
    winner: String,
  },
  data() {
    return {
      selectedPiece: "",
      selectedCell: { row: null, col: null },
      gameStarted: false,
      placedPieces: 0,
    };
  },
  methods: {
    selectPiece(piece) {
      this.selectedPiece = piece;
    },
    handleClick(row, col) {
      if (!this.gameStarted) {
        if (
          (this.currentPlayer === "Player A" && row === 0) ||
          (this.currentPlayer === "Player B" && row === 4)
        ) {
          if (this.board[row][col] === "" && this.selectedPiece) {
            this.$emit("place-piece", {
              row,
              col,
              piece: `${this.currentPlayer[0]}-${this.selectedPiece}`,
            });
            this.selectedPiece = "";
            this.placedPieces++;

            if (this.placedPieces === 5) {
              this.gameStarted = true;
              this.$emit("next-player");
            }
          } else {
            alert("Cell already occupied or no piece selected!");
          }
        }
      } else {
        if (
          this.selectedCell.row !== null &&
          this.validMoves.some((move) => move.row === row && move.col === col)
        ) {
          this.$emit("make-move", {
            from: this.selectedCell,
            to: { row, col },
          });
          this.selectedCell = { row, col };
        } else {
          this.selectedCell = { row, col };
        }
      }
    },
    getCellClass(row, col) {
      return this.selectedCell.row === row && this.selectedCell.col === col ? "selected" : "";
    },
    getPieceClass(cell) {
      if (cell.startsWith('A-')) return 'piece-a';
      if (cell.startsWith('B-')) return 'piece-b';
      return '';
    },
    getPieceLabel(cell) {
      return cell ? cell : '';
    },
    restartGame() {
      this.$emit("restart-game");
    },
  },
};
</script>

<style scoped>
/* Center the chessboard and place the move history at the bottom */
.layout-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.chess-board-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.current-player {
  margin-bottom: 20px;
}

.piece-selection {
  margin-bottom: 20px;
}

.chess-board {
  display: grid;
  grid-template-columns: repeat(5, 50px);
  grid-gap: 1px;
  margin-bottom: 20px;
}

.row {
  display: contents;
}

.cell {
  width: 50px;
  height: 50px;
  background-color: lightgray;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
}

.cell.selected {
  border: 2px solid red;
}

.piece-a {
  color: silver; /* Different color for Player A pieces */
}

.piece-b {
  color: red; /* Different color for Player B pieces */
}

/* Move history at the bottom of the board */
.move-history {
  margin-top: 20px;
}

.move-history ul {
  list-style-type: none;
  padding: 0;
}

.game-over {
  color: red;
  font-weight: bold;
}
</style>
