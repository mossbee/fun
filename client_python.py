#!/usr/bin/env python3
"""
Gomoku Bot Client - Python Version
This bot connects to the server and provides an HTTP API for getting moves.
Uses only standard Python libraries - no Flask required.
"""

import socket
import json
import time
import sys
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

class BotHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests for getting moves"""
        if self.path == '/get_move':
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                game_state = json.loads(post_data.decode())
                
                # Get move from bot (access via server's bot_instance)
                board = game_state['board']
                current_player = game_state['currentPlayer']
                row, col = self.server.bot_instance.get_move(board, current_player)
                
                # Send response
                response = {'row': row, 'col': col}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"Error in get_move endpoint: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress HTTP server logs"""
        pass

class BotHTTPServer(HTTPServer):
    def __init__(self, server_address, bot_instance):
        self.bot_instance = bot_instance
        super().__init__(server_address, BotHTTPHandler)

class GomokuBot:
    def __init__(self, server_host, server_port=8080, bot_port=8081):
        # Clean up server_host - remove http:// if present
        if server_host.startswith('http://'):
            server_host = server_host[7:]  # Remove 'http://'
        elif server_host.startswith('https://'):
            server_host = server_host[8:]  # Remove 'https://'
        
        self.server_host = server_host
        self.server_port = server_port
        self.bot_port = bot_port
        self.base_url = f"http://{server_host}:{server_port}"
        self.player = None  # Will be set when registering
        self.http_server = None
        
    def get_move(self, board, current_player):
        """
        SMART BOT STRATEGY - Focus on completing five in a row!
        
        Parameters:
        - board: 15x15 list of lists representing the game board
        - current_player: 'X' or 'O' (your player)
        
        Returns:
        - tuple (row, col) with your move (0-14 for both row and col)
        """
        
        # ========================================
        # SMART BOT IMPLEMENTATION
        # ========================================
        
        # Find all valid moves
        valid_moves = []
        for i in range(15):
            for j in range(15):
                if board[i][j] == ' ':
                    valid_moves.append((i, j))
        
        if not valid_moves:
            return (7, 7)  # Fallback
        
        # Strategy priority:
        # 1. Win immediately (5 in a row)
        # 2. Block opponent from winning
        # 3. Create winning opportunities (4 in a row)
        # 4. Block opponent's 4-in-a-row threats
        # 5. Create 3-in-a-row opportunities
        # 6. Block opponent's 3-in-a-row threats
        # 7. Play in center or near existing pieces
        
        # Check for immediate win
        winning_move = self.find_winning_move(board, current_player)
        if winning_move:
            return winning_move
        
        # Check for opponent's winning move (block it)
        opponent = 'O' if current_player == 'X' else 'X'
        blocking_move = self.find_winning_move(board, opponent)
        if blocking_move:
            return blocking_move
        
        # Look for moves that create 4-in-a-row opportunities
        four_move = self.find_four_in_row_move(board, current_player)
        if four_move:
            return four_move
        
        # Block opponent's 4-in-a-row threats
        block_four = self.find_four_in_row_move(board, opponent)
        if block_four:
            return block_four
        
        # Look for moves that create 3-in-a-row opportunities
        three_move = self.find_three_in_row_move(board, current_player)
        if three_move:
            return three_move
        
        # Block opponent's 3-in-a-row threats
        block_three = self.find_three_in_row_move(board, opponent)
        if block_three:
            return block_three
        
        # Play strategically near existing pieces or center
        strategic_move = self.find_strategic_move(board, current_player)
        if strategic_move:
            return strategic_move
        
        # Fallback to random move
        import random
        return random.choice(valid_moves)
    
    def find_winning_move(self, board, player):
        """Find a move that creates 5 in a row"""
        for i in range(15):
            for j in range(15):
                if board[i][j] == ' ':
                    # Try this move
                    board[i][j] = player
                    if self.check_win_at_position(board, i, j, player):
                        board[i][j] = ' '  # Restore
                        return (i, j)
                    board[i][j] = ' '  # Restore
        return None
    
    def find_four_in_row_move(self, board, player):
        """Find a move that creates 4 in a row (with space to win)"""
        for i in range(15):
            for j in range(15):
                if board[i][j] == ' ':
                    # Try this move
                    board[i][j] = player
                    if self.count_consecutive(board, i, j, player) >= 4:
                        board[i][j] = ' '  # Restore
                        return (i, j)
                    board[i][j] = ' '  # Restore
        return None
    
    def find_three_in_row_move(self, board, player):
        """Find a move that creates 3 in a row"""
        for i in range(15):
            for j in range(15):
                if board[i][j] == ' ':
                    # Try this move
                    board[i][j] = player
                    if self.count_consecutive(board, i, j, player) >= 3:
                        board[i][j] = ' '  # Restore
                        return (i, j)
                    board[i][j] = ' '  # Restore
        return None
    
    def find_strategic_move(self, board, player):
        """Find a strategic move near existing pieces or center"""
        # Prefer center and near existing pieces
        center_moves = [(7, 7), (6, 7), (8, 7), (7, 6), (7, 8), (6, 6), (8, 8), (6, 8), (8, 6)]
        
        for move in center_moves:
            if board[move[0]][move[1]] == ' ':
                return move
        
        # Look for moves near existing pieces
        for i in range(15):
            for j in range(15):
                if board[i][j] == ' ':
                    # Check if this position is near any existing piece
                    if self.is_near_existing_piece(board, i, j):
                        return (i, j)
        
        return None
    
    def check_win_at_position(self, board, row, col, player):
        """Check if placing at (row, col) creates a win for player"""
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        
        for dr, dc in directions:
            count = 1
            
            # Check in positive direction
            r, c = row + dr, col + dc
            while (0 <= r < 15 and 0 <= c < 15 and board[r][c] == player):
                count += 1
                r += dr
                c += dc
            
            # Check in negative direction
            r, c = row - dr, col - dc
            while (0 <= r < 15 and 0 <= c < 15 and board[r][c] == player):
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        return False
    
    def count_consecutive(self, board, row, col, player):
        """Count consecutive pieces in all directions from position"""
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        max_count = 0
        
        for dr, dc in directions:
            count = 1
            
            # Check in positive direction
            r, c = row + dr, col + dc
            while (0 <= r < 15 and 0 <= c < 15 and board[r][c] == player):
                count += 1
                r += dr
                c += dc
            
            # Check in negative direction
            r, c = row - dr, col - dc
            while (0 <= r < 15 and 0 <= c < 15 and board[r][c] == player):
                count += 1
                r -= dr
                c -= dc
            
            max_count = max(max_count, count)
        
        return max_count
    
    def is_near_existing_piece(self, board, row, col):
        """Check if position is near any existing piece"""
        for i in range(max(0, row-2), min(15, row+3)):
            for j in range(max(0, col-2), min(15, col+3)):
                if board[i][j] != ' ':
                    return True
        return False
    
    def register_with_server(self, player):
        """Register this bot with the server"""
        try:
            # Get local IP address
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            bot_info = {
                'host': local_ip,
                'port': self.bot_port,
                'name': f'Python Bot ({player})'
            }
            
            response = requests.post(
                f"{self.base_url}/api/register-bot",
                json={'player': player, 'bot_info': bot_info},
                timeout=5
            )
            
            if response.status_code == 200:
                self.player = player
                print(f"✅ Successfully registered as player {player}")
                return True
            else:
                print(f"❌ Failed to register: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error registering with server: {e}")
            return False
    
    def start_bot_server(self):
        """Start the HTTP server for this bot using standard library"""
        try:
            # Start HTTP server with custom server class
            self.http_server = BotHTTPServer(('0.0.0.0', self.bot_port), self)
            print(f"🤖 Bot server starting on port {self.bot_port}")
            print(f"🌐 Bot will accept move requests at http://0.0.0.0:{self.bot_port}/get_move")
            print("⏹️  Press Ctrl+C to stop the bot")
            
            # Run server
            self.http_server.serve_forever()
            
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
        except Exception as e:
            print(f"❌ Error starting bot server: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python client_python.py <server_host> <player> [bot_port]")
        print("Example: python client_python.py 192.168.1.100 X 8081")
        print()
        print("Requirements:")
        print("- Python 3.6+")
        print("- requests library: pip install requests")
        sys.exit(1)
    
    server_host = sys.argv[1]
    player = sys.argv[2]
    bot_port = int(sys.argv[3]) if len(sys.argv) > 3 else 8081
    
    if player not in ['X', 'O']:
        print("Player must be 'X' or 'O'")
        sys.exit(1)
    
    # Create bot instance
    bot = GomokuBot(server_host, 8080, bot_port)
    
    # Register with server
    if not bot.register_with_server(player):
        print("Failed to register with server. Exiting.")
        sys.exit(1)
    
    print("🤖 Bot is ready to play!")
    print("📋 Available variables in get_move():")
    print("   - board: 15x15 array ('X', 'O', or ' ')")
    print("   - current_player: 'X' or 'O'")
    print()
    print("💡 Edit the get_move() function to implement your strategy!")
    print()
    
    # Start the bot's HTTP server
    bot.start_bot_server()

if __name__ == "__main__":
    main() 