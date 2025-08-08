let gameInterval;
let isGameRunning = false;

async function startGame() {
    const response = await fetch('/api/start-game', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    });
    const result = await response.json();
    if (result.status === 'success') {
        updateStatus('Game started! Bots are playing...', 'playing');
        isGameRunning = true;
        startGameLoop();
    } else {
        alert('Please wait for both bots to connect first!');
    }
}

async function resetGame() {
    await fetch('/api/reset-game', {method: 'POST'});
    updateStatus('Game reset - Waiting for bots to connect', 'waiting');
    isGameRunning = false;
    stopGameLoop();
    refreshBoard();
}

async function refreshBoard() {
    try {
        const response = await fetch('/api/game-state');
        const gameState = await response.json();
        displayBoard(gameState.board);
        updateGameStatus(gameState);
        
        // Stop auto-refresh if game is over
        if (gameState.gameOver && isGameRunning) {
            stopGameLoop();
            isGameRunning = false;
        }
    } catch (error) {
        console.error('Error refreshing board:', error);
    }
}

async function updateBotStatus() {
    try {
        const response = await fetch('/api/connected-bots');
        const bots = await response.json();
        
        // Update Player X status
        const botXStatus = document.getElementById('bot-x-status');
        if (bots.X) {
            botXStatus.textContent = `Connected: ${bots.X.name} (${bots.X.host}:${bots.X.port})`;
            botXStatus.className = 'bot-status connected';
        } else {
            botXStatus.textContent = 'Not Connected';
            botXStatus.className = 'bot-status disconnected';
        }
        
        // Update Player O status
        const botOStatus = document.getElementById('bot-o-status');
        if (bots.O) {
            botOStatus.textContent = `Connected: ${bots.O.name} (${bots.O.host}:${bots.O.port})`;
            botOStatus.className = 'bot-status connected';
        } else {
            botOStatus.textContent = 'Not Connected';
            botOStatus.className = 'bot-status disconnected';
        }
        
        // Update main status
        const hasBothBots = bots.X && bots.O;
        if (hasBothBots && !isGameRunning) {
            updateStatus('Both bots connected! Click "Start Game" to begin', 'waiting');
        } else if (!hasBothBots && !isGameRunning) {
            updateStatus('Waiting for bots to connect...', 'waiting');
        }
        
    } catch (error) {
        console.error('Error updating bot status:', error);
    }
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
        statusText = `🏁 Game Over! Winner: ${gameState.winner}`;
        statusClass = 'finished';
    } else if (isGameRunning) {
        statusText = `🎮 Game in progress - Current Player: ${gameState.currentPlayer}`;
        statusClass = 'playing';
    } else {
        statusText = `⏳ Waiting for game to start - Current Player: ${gameState.currentPlayer}`;
        statusClass = 'waiting';
    }
    
    updateStatus(statusText, statusClass);
}

function updateStatus(text, className) {
    const status = document.getElementById('status');
    status.textContent = text;
    status.className = `status ${className}`;
}

function startGameLoop() {
    // Refresh immediately
    refreshBoard();
    // Then refresh every 500ms for smooth updates
    gameInterval = setInterval(refreshBoard, 500);
}

function stopGameLoop() {
    if (gameInterval) {
        clearInterval(gameInterval);
        gameInterval = null;
    }
}

// Load initial state
refreshBoard();
updateBotStatus();

// Auto-refresh board and bot status
setInterval(() => {
    if (!isGameRunning) {
        refreshBoard();
        updateBotStatus();
    }
}, 2000); 