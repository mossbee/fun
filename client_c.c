/*
 * Gomoku Bot Client - C Version
 * Compile: gcc -o client_c client_c.c
 * Run: ./client_c <server_ip>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>

#define BOARD_SIZE 15
#define BUFFER_SIZE 4096
#define MAX_MOVES 225

typedef struct {
    char board[BOARD_SIZE][BOARD_SIZE];
    char current_player;
    int game_over;
    char winner;
} GameState;

typedef struct {
    int row;
    int col;
} Move;

// Function to implement your bot logic
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
    
    // ========================================
    // EXAMPLE BOT IMPLEMENTATION
    // ========================================
    // This is a simple random bot. Replace this with your strategy!
    
    // Find all valid moves
    int valid_moves[MAX_MOVES][2];  // Max possible moves
    int valid_count = 0;
    
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            if (board[i][j] == ' ') {
                valid_moves[valid_count][0] = i;
                valid_moves[valid_count][1] = j;
                valid_count++;
            }
        }
    }
    
    // Pick a random move
    if (valid_count > 0) {
        int random_index = rand() % valid_count;
        move.row = valid_moves[random_index][0];
        move.col = valid_moves[random_index][1];
    } else {
        move.row = 7;
        move.col = 7;
    }
    
    return move;
}

int send_http_request(const char* host, int port, const char* method, const char* path, 
                     const char* data, char* response, int response_size) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        return -1;
    }
    
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    
    if (inet_pton(AF_INET, host, &server_addr.sin_addr) <= 0) {
        close(sock);
        return -1;
    }
    
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        close(sock);
        return -1;
    }
    
    // Build HTTP request
    char request[BUFFER_SIZE];
    if (data && strlen(data) > 0) {
        snprintf(request, BUFFER_SIZE,
                "%s %s HTTP/1.1\r\n"
                "Host: %s\r\n"
                "Content-Type: application/json\r\n"
                "Content-Length: %zu\r\n"
                "\r\n"
                "%s",
                method, path, host, strlen(data), data);
    } else {
        snprintf(request, BUFFER_SIZE,
                "%s %s HTTP/1.1\r\n"
                "Host: %s\r\n"
                "\r\n",
                method, path, host);
    }
    
    // Send request
    if (send(sock, request, strlen(request), 0) < 0) {
        close(sock);
        return -1;
    }
    
    // Receive response
    int bytes_received = recv(sock, response, response_size - 1, 0);
    if (bytes_received > 0) {
        response[bytes_received] = '\0';
    }
    
    close(sock);
    return bytes_received;
}

int parse_json_board(const char* json_str, char board[BOARD_SIZE][BOARD_SIZE]) {
    // Simple JSON parsing for the board
    // This is a simplified parser - in a real implementation you'd use a proper JSON library
    
    const char* board_start = strstr(json_str, "\"board\":");
    if (!board_start) return 0;
    
    // Find the board array
    const char* array_start = strchr(board_start, '[');
    if (!array_start) return 0;
    
    int row = 0, col = 0;
    const char* p = array_start + 1;
    
    while (row < BOARD_SIZE && *p) {
        if (*p == '[') {
            col = 0;
            p++;
            while (col < BOARD_SIZE && *p && *p != ']') {
                if (*p == '"') {
                    p++;
                    if (*p == 'X' || *p == 'O' || *p == ' ') {
                        board[row][col] = *p;
                    } else {
                        board[row][col] = ' ';
                    }
                    col++;
                    p++;
                }
                p++;
            }
            row++;
        }
        p++;
    }
    
    return 1;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <server_ip>\n", argv[0]);
        printf("Example: %s 192.168.1.100\n", argv[0]);
        printf("\nNote: This client makes HTTP requests to the server.\n");
        printf("Make sure the server is running and accessible.\n");
        return 1;
    }
    
    char* server_ip = argv[1];
    
    // Initialize random seed
    srand(time(NULL));
    
    printf("🎮 GOMOKU BOT CLIENT - C\n");
    printf("==================================================\n");
    printf("Connecting to server: %s\n", server_ip);
    printf("\n🤖 Bot is ready to play!\n");
    printf("📋 Available variables in get_move():\n");
    printf("   - board: 15x15 array ('X', 'O', or ' ')\n");
    printf("   - current_player: 'X' or 'O'\n");
    printf("\n💡 Edit the get_move() function to implement your strategy!\n\n");
    
    char response[BUFFER_SIZE];
    char board[BOARD_SIZE][BOARD_SIZE];
    
    while (1) {
        // Get game state
        if (send_http_request(server_ip, 8080, "GET", "/api/game-state", 
                             NULL, response, BUFFER_SIZE) > 0) {
            
            // Parse the response
            if (parse_json_board(response, board)) {
                
                // Extract current player (simplified)
                char current_player = 'X';
                const char* player_str = strstr(response, "\"currentPlayer\":\"");
                if (player_str) {
                    player_str += 16;
                    if (*player_str == 'O') current_player = 'O';
                }
                
                // Check if game is over
                if (strstr(response, "\"gameOver\":true")) {
                    printf("🏁 Game over!\n");
                    break;
                }
                
                // Get our move
                Move move = get_move(board, current_player);
                
                // Validate move
                if (move.row < 0 || move.row >= BOARD_SIZE || 
                    move.col < 0 || move.col >= BOARD_SIZE) {
                    printf("❌ Invalid move: (%d, %d)\n", move.row, move.col);
                    sleep(2);
                    continue;
                }
                
                if (board[move.row][move.col] != ' ') {
                    printf("❌ Position (%d, %d) is already occupied\n", move.row, move.col);
                    sleep(2);
                    continue;
                }
                
                // Send move
                char move_data[100];
                snprintf(move_data, sizeof(move_data), "{\"row\":%d,\"col\":%d}", move.row, move.col);
                
                printf("🎯 Making move: (%d, %d)\n", move.row, move.col);
                
                if (send_http_request(server_ip, 8080, "POST", "/api/move", 
                                     move_data, response, BUFFER_SIZE) > 0) {
                    printf("✅ Move sent successfully\n");
                } else {
                    printf("❌ Failed to send move\n");
                }
                
            } else {
                printf("❌ Could not parse game state\n");
            }
        } else {
            printf("❌ Could not get game state\n");
        }
        
        sleep(1);
    }
    
    return 0;
} 