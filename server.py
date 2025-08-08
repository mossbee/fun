import http.server
import socketserver
import json
import threading
import time
import os
from urllib.parse import urlparse, parse_qs
import base64

class GomokuGame:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.move_history = []
        
    def make_move(self, row, col, player):
        """Make a move on the board"""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            self.move_history.append((row, col, player))
            
            if self.check_win(row, col, player):
                self.game_over = True
                self.winner = player
            elif self.is_board_full():
                self.game_over = True
                self.winner = 'Tie'
            else:
                self.current_player = 'O' if player == 'X' else 'X'
            return True
        return False
    
    def is_valid_move(self, row, col):
        """Check if a move is valid"""
        return (0 <= row < self.board_size and 
                0 <= col < self.board_size and 
                self.board[row][col] == ' ')
    
    def check_win(self, row, col, player):
        """Check if the last move resulted in a win"""
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        
        for dr, dc in directions:
            count = 1
            
            # Check in positive direction
            r, c = row + dr, col + dc
            while (0 <= r < self.board_size and 
                   0 <= c < self.board_size and 
                   self.board[r][c] == player):
                count += 1
                r += dr
                c += dc
            
            # Check in negative direction
            r, c = row - dr, col - dc
            while (0 <= r < self.board_size and 
                   0 <= c < self.board_size and 
                   self.board[r][c] == player):
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        return False
    
    def is_board_full(self):
        """Check if the board is full"""
        return all(self.board[i][j] != ' ' 
                  for i in range(self.board_size) 
                  for j in range(self.board_size))
    
    def get_game_state(self):
        """Get current game state as dictionary"""
        return {
            'board': self.board,
            'currentPlayer': self.current_player,
            'gameOver': self.game_over,
            'winner': self.winner,
            'moveHistory': self.move_history
        }
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.move_history = []

class GameServer:
    def __init__(self, port=8080):
        self.port = port
        self.game = GomokuGame()
        self.bots = {'X': None, 'O': None}
        self.game_thread = None
        self.running = False
        
    def set_bot(self, player, bot_code):
        """Set bot code for a player"""
        self.bots[player] = bot_code
        
    def start_game(self):
        """Start the game if both bots are ready"""
        if self.bots['X'] and self.bots['O']:
            self.game.reset_game()
            self.running = True
            self.game_thread = threading.Thread(target=self.run_game)
            self.game_thread.daemon = True
            self.game_thread.start()
            return True
        return False
    
    def run_game(self):
        """Run the game loop"""
        while self.running and not self.game.game_over:
            current_player = self.game.current_player
            bot_code = self.bots[current_player]
            
            if bot_code:
                try:
                    # Execute bot code to get move
                    move = self.execute_bot(bot_code, self.game.get_game_state())
                    if move and self.game.make_move(move['row'], move['col'], current_player):
                        print(f"Player {current_player} moved to ({move['row']}, {move['col']})")
                        self.display_board()
                    else:
                        print(f"Invalid move by player {current_player}")
                        # Make a random valid move as fallback
                        self.make_random_move(current_player)
                except Exception as e:
                    print(f"Bot error for player {current_player}: {e}")
                    # Make a random valid move as fallback
                    self.make_random_move(current_player)
            
            time.sleep(1)  # Delay between moves
        
        if self.game.game_over:
            print(f"Game over! Winner: {self.game.winner}")
    
    def execute_bot(self, bot_code, game_state):
        """Execute bot code and return move"""
        # Create a safe execution environment
        namespace = {
            'gameState': game_state,
            'board': game_state['board'],
            'currentPlayer': game_state['currentPlayer'],
            'gameOver': game_state['gameOver'],
            'winner': game_state['winner']
        }
        
        try:
            # Execute the bot code
            exec(bot_code, namespace)
            
            # The bot should set a 'move' variable
            if 'move' in namespace:
                return namespace['move']
        except Exception as e:
            print(f"Bot execution error: {e}")
        
        return None
    
    def make_random_move(self, player):
        """Make a random valid move as fallback"""
        import random
        valid_moves = []
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.is_valid_move(i, j):
                    valid_moves.append((i, j))
        
        if valid_moves:
            row, col = random.choice(valid_moves)
            self.game.make_move(row, col, player)
            print(f"Random move for player {player}: ({row}, {col})")
    
    def display_board(self):
        """Display the current board"""
        print("\n" + "="*50)
        print("Current Board:")
        print("  " + " ".join(str(i) for i in range(self.game.board_size)))
        for i, row in enumerate(self.game.board):
            print(f"{i:2d} {' '.join(cell if cell != ' ' else '.' for cell in row)}")
        print(f"Current player: {self.game.current_player}")
        if self.game.game_over:
            print(f"Game over! Winner: {self.game.winner}")
        print("="*50)

class GameHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, game_server=None, **kwargs):
        self.game_server = game_server
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_index_html().encode())
        elif parsed_path.path == '/api/game-state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = self.game_server.game.get_game_state()
            self.wfile.write(json.dumps(response).encode())
        elif parsed_path.path == '/api/bots':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'X': self.game_server.bots['X'],
                'O': self.game_server.bots['O']
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/set-bot':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            player = data.get('player')
            bot_code = data.get('code')
            
            if player in ['X', 'O'] and bot_code:
                self.game_server.set_bot(player, bot_code)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid player or code'}).encode())
        
        elif parsed_path.path == '/api/start-game':
            success = self.game_server.start_game()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success' if success else 'error'}).encode())
        
        elif parsed_path.path == '/api/reset-game':
            self.game_server.game.reset_game()
            self.game_server.running = False
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())
    
    def get_index_html(self):
        """Return the main HTML page"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gomoku Bot Battle</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .panel {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .board {
            display: grid;
            grid-template-columns: repeat(15, 30px);
            gap: 1px;
            background: #333;
            padding: 10px;
            border-radius: 8px;
        }
        .cell {
            width: 30px;
            height: 30px;
            background: #f9f9f9;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            cursor: pointer;
        }
        .cell.X { color: #e74c3c; }
        .cell.O { color: #3498db; }
        .controls {
            margin-top: 20px;
            display: flex;
            gap: 10px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .btn-primary { background: #3498db; color: white; }
        .btn-success { background: #27ae60; color: white; }
        .btn-warning { background: #f39c12; color: white; }
        .btn-danger { background: #e74c3c; color: white; }
        textarea {
            width: 100%;
            height: 300px;
            font-family: monospace;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            resize: vertical;
        }
        .status {
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .status.waiting { background: #fff3cd; color: #856404; }
        .status.playing { background: #d1ecf1; color: #0c5460; }
        .status.finished { background: #d4edda; color: #155724; }
        .protocol-docs {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
        }
        .protocol-docs h3 {
            margin-top: 0;
        }
        .protocol-docs code {
            background: #e9ecef;
            padding: 2px 4px;
            border-radius: 2px;
        }
    </style>
</head>
<body>
    <h1>🎮 Gomoku Bot Battle</h1>
    
    <div class="container">
        <div class="panel">
            <h2>Game Board</h2>
            <div id="board" class="board"></div>
            <div id="status" class="status waiting">Waiting for bots...</div>
            <div class="controls">
                <button class="btn-primary" onclick="startGame()">Start Game</button>
                <button class="btn-warning" onclick="resetGame()">Reset Game</button>
                <button class="btn-success" onclick="refreshBoard()">Refresh</button>
            </div>
        </div>
        
        <div class="panel">
            <h2>Bot Editor</h2>
            <div>
                <label>Player X Bot:</label>
                <textarea id="botX" placeholder="Enter bot code for player X...">// Example bot code for player X
// Available variables: gameState, board, currentPlayer, gameOver, winner
// Set the 'move' variable with your move: {row: 7, col: 8}

// Simple random bot
const validMoves = [];
for (let i = 0; i < 15; i++) {
    for (let j = 0; j < 15; j++) {
        if (board[i][j] === ' ') {
            validMoves.push({row: i, col: j});
        }
    }
}

if (validMoves.length > 0) {
    const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)];
    move = randomMove;
}</textarea>
            </div>
            <div style="margin-top: 10px;">
                <label>Player O Bot:</label>
                <textarea id="botO" placeholder="Enter bot code for player O...">// Example bot code for player O
// Available variables: gameState, board, currentPlayer, gameOver, winner
// Set the 'move' variable with your move: {row: 7, col: 8}

// Simple random bot
const validMoves = [];
for (let i = 0; i < 15; i++) {
    for (let j = 0; j < 15; j++) {
        if (board[i][j] === ' ') {
            validMoves.push({row: i, col: j});
        }
    }
}

if (validMoves.length > 0) {
    const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)];
    move = randomMove;
}</textarea>
            </div>
            <div class="controls">
                <button class="btn-primary" onclick="saveBots()">Save Bots</button>
                <button class="btn-success" onclick="loadBots()">Load Bots</button>
            </div>
        </div>
    </div>
    
    <div class="protocol-docs">
        <h3>🤖 Bot Protocol Documentation</h3>
        <p><strong>Your bot code will receive these variables:</strong></p>
        <ul>
            <li><code>gameState</code> - Complete game state object</li>
            <li><code>board</code> - 15x15 array representing the board ('X', 'O', or ' ')</li>
            <li><code>currentPlayer</code> - 'X' or 'O' (your player)</li>
            <li><code>gameOver</code> - true/false</li>
            <li><code>winner</code> - 'X', 'O', 'Tie', or null</li>
        </ul>
        
        <p><strong>Your bot must set the <code>move</code> variable:</strong></p>
        <pre><code>move = {row: 7, col: 8};  // row and col must be 0-14</code></pre>
        
        <p><strong>Example bot strategies:</strong></p>
        <ul>
            <li><strong>Random:</strong> Pick any empty cell</li>
            <li><strong>Center:</strong> Always play in the center</li>
            <li><strong>Win First:</strong> Check for winning moves, then blocking moves</li>
            <li><strong>Pattern:</strong> Look for patterns and create lines</li>
        </ul>
        
        <p><strong>Board coordinates:</strong> (0,0) is top-left, (14,14) is bottom-right</p>
    </div>

    <script>
        let gameInterval;
        
        async function startGame() {
            const response = await fetch('/api/start-game', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            });
            const result = await response.json();
            if (result.status === 'success') {
                updateStatus('Game started!', 'playing');
                startGameLoop();
            } else {
                alert('Please save both bots first!');
            }
        }
        
        async function resetGame() {
            await fetch('/api/reset-game', {method: 'POST'});
            updateStatus('Game reset', 'waiting');
            stopGameLoop();
            refreshBoard();
        }
        
        async function saveBots() {
            const botX = document.getElementById('botX').value;
            const botO = document.getElementById('botO').value;
            
            await fetch('/api/set-bot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({player: 'X', code: botX})
            });
            
            await fetch('/api/set-bot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({player: 'O', code: botO})
            });
            
            alert('Bots saved!');
        }
        
        async function loadBots() {
            const response = await fetch('/api/bots');
            const bots = await response.json();
            
            document.getElementById('botX').value = bots.X || '';
            document.getElementById('botO').value = bots.O || '';
        }
        
        async function refreshBoard() {
            const response = await fetch('/api/game-state');
            const gameState = await response.json();
            displayBoard(gameState.board);
            updateGameStatus(gameState);
        }
        
        function displayBoard(board) {
            const boardElement = document.getElementById('board');
            boardElement.innerHTML = '';
            
            for (let i = 0; i < 15; i++) {
                for (let j = 0; j < 15; j++) {
                    const cell = document.createElement('div');
                    cell.className = 'cell';
                    cell.textContent = board[i][j];
                    if (board[i][j] === 'X') cell.classList.add('X');
                    if (board[i][j] === 'O') cell.classList.add('O');
                    boardElement.appendChild(cell);
                }
            }
        }
        
        function updateGameStatus(gameState) {
            let statusText = '';
            let statusClass = 'waiting';
            
            if (gameState.gameOver) {
                statusText = `Game Over! Winner: ${gameState.winner}`;
                statusClass = 'finished';
            } else {
                statusText = `Current Player: ${gameState.currentPlayer}`;
                statusClass = 'playing';
            }
            
            updateStatus(statusText, statusClass);
        }
        
        function updateStatus(text, className) {
            const status = document.getElementById('status');
            status.textContent = text;
            status.className = `status ${className}`;
        }
        
        function startGameLoop() {
            gameInterval = setInterval(refreshBoard, 1000);
        }
        
        function stopGameLoop() {
            if (gameInterval) {
                clearInterval(gameInterval);
                gameInterval = null;
            }
        }
        
        // Load initial state
        loadBots();
        refreshBoard();
    </script>
</body>
</html>
        '''

def run_server(port=8080):
    """Run the game server"""
    game_server = GameServer(port)
    
    # Create custom handler with game server
    handler = type('GameHandler', (GameHTTPRequestHandler,), {
        'game_server': game_server
    })
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🎮 Gomoku Bot Battle Server running on http://localhost:{port}")
        print("📱 Other computers can access via: http://YOUR_IP_ADDRESS:8080")
        print("🤖 Teams can create bots by visiting the URL in their browser")
        print("⏹️  Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    run_server() 