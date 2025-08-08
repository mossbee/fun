#!/usr/bin/env python3
"""
Gomoku Bot Client - Python Version
Teams can implement their bot logic in the get_move() function.
"""

import socket
import json
import time
import sys
import requests

class GomokuBot:
    def __init__(self, server_host, server_port=8080):
        self.server_host = server_host
        self.server_port = server_port
        self.base_url = f"http://{server_host}:{server_port}"
        
    def get_game_state(self):
        """Get current game state from server"""
        try:
            response = requests.get(f"{self.base_url}/api/game-state", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"❌ Error getting game state: {e}")
        return None
    
    def send_move(self, row, col):
        """Send a move to the server"""
        try:
            move_data = {"row": row, "col": col}
            response = requests.post(f"{self.base_url}/api/move", json=move_data, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error sending move: {e}")
            return False
    
    def get_move(self, board, current_player):
        """
        IMPLEMENT YOUR BOT LOGIC HERE!
        
        Parameters:
        - board: 15x15 list of lists representing the game board
        - current_player: 'X' or 'O' (your player)
        
        Returns:
        - tuple (row, col) with your move (0-14 for both row and col)
        """
        
        # ========================================
        # EXAMPLE BOT IMPLEMENTATION
        # ========================================
        # This is a simple random bot. Replace this with your strategy!
        
        import random
        
        # Find all valid moves
        valid_moves = []
        for i in range(15):
            for j in range(15):
                if board[i][j] == ' ':
                    valid_moves.append((i, j))
        
        # Pick a random move
        if valid_moves:
            return random.choice(valid_moves)
        
        # Fallback
        return (7, 7)
    
    def play_game(self):
        """Main game loop"""
        print("🤖 Bot is ready to play!")
        print("📋 Available variables in get_move():")
        print("   - board: 15x15 array ('X', 'O', or ' ')")
        print("   - current_player: 'X' or 'O'")
        print()
        print("💡 Edit the get_move() function to implement your strategy!")
        print()
        
        while True:
            try:
                # Get current game state
                game_state = self.get_game_state()
                if not game_state:
                    print("❌ Could not get game state")
                    time.sleep(2)
                    continue
                
                # Check if game is over
                if game_state.get('gameOver', False):
                    winner = game_state.get('winner', 'Unknown')
                    print(f"🏁 Game over! Winner: {winner}")
                    break
                
                # Check if it's our turn
                current_player = game_state.get('currentPlayer')
                if not current_player:
                    print("❌ Could not determine current player")
                    time.sleep(2)
                    continue
                
                # Get our move
                board = game_state.get('board', [])
                if not board:
                    print("❌ Invalid board state")
                    time.sleep(2)
                    continue
                
                # Calculate our move
                row, col = self.get_move(board, current_player)
                
                # Validate move
                if not (0 <= row < 15 and 0 <= col < 15):
                    print(f"❌ Invalid move: ({row}, {col})")
                    time.sleep(2)
                    continue
                
                if board[row][col] != ' ':
                    print(f"❌ Position ({row}, {col}) is already occupied")
                    time.sleep(2)
                    continue
                
                # Send our move
                print(f"🎯 Making move: ({row}, {col})")
                if self.send_move(row, col):
                    print(f"✅ Move sent successfully")
                else:
                    print(f"❌ Failed to send move")
                
                # Wait a bit before next turn
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in game loop: {e}")
                time.sleep(2)

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python3 client_python.py <server_ip>")
        print("Example: python3 client_python.py 192.168.1.100")
        print()
        print("Note: This client requires the 'requests' library.")
        print("Install with: pip install requests")
        sys.exit(1)
    
    server_host = sys.argv[1]
    
    print("🎮 GOMOKU BOT CLIENT - PYTHON")
    print("=" * 50)
    print(f"Connecting to server: {server_host}")
    print()
    
    # Create and run bot
    bot = GomokuBot(server_host)
    bot.play_game()

if __name__ == "__main__":
    main() 