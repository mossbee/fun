import http.server
import socketserver
import json
import threading
import time
import os
from urllib.parse import urlparse, parse_qs
import socket
import requests

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
        self.connected_bots = {'X': None, 'O': None}  # Store bot info
        self.game_thread = None
        self.running = False
        
    def register_bot(self, player, bot_info):
        """Register a bot for a player"""
        if player in ['X', 'O']:
            self.connected_bots[player] = bot_info
            print(f"🤖 Bot registered for player {player}: {bot_info}")
            return True
        return False
    
    def unregister_bot(self, player):
        """Unregister a bot"""
        if player in ['X', 'O']:
            self.connected_bots[player] = None
            print(f"🤖 Bot unregistered for player {player}")
    
    def start_game(self):
        """Start the game if both bots are connected"""
        if self.connected_bots['X'] and self.connected_bots['O']:
            self.game.reset_game()
            self.running = True
            self.game_thread = threading.Thread(target=self.run_game)
            self.game_thread.daemon = True
            self.game_thread.start()
            print("🎮 Game started! Bots are playing...")
            return True
        else:
            print("❌ Need both bots connected to start game")
            return False
    
    def stop_game(self):
        """Stop the game"""
        self.running = False
        if self.game_thread:
            self.game_thread.join(timeout=1)
    
    def run_game(self):
        """Run the game loop - get moves from connected bots"""
        while self.running and not self.game.game_over:
            current_player = self.game.current_player
            bot_info = self.connected_bots[current_player]
            
            if bot_info:
                try:
                    # Get move from bot via HTTP API
                    move = self.get_bot_move(bot_info, self.game.get_game_state())
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
            print(f"🏁 Game over! Winner: {self.game.winner}")
    
    def get_bot_move(self, bot_info, game_state):
        """Get move from a connected bot"""
        try:
            # Send game state to bot and get move back
            response = requests.post(
                f"http://{bot_info['host']}:{bot_info['port']}/get_move",
                json=game_state,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting move from bot: {e}")
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
            # Serve the main HTML file
            try:
                with open('static/index.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, "File not found")
        elif parsed_path.path.startswith('/static/'):
            # Serve static files
            file_path = parsed_path.path[1:]  # Remove leading slash
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # Determine content type based on file extension
                if file_path.endswith('.css'):
                    content_type = 'text/css'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript'
                else:
                    content_type = 'text/plain'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, "File not found")
        elif parsed_path.path == '/api/game-state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = self.game_server.game.get_game_state()
            self.wfile.write(json.dumps(response).encode())
        elif parsed_path.path == '/api/connected-bots':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'X': self.game_server.connected_bots['X'],
                'O': self.game_server.connected_bots['O']
            }
            self.wfile.write(json.dumps(response).encode())
        elif parsed_path.path == '/api/game-status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'isRunning': self.game_server.running,
                'hasBots': bool(self.game_server.connected_bots['X'] and self.game_server.connected_bots['O'])
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/register-bot':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            player = data.get('player')
            bot_info = data.get('bot_info')
            
            if player in ['X', 'O'] and bot_info:
                success = self.game_server.register_bot(player, bot_info)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success' if success else 'error'}).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid player or bot info'}).encode())
        
        elif parsed_path.path == '/api/start-game':
            success = self.game_server.start_game()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success' if success else 'error'}).encode())
        
        elif parsed_path.path == '/api/reset-game':
            self.game_server.game.reset_game()
            self.game_server.stop_game()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())

def run_server(port=8080):
    """Run the game server"""
    game_server = GameServer(port)
    
    # Create custom handler class that passes game_server to each instance
    class GameHandler(GameHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, game_server=game_server, **kwargs)
    
    with socketserver.TCPServer(("", port), GameHandler) as httpd:
        print(f"🎮 Gomoku Bot Battle Server running on http://localhost:{port}")
        print("📱 Other computers can access via: http://YOUR_IP_ADDRESS:8080")
        print("🤖 Bots should connect via HTTP API")
        print("⏹️  Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    run_server() 