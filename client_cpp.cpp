/*
 * Gomoku Bot Client - C++ Version
 * Compile: g++ -o client_cpp client_cpp.cpp
 * Run: ./client_cpp <server_ip>
 */

#include <iostream>
#include <string>
#include <vector>
#include <random>
#include <chrono>
#include <thread>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

const int BOARD_SIZE = 15;
const int BUFFER_SIZE = 4096;

struct Move {
    int row;
    int col;
};

class GomokuBot {
private:
    std::string server_ip;
    int server_port;
    
public:
    GomokuBot(const std::string& ip, int port = 8080) 
        : server_ip(ip), server_port(port) {}
    
    bool send_http_request(const std::string& method, const std::string& path, 
                          const std::string& data, std::string& response) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            return false;
        }
        
        struct sockaddr_in server_addr;
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(server_port);
        
        if (inet_pton(AF_INET, server_ip.c_str(), &server_addr.sin_addr) <= 0) {
            close(sock);
            return false;
        }
        
        if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
            close(sock);
            return false;
        }
        
        // Build HTTP request
        std::string request;
        if (!data.empty()) {
            request = method + " " + path + " HTTP/1.1\r\n"
                     "Host: " + server_ip + "\r\n"
                     "Content-Type: application/json\r\n"
                     "Content-Length: " + std::to_string(data.length()) + "\r\n"
                     "\r\n" + data;
        } else {
            request = method + " " + path + " HTTP/1.1\r\n"
                     "Host: " + server_ip + "\r\n"
                     "\r\n";
        }
        
        // Send request
        if (send(sock, request.c_str(), request.length(), 0) < 0) {
            close(sock);
            return false;
        }
        
        // Receive response
        char buffer[BUFFER_SIZE];
        int bytes_received = recv(sock, buffer, BUFFER_SIZE - 1, 0);
        if (bytes_received > 0) {
            buffer[bytes_received] = '\0';
            response = std::string(buffer);
        }
        
        close(sock);
        return bytes_received > 0;
    }
    
    bool parse_json_board(const std::string& json_str, std::vector<std::vector<char>>& board) {
        // Simple JSON parsing for the board
        // This is a simplified parser - in a real implementation you'd use a proper JSON library
        
        size_t board_start = json_str.find("\"board\":");
        if (board_start == std::string::npos) return false;
        
        size_t array_start = json_str.find('[', board_start);
        if (array_start == std::string::npos) return false;
        
        board.clear();
        board.resize(BOARD_SIZE, std::vector<char>(BOARD_SIZE, ' '));
        
        size_t pos = array_start + 1;
        int row = 0;
        
        while (row < BOARD_SIZE && pos < json_str.length()) {
            size_t row_start = json_str.find('[', pos);
            if (row_start == std::string::npos) break;
            
            size_t row_end = json_str.find(']', row_start);
            if (row_end == std::string::npos) break;
            
            std::string row_str = json_str.substr(row_start + 1, row_end - row_start - 1);
            
            int col = 0;
            size_t col_pos = 0;
            while (col < BOARD_SIZE && col_pos < row_str.length()) {
                size_t quote_start = row_str.find('"', col_pos);
                if (quote_start == std::string::npos) break;
                
                size_t quote_end = row_str.find('"', quote_start + 1);
                if (quote_end == std::string::npos) break;
                
                char cell = row_str[quote_start + 1];
                if (cell == 'X' || cell == 'O' || cell == ' ') {
                    board[row][col] = cell;
                }
                
                col++;
                col_pos = quote_end + 1;
            }
            
            row++;
            pos = row_end + 1;
        }
        
        return true;
    }
    
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
        
        // ========================================
        // EXAMPLE BOT IMPLEMENTATION
        // ========================================
        // This is a simple random bot. Replace this with your strategy!
        
        std::vector<Move> valid_moves;
        
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (board[i][j] == ' ') {
                    valid_moves.push_back({i, j});
                }
            }
        }
        
        if (!valid_moves.empty()) {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> dis(0, valid_moves.size() - 1);
            return valid_moves[dis(gen)];
        }
        
        return {7, 7};  // Fallback to center
    }
    
    void play_game() {
        std::cout << "🤖 Bot is ready to play!" << std::endl;
        std::cout << "📋 Available variables in get_move():" << std::endl;
        std::cout << "   - board: 15x15 vector ('X', 'O', or ' ')" << std::endl;
        std::cout << "   - current_player: 'X' or 'O'" << std::endl;
        std::cout << std::endl;
        std::cout << "💡 Edit the get_move() method to implement your strategy!" << std::endl;
        std::cout << std::endl;
        
        while (true) {
            try {
                // Get game state
                std::string response;
                if (send_http_request("GET", "/api/game-state", "", response)) {
                    
                    std::vector<std::vector<char>> board;
                    if (parse_json_board(response, board)) {
                        
                        // Extract current player
                        char current_player = 'X';
                        size_t player_pos = response.find("\"currentPlayer\":\"");
                        if (player_pos != std::string::npos) {
                            player_pos += 16;
                            if (response[player_pos] == 'O') current_player = 'O';
                        }
                        
                        // Check if game is over
                        if (response.find("\"gameOver\":true") != std::string::npos) {
                            std::cout << "🏁 Game over!" << std::endl;
                            break;
                        }
                        
                        // Get our move
                        Move move = get_move(board, current_player);
                        
                        // Validate move
                        if (move.row < 0 || move.row >= BOARD_SIZE || 
                            move.col < 0 || move.col >= BOARD_SIZE) {
                            std::cout << "❌ Invalid move: (" << move.row << ", " << move.col << ")" << std::endl;
                            std::this_thread::sleep_for(std::chrono::seconds(2));
                            continue;
                        }
                        
                        if (board[move.row][move.col] != ' ') {
                            std::cout << "❌ Position (" << move.row << ", " << move.col << ") is already occupied" << std::endl;
                            std::this_thread::sleep_for(std::chrono::seconds(2));
                            continue;
                        }
                        
                        // Send move
                        std::string move_data = "{\"row\":" + std::to_string(move.row) + 
                                              ",\"col\":" + std::to_string(move.col) + "}";
                        
                        std::cout << "🎯 Making move: (" << move.row << ", " << move.col << ")" << std::endl;
                        
                        if (send_http_request("POST", "/api/move", move_data, response)) {
                            std::cout << "✅ Move sent successfully" << std::endl;
                        } else {
                            std::cout << "❌ Failed to send move" << std::endl;
                        }
                        
                    } else {
                        std::cout << "❌ Could not parse game state" << std::endl;
                    }
                } else {
                    std::cout << "❌ Could not get game state" << std::endl;
                }
                
                std::this_thread::sleep_for(std::chrono::seconds(1));
                
            } catch (const std::exception& e) {
                std::cout << "❌ Error in game loop: " << e.what() << std::endl;
                std::this_thread::sleep_for(std::chrono::seconds(2));
            }
        }
    }
};

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cout << "Usage: " << argv[0] << " <server_ip>" << std::endl;
        std::cout << "Example: " << argv[0] << " 192.168.1.100" << std::endl;
        std::cout << std::endl;
        std::cout << "Note: This client makes HTTP requests to the server." << std::endl;
        std::cout << "Make sure the server is running and accessible." << std::endl;
        return 1;
    }
    
    std::string server_ip = argv[1];
    
    std::cout << "🎮 GOMOKU BOT CLIENT - C++" << std::endl;
    std::cout << "==================================================" << std::endl;
    std::cout << "Connecting to server: " << server_ip << std::endl;
    std::cout << std::endl;
    
    GomokuBot bot(server_ip);
    bot.play_game();
    
    return 0;
} 