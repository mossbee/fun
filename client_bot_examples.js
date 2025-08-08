// ========================================
// GOMOKU BOT EXAMPLES
// ========================================
// These are example bot implementations that teams can use as starting points.
// Copy any of these functions and modify them to create your own bot!

// ========================================
// 1. RANDOM BOT (Basic)
// ========================================
function randomBot() {
    // Find all valid moves
    const validMoves = [];
    for (let i = 0; i < 15; i++) {
        for (let j = 0; j < 15; j++) {
            if (board[i][j] === ' ') {
                validMoves.push({row: i, col: j});
            }
        }
    }
    
    // Pick a random move
    if (validMoves.length > 0) {
        const randomIndex = Math.floor(Math.random() * validMoves.length);
        move = validMoves[randomIndex];
    }
}

// ========================================
// 2. CENTER BOT (Always plays center)
// ========================================
function centerBot() {
    // Try to play in the center
    const center = 7;
    if (board[center][center] === ' ') {
        move = {row: center, col: center};
        return;
    }
    
    // If center is taken, play randomly
    randomBot();
}

// ========================================
// 3. WIN-FIRST BOT (Tries to win, then block)
// ========================================
function winFirstBot() {
    // First, try to find a winning move
    const winningMove = findWinningMove(currentPlayer);
    if (winningMove) {
        move = winningMove;
        return;
    }
    
    // Second, try to block opponent's winning move
    const opponent = currentPlayer === 'X' ? 'O' : 'X';
    const blockingMove = findWinningMove(opponent);
    if (blockingMove) {
        move = blockingMove;
        return;
    }
    
    // Otherwise, play randomly
    randomBot();
}

function findWinningMove(player) {
    for (let i = 0; i < 15; i++) {
        for (let j = 0; j < 15; j++) {
            if (board[i][j] === ' ') {
                // Temporarily make the move
                board[i][j] = player;
                
                // Check if this creates a win
                if (checkWin(i, j, player)) {
                    board[i][j] = ' '; // Undo the move
                    return {row: i, col: j};
                }
                
                board[i][j] = ' '; // Undo the move
            }
        }
    }
    return null;
}

function checkWin(row, col, player) {
    const directions = [[1,0], [0,1], [1,1], [1,-1]];
    
    for (const [dr, dc] of directions) {
        let count = 1;
        
        // Check in positive direction
        let r = row + dr, c = col + dc;
        while (r >= 0 && r < 15 && c >= 0 && c < 15 && board[r][c] === player) {
            count++;
            r += dr;
            c += dc;
        }
        
        // Check in negative direction
        r = row - dr; c = col - dc;
        while (r >= 0 && r < 15 && c >= 0 && c < 15 && board[r][c] === player) {
            count++;
            r -= dr;
            c -= dc;
        }
        
        if (count >= 5) return true;
    }
    return false;
}

// ========================================
// 4. PATTERN BOT (Looks for patterns)
// ========================================
function patternBot() {
    // Try to win first
    const winningMove = findWinningMove(currentPlayer);
    if (winningMove) {
        move = winningMove;
        return;
    }
    
    // Try to block opponent
    const opponent = currentPlayer === 'X' ? 'O' : 'X';
    const blockingMove = findWinningMove(opponent);
    if (blockingMove) {
        move = blockingMove;
        return;
    }
    
    // Look for opportunities to create lines of 4
    const move4 = findCreatingMove(currentPlayer, 4);
    if (move4) {
        move = move4;
        return;
    }
    
    // Block opponent's lines of 4
    const block4 = findCreatingMove(opponent, 4);
    if (block4) {
        move = block4;
        return;
    }
    
    // Look for opportunities to create lines of 3
    const move3 = findCreatingMove(currentPlayer, 3);
    if (move3) {
        move = move3;
        return;
    }
    
    // Otherwise, play randomly
    randomBot();
}

function findCreatingMove(player, length) {
    for (let i = 0; i < 15; i++) {
        for (let j = 0; j < 15; j++) {
            if (board[i][j] === ' ') {
                // Check if this move creates a line of the desired length
                if (countConsecutive(i, j, player) >= length) {
                    return {row: i, col: j};
                }
            }
        }
    }
    return null;
}

function countConsecutive(row, col, player) {
    const directions = [[1,0], [0,1], [1,1], [1,-1]];
    let maxCount = 0;
    
    for (const [dr, dc] of directions) {
        let count = 1;
        
        // Check in positive direction
        let r = row + dr, c = col + dc;
        while (r >= 0 && r < 15 && c >= 0 && c < 15 && board[r][c] === player) {
            count++;
            r += dr;
            c += dc;
        }
        
        // Check in negative direction
        r = row - dr; c = col - dc;
        while (r >= 0 && r < 15 && c >= 0 && c < 15 && board[r][c] === player) {
            count++;
            r -= dr;
            c -= dc;
        }
        
        maxCount = Math.max(maxCount, count);
    }
    
    return maxCount;
}

// ========================================
// 5. EDGE BOT (Prefers edge positions)
// ========================================
function edgeBot() {
    const validMoves = [];
    const edgeMoves = [];
    
    for (let i = 0; i < 15; i++) {
        for (let j = 0; j < 15; j++) {
            if (board[i][j] === ' ') {
                validMoves.push({row: i, col: j});
                
                // Check if it's an edge position
                if (i === 0 || i === 14 || j === 0 || j === 14) {
                    edgeMoves.push({row: i, col: j});
                }
            }
        }
    }
    
    // Prefer edge moves, but fall back to any valid move
    if (edgeMoves.length > 0) {
        const randomIndex = Math.floor(Math.random() * edgeMoves.length);
        move = edgeMoves[randomIndex];
    } else if (validMoves.length > 0) {
        const randomIndex = Math.floor(Math.random() * validMoves.length);
        move = validMoves[randomIndex];
    }
}

// ========================================
// 6. CORNER BOT (Prefers corner positions)
// ========================================
function cornerBot() {
    const validMoves = [];
    const cornerMoves = [];
    
    for (let i = 0; i < 15; i++) {
        for (let j = 0; j < 15; j++) {
            if (board[i][j] === ' ') {
                validMoves.push({row: i, col: j});
                
                // Check if it's a corner position
                if ((i === 0 || i === 14) && (j === 0 || j === 14)) {
                    cornerMoves.push({row: i, col: j});
                }
            }
        }
    }
    
    // Prefer corner moves, but fall back to any valid move
    if (cornerMoves.length > 0) {
        const randomIndex = Math.floor(Math.random() * cornerMoves.length);
        move = cornerMoves[randomIndex];
    } else if (validMoves.length > 0) {
        const randomIndex = Math.floor(Math.random() * validMoves.length);
        move = validMoves[randomIndex];
    }
}

// ========================================
// 7. AGGRESSIVE BOT (Always tries to attack)
// ========================================
function aggressiveBot() {
    // Try to win
    const winningMove = findWinningMove(currentPlayer);
    if (winningMove) {
        move = winningMove;
        return;
    }
    
    // Try to create lines of 4
    const move4 = findCreatingMove(currentPlayer, 4);
    if (move4) {
        move = move4;
        return;
    }
    
    // Try to create lines of 3
    const move3 = findCreatingMove(currentPlayer, 3);
    if (move3) {
        move = move3;
        return;
    }
    
    // Try to create lines of 2
    const move2 = findCreatingMove(currentPlayer, 2);
    if (move2) {
        move = move2;
        return;
    }
    
    // Otherwise, play randomly
    randomBot();
}

// ========================================
// 8. DEFENSIVE BOT (Always tries to block)
// ========================================
function defensiveBot() {
    const opponent = currentPlayer === 'X' ? 'O' : 'X';
    
    // Block opponent's winning move
    const blockingMove = findWinningMove(opponent);
    if (blockingMove) {
        move = blockingMove;
        return;
    }
    
    // Block opponent's lines of 4
    const block4 = findCreatingMove(opponent, 4);
    if (block4) {
        move = block4;
        return;
    }
    
    // Block opponent's lines of 3
    const block3 = findCreatingMove(opponent, 3);
    if (block3) {
        move = block3;
        return;
    }
    
    // Try to win if possible
    const winningMove = findWinningMove(currentPlayer);
    if (winningMove) {
        move = winningMove;
        return;
    }
    
    // Otherwise, play randomly
    randomBot();
}

// ========================================
// HOW TO USE THESE EXAMPLES
// ========================================
// To use any of these bots, copy the function body and paste it into your bot code.
// For example, to use the win-first bot:

/*
// Copy this into your bot code:
const validMoves = [];
for (let i = 0; i < 15; i++) {
    for (let j = 0; j < 15; j++) {
        if (board[i][j] === ' ') {
            validMoves.push({row: i, col: j});
        }
    }
}

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
        if (validMoves.length > 0) {
            const randomIndex = Math.floor(Math.random() * validMoves.length);
            move = validMoves[randomIndex];
        }
    }
}

function findWinningMove(player) {
    for (let i = 0; i < 15; i++) {
        for (let j = 0; j < 15; j++) {
            if (board[i][j] === ' ') {
                board[i][j] = player;
                if (checkWin(i, j, player)) {
                    board[i][j] = ' ';
                    return {row: i, col: j};
                }
                board[i][j] = ' ';
            }
        }
    }
    return null;
}

function checkWin(row, col, player) {
    const directions = [[1,0], [0,1], [1,1], [1,-1]];
    for (const [dr, dc] of directions) {
        let count = 1;
        let r = row + dr, c = col + dc;
        while (r >= 0 && r < 15 && c >= 0 && c < 15 && board[r][c] === player) {
            count++;
            r += dr;
            c += dc;
        }
        r = row - dr; c = col - dc;
        while (r >= 0 && r < 15 && c >= 0 && c < 15 && board[r][c] === player) {
            count++;
            r -= dr;
            c -= dc;
        }
        if (count >= 5) return true;
    }
    return false;
}
*/ 