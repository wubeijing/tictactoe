from game import *

# Start Game
game = TicTacToe()
while game.running:
    game.curr_menu.display_menu()
    game.game_loop()
