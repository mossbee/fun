# 🎮 Gomoku Bot Battle

A web-based Gomoku (Five in a Row) game where teams create JavaScript bots to battle against each other!

## 🚀 Quick Start

### For the Host (Your Computer)

1. **Start the server:**
   ```bash
   python server.py
   ```

2. **Find your IP address:**
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig` or `ip addr`

3. **Share the URL:**
   - Tell other teams to visit: `http://YOUR_IP_ADDRESS:8080`
   - Example: `http://192.168.1.100:8080`

### For Teams (Other Computers)

1. **Open a web browser**
2. **Visit the URL provided by the host**
3. **Create your bot!**

## 🤖 How to Create a Bot

### Basic Bot Structure

Your bot code should set a `move` variable with your chosen position:

```javascript
// Your bot code goes here
// Available variables: gameState, board, currentPlayer, gameOver, winner

// Example: Random bot
const validMoves = [];
for (let i = 0; i < 15; i++) {
    for (let j = 0; j < 15; j++) {
        if (board[i][j] === ' ') {
            validMoves.push({row: i, col: j});
        }
    }
}

if (validMoves.length > 0) {
    const randomIndex = Math.floor(Math.random() * validMoves.length);
    move = validMoves[randomIndex];
}
```

### Available Variables

- `gameState` - Complete game state object
- `board` - 15x15 array representing the board ('X', 'O', or ' ')
- `currentPlayer` - 'X' or 'O' (your player)
- `gameOver` - true/false
- `winner` - 'X', 'O', 'Tie', or null

### Making a Move

Set the `move` variable with your chosen position:

```javascript
move = {row: 7, col: 8};  // row and col must be 0-14
```

**Board coordinates:** (0,0) is top-left, (14,14) is bottom-right

## 🎯 Bot Strategies

### 1. Random Bot
```javascript
const validMoves = [];
for (let i = 0; i < 15; i++) {
    for (let j = 0; j < 15; j++) {
        if (board[i][j] === ' ') {
            validMoves.push({row: i, col: j});
        }
    }
}
if (validMoves.length > 0) {
    move = validMoves[Math.floor(Math.random() * validMoves.length)];
}
```

### 2. Center Bot
```javascript
if (board[7][7] === ' ') {
    move = {row: 7, col: 7};
} else {
    // fallback to random
}
```

### 3. Win-First Bot
```javascript
// First, try to find a winning move
const winningMove = findWinningMove(currentPlayer);
if (winningMove) {
    move = winningMove;
} else {
    // Second, try to block opponent's winning move
    const opponent = currentPlayer === 'X' ? 'O' : 'X';
    const blockingMove = findWinningMove(opponent);
    if (blockingMove) {
        move = blockingMove;
    } else {
        // Otherwise, play randomly
    }
}
```

## 🏆 Advanced Strategies

### Pattern Recognition
Look for opportunities to create lines of 4, 3, or 2 pieces.

### Defensive Play
Always check if your opponent can win on their next move and block them.

### Aggressive Play
Focus on creating multiple threats that your opponent can't block all at once.

### Position Evaluation
Consider the strategic value of different board positions (center, corners, edges).

## 📋 Game Rules

1. **Objective:** Get 5 pieces in a row (horizontal, vertical, or diagonal)
2. **Board:** 15x15 grid
3. **Players:** X goes first, then O
4. **Winning:** First to get 5 in a row wins
5. **Tie:** If board fills up without a winner

## 🎮 How to Play

1. **Host starts the server** (`python server.py`)
2. **Teams visit the URL** in their browsers
3. **Teams write bot code** in the text areas
4. **Host clicks "Save Bots"** to load the bots
5. **Host clicks "Start Game"** to begin the battle
6. **Watch the bots play!** The board updates in real-time

## 🔧 Troubleshooting

### Can't connect to the server?
- Make sure the host computer's firewall allows connections on port 8080
- Verify all computers are on the same local network
- Check that the IP address is correct

### Bot not working?
- Make sure your bot sets the `move` variable
- Check that row and col are between 0 and 14
- Verify the move is on an empty cell

### Game not starting?
- Make sure both Player X and Player O bots are saved
- Check that the bot code is valid JavaScript

## 📚 Example Bots

See `client_bot_examples.js` for complete bot implementations including:
- Random Bot
- Center Bot
- Win-First Bot
- Pattern Bot
- Edge Bot
- Corner Bot
- Aggressive Bot
- Defensive Bot

## 🎯 Tips for Teams

1. **Start simple** - Get a basic bot working first
2. **Test your logic** - Make sure your bot can find winning moves
3. **Think defensively** - Don't forget to block your opponent
4. **Look for patterns** - Try to create multiple threats
5. **Be creative** - Try unusual strategies!

## 🏆 Competition Ideas

- **Round Robin:** Each bot plays against every other bot
- **Tournament:** Single elimination bracket
- **Time Limit:** Bots must make moves within a time limit
- **Strategy Categories:** Best offensive bot, best defensive bot, most creative

## 🔄 API Endpoints

The server provides these endpoints:
- `GET /` - Main game interface
- `GET /api/game-state` - Current game state
- `GET /api/bots` - Current bot code
- `POST /api/set-bot` - Save bot code
- `POST /api/start-game` - Start the game
- `POST /api/reset-game` - Reset the game

## 🎉 Have Fun!

This is designed to be educational and fun. Experiment with different strategies, learn from other teams, and enjoy the competition!

---

**Requirements:** Only Python 3.x (no additional packages needed)
**Network:** Local network connection
**Browsers:** Any modern web browser 