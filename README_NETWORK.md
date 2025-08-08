# 🎮 Gomoku Bot Battle - Network Edition

A clean Gomoku (Five in a Row) game server where bots connect via network and compete automatically.

## 🏗️ Architecture

- **Server** (`server.py`) - Manages the game and serves web interface
- **Bots** (`client_python.py`) - Connect via HTTP API to provide moves
- **Web Interface** - Shows game progress and bot connection status

## 🚀 Quick Start

### 1. Start the Server

```bash
python server.py
```

The server will start on `http://localhost:8080`

### 2. Connect Bots

On different machines (or different terminals), run:

```bash
# Bot for Player X
python client_python.py SERVER_IP X 8081

# Bot for Player O  
python client_python.py SERVER_IP O 8082
```

**Example:**
```bash
# If server is on 192.168.1.100
python client_python.py 192.168.1.100 X 8081
python client_python.py 192.168.1.100 O 8082
```

### 3. Start the Game

1. Open `http://localhost:8080` in your browser
2. Wait for both bots to connect (green status)
3. Click "Start Game" button
4. Watch the bots compete!

## 📋 Requirements

### Server
- Python 3.6+
- `requests` library

### Bot Client
- Python 3.6+
- `requests` library only (uses standard Python HTTP server)

Install bot dependencies:
```bash
pip install requests
```

## 🤖 Bot Development

Edit the `get_move()` function in `client_python.py`:

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
    
    # Your strategy here!
    # Example: Random bot
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

## 🌐 Network Setup

### Same Network
- All machines must be on the same local network
- Use the server's local IP address (e.g., `192.168.1.100`)
- Each bot needs a unique port

### Port Configuration
- Server: `8080` (default)
- Bot X: `8081` (default)
- Bot O: `8082` (default)

## 📡 API Protocol

### Bot Registration
```
POST /api/register-bot
{
  "player": "X" or "O",
  "bot_info": {
    "host": "192.168.1.101",
    "port": 8081,
    "name": "My Bot"
  }
}
```

### Bot Move Request
```
POST http://BOT_HOST:BOT_PORT/get_move
{
  "board": [15x15 array],
  "currentPlayer": "X" or "O",
  "gameOver": true/false,
  "winner": "X", "O", "Tie", or null
}
```

### Bot Move Response
```
{
  "row": 7,
  "col": 8
}
```

## 🎯 Game Rules

- 15x15 board
- First player to get 5 in a row wins
- Can be horizontal, vertical, or diagonal
- If board fills up, it's a tie

## 🔧 Troubleshooting

### Bot Connection Issues
1. Check if bots are on the same network as server
2. Verify server IP address is correct
3. Ensure each bot uses a unique port
4. Check firewall settings

### Game Not Starting
1. Make sure both bots show "Connected" status
2. Check server console for error messages
3. Verify bot HTTP servers are running

### Move Errors
1. Ensure bot returns valid coordinates (0-14)
2. Check that move position is empty
3. Verify bot response format

## 📁 File Structure

```
fun/
├── server.py              # Main game server
├── client_python.py       # Bot client template
├── requirements.txt       # Bot dependencies
├── static/
│   ├── index.html        # Web interface
│   ├── style.css         # Styles
│   └── script.js         # Client-side logic
└── README_NETWORK.md     # This file
```

## 🎮 Example Game Flow

1. **Start Server**: `python server.py`
2. **Connect Bot X**: `python client_python.py 192.168.1.100 X 8081`
3. **Connect Bot O**: `python client_python.py 192.168.1.100 O 8082`
4. **Open Browser**: `http://localhost:8080`
5. **Start Game**: Click "Start Game" when both bots connected
6. **Watch**: Bots play automatically!

The web interface shows real-time game progress and bot connection status. 