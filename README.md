# 🎮 Gomoku Bot Battle

A Gomoku (Five in a Row) game where teams create bots to battle against each other! Supports both web-based JavaScript bots and standalone client programs in Python, C, and C++.

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

#### Option 1: Web-Based (Easiest)
1. **Open a web browser**
2. **Visit the URL provided by the host**
3. **Create your bot using JavaScript!**

#### Option 2: Client Programs (Advanced)
Choose your preferred programming language:

**Python Client:**
```bash
# Install requests library (if needed)
pip install requests

# Run the bot
python3 client_python.py <server_ip>
```

**C Client:**
```bash
# Compile the bot
gcc -o client_c client_c.c

# Run the bot
./client_c <server_ip>
```

**C++ Client:**
```bash
# Compile the bot
g++ -o client_cpp client_cpp.cpp

# Run the bot
./client_cpp <server_ip>
```

## 🤖 How to Create a Bot

### Web-Based Bots (JavaScript)

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

### Client Program Bots (Python/C/C++)

For client programs, implement your bot logic in the `get_move()` function:

**Python:**
```python
def get_move(self, board, current_player):
    """
    IMPLEMENT YOUR BOT LOGIC HERE!
    
    Parameters:
    - board: 15x15 list of lists representing the game board
    - current_player: 'X' or 'O' (your player)
    
    Returns:
    - tuple (row, col) with your move (0-14 for both row and col)
    """
    
    # Your strategy here
    import random
    
    valid_moves = []
    for i in range(15):
        for j in range(15):
            if board[i][j] == ' ':
                valid_moves.append((i, j))
    
    if valid_moves:
        return random.choice(valid_moves)
    
    return (7, 7)  # Fallback
```

**C:**
```c
Move get_move(char board[BOARD_SIZE][BOARD_SIZE], char current_player) {
    /*
     * IMPLEMENT YOUR BOT LOGIC HERE!
     * 
     * Parameters:
     * - board: 15x15 array representing the game board
     * - current_player: 'X' or 'O' (your player)
     * 
     * Returns:
     * - Move with row and col (0-14 for both)
     */
    
    Move move;
    
    // Your strategy here
    // Find valid moves and pick one
    
    return move;
}
```

**C++:**
```cpp
Move get_move(const std::vector<std::vector<char>>& board, char current_player) {
    /*
     * IMPLEMENT YOUR BOT LOGIC HERE!
     * 
     * Parameters:
     * - board: 15x15 vector representing the game board
     * - current_player: 'X' or 'O' (your player)
     * 
     * Returns:
     * - Move with row and col (0-14 for both)
     */
    
    // Your strategy here
    // Find valid moves and pick one
    
    return {7, 7};  // Fallback
}
```

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
- Try a different port if 8080 is already in use: `python3 -c "from server import run_server; run_server(8081)"`

### Bot not working?
- Make sure your bot sets the `move` variable (JavaScript) or returns a move (Python/C/C++)
- Check that row and col are between 0 and 14
- Verify the move is on an empty cell

### Game not starting?
- Make sure both Player X and Player O bots are saved
- Check that the bot code is valid JavaScript

### Client program errors?
- **Python client**: Make sure you have `requests` library: `pip install requests`
- **C/C++ clients**: Make sure you have a compiler installed: `sudo apt install gcc g++`
- **Connection errors**: Check that the server IP is correct (don't include `http://`)

### Server errors?
- If you see "Address already in use", try a different port
- If the server crashes, check the console for error messages
- Make sure you're using Python 3.x

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
- `POST /api/move` - Make a move (for client programs)

## 🎯 Web-Based vs Client Programs

### Web-Based Approach (Recommended for Beginners)
- **Pros:** No installation, immediate testing, visual feedback
- **Cons:** Limited to JavaScript, no external libraries
- **Best for:** Quick prototyping, beginners, teams new to programming

### Client Programs (Recommended for Advanced Teams)
- **Pros:** Use your preferred language, external libraries, better debugging
- **Cons:** Requires compilation/installation, more setup
- **Best for:** Complex algorithms, teams with programming experience

### Which to Choose?
- **Start with web-based** if you're new to programming
- **Use client programs** if you want to use Python/C/C++ or need advanced features
- **Both work together** - you can have web bots vs client bots!

## 🎉 Have Fun!

This is designed to be educational and fun. Experiment with different strategies, learn from other teams, and enjoy the competition!

---

**Requirements:** 
- **Server:** Python 3.x (no additional packages needed)
- **Python Client:** `pip install requests`
- **C/C++ Clients:** Standard compiler (gcc/g++)
- **Network:** Local network connection
- **Browsers:** Any modern web browser 