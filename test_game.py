#!/usr/bin/env python3
"""
Test script for Gomoku game logic
"""

from server import GomokuGame

def test_basic_game():
    """Test basic game functionality"""
    print("🧪 Testing basic game functionality...")
    
    game = GomokuGame()
    
    # Test initial state
    assert game.current_player == 'X'
    assert not game.game_over
    assert game.winner is None
    
    # Test valid move
    assert game.make_move(7, 7, 'X') == True
    assert game.board[7][7] == 'X'
    assert game.current_player == 'O'
    
    # Test invalid move (same position)
    assert game.make_move(7, 7, 'O') == False
    
    # Test invalid move (out of bounds)
    assert game.make_move(15, 15, 'O') == False
    
    print("✅ Basic game functionality tests passed!")

def test_win_conditions():
    """Test win detection"""
    print("🧪 Testing win conditions...")
    
    game = GomokuGame()
    
    # Test horizontal win
    game.make_move(7, 7, 'X')  # Center
    game.make_move(7, 8, 'X')  # Right
    game.make_move(7, 9, 'X')  # Right
    game.make_move(7, 10, 'X') # Right
    game.make_move(7, 11, 'X') # Right - should win
    
    assert game.game_over == True
    assert game.winner == 'X'
    
    print("✅ Win condition tests passed!")

def test_bot_execution():
    """Test bot code execution"""
    print("🧪 Testing bot execution...")
    
    game = GomokuGame()
    
    # Test simple bot code
    bot_code = """
validMoves = []
for i in range(15):
    for j in range(15):
        if board[i][j] == ' ':
            validMoves.append({'row': i, 'col': j})

if validMoves:
    move = validMoves[0]
"""
    
    from server import GameServer
    server = GameServer()
    
    # Test bot execution
    game_state = game.get_game_state()
    move = server.execute_bot(bot_code, game_state)
    
    assert move is not None
    assert 'row' in move
    assert 'col' in move
    assert 0 <= move['row'] < 15
    assert 0 <= move['col'] < 15
    
    print("✅ Bot execution tests passed!")

def test_full_game():
    """Test a complete game"""
    print("🧪 Testing complete game...")
    
    game = GomokuGame()
    
    # Play a few moves
    moves = [
        (7, 7, 'X'),  # Center
        (7, 8, 'O'),  # Right of center
        (8, 7, 'X'),  # Below center
        (8, 8, 'O'),  # Diagonal
        (6, 7, 'X'),  # Above center
    ]
    
    for row, col, player in moves:
        assert game.make_move(row, col, player) == True
    
    # Check game state
    assert not game.game_over
    assert game.winner is None
    assert game.current_player == 'O'
    
    print("✅ Complete game test passed!")

if __name__ == "__main__":
    print("🎮 Running Gomoku game tests...")
    print("=" * 50)
    
    try:
        test_basic_game()
        test_win_conditions()
        test_bot_execution()
        test_full_game()
        
        print("=" * 50)
        print("🎉 All tests passed! The game is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 