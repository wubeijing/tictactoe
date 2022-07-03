import numpy as np
import pygame
import sys
from player import *
from menu import *

class Board:
    """
    This class is used to create a 1d array of zeros with default size of 9.
    """

    def __init__(self, size=9):
        self.size = size
        self.board = np.zeros((self.size))

    def display(self):
        print(self.board)

    def transform(self):
        """ Reshape the 1d array to 3x3. """
        return np.reshape(self.board, (self.size//3, self.size//3))

    def length(self):
        return len(self.board)

    def occupied_square(self, pos):
        """ Check whether a square is occupied. """
        return self.board[pos] != 0

    def empty_square(self):
        """ Return a list of empty squares. """
        return [i for i in range(len(self.board)) if self.board[i] == 0]

    def place_move(self, player, pos):
        """ If a square is not occupied, player places move in the square. """
        assert not self.occupied_square(pos)
        self.board[pos] = player

    def undo_move(self, pos):
        self.board[pos] = 0

    def reset(self):
        """ Reset board to all zeros. """
        for i in range(len(self.board)):
            self.board[i] = 0

    def __str__(self):
        return [i for i in range(len(self.board))]

    def __repr__(self):
        return __str__(self)

class TicTacToe():
    """
    This class plays TicTacToe game.
    """

    def __init__(self):

        self.board = Board()
        self.WIDTH = 600
        self.BAR = 50
        self.HEIGHT = self.WIDTH + self.BAR
        self.LINE_WIDTH = 15
        self.SQUARE_SIZE = self.WIDTH//(self.board.length()//3)
        self.CIRCLE_RADIUS = self.SQUARE_SIZE//3
        self.CIRCLE_WIDTH = 15
        self.SPACE = self.SQUARE_SIZE//4
        self.CROSS_WIDTH = 25
        self.bar_txt_x = self.WIDTH/2
        self.bar_txt_y = self.HEIGHT-30

        self.BG_COLOR = (0, 0, 0)
        self.LINE_COLOR = (128, 128, 128)
        self.WINNING_LINE = (255, 255, 255)
        self.font_name = "8-BIT WONDER.TTF"
        self.font_color = (255, 255, 255)
        self.PLAYER1_COLOR = (214, 45, 32)
        self.PLAYER2_COLOR = (0, 87, 231)

        self.player = -1
        self.winner = -1
        self.maximizer = HardAI(1)
        self.minimizer = HumanPlayer(2)

        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False

        self.running = True
        self.playing = False
        self.main_menu = MainMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill(self.BG_COLOR)

    def draw_lines(self):
        """ Draw board lines. """

        pygame.draw.line(self.screen, self.LINE_COLOR, \
                         (0, 0), (self.SQUARE_SIZE*3, 0), \
                        self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, \
                         (0, self.SQUARE_SIZE), (self.SQUARE_SIZE*3, self.SQUARE_SIZE), \
                        self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, \
                         (0, self.SQUARE_SIZE*2), (self.SQUARE_SIZE*3, self.SQUARE_SIZE*2), \
                        self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, \
                         (0, self.SQUARE_SIZE*3), (self.SQUARE_SIZE*3, self.SQUARE_SIZE*3), \
                        self.LINE_WIDTH//2)
        pygame.draw.line(self.screen, self.LINE_COLOR, \
                         (0, 0), (0, self.SQUARE_SIZE*3), \
                        self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, \
                         (self.SQUARE_SIZE, 0), (self.SQUARE_SIZE, self.SQUARE_SIZE*3), \
                        self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, \
                         (self.SQUARE_SIZE*2, 0), (self.SQUARE_SIZE*2, self.SQUARE_SIZE*3), \
                        self.LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, \
                         (self.SQUARE_SIZE*3, 0), (self.SQUARE_SIZE*3, self.SQUARE_SIZE*3), \
                        self.LINE_WIDTH)

    def draw_figures(self):
        """ Draw 'X' or 'O' on game board. """

        transform_board = self.board.transform()
        for row in range(self.board.length()//3):
            for col in range(self.board.length()//3):
                if transform_board[row][col] == 1:
                    pygame.draw.circle(self.screen, self.PLAYER1_COLOR, \
                    (int(col*self.SQUARE_SIZE + self.SQUARE_SIZE//2), int(row*self.SQUARE_SIZE + self.SQUARE_SIZE//2)), \
                    self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)
                elif transform_board[row][col] == 2:
                    pygame.draw.line(self.screen, self.PLAYER2_COLOR, \
                        (col*self.SQUARE_SIZE + self.SPACE, row*self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE), \
                        (col*self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE, row*self.SQUARE_SIZE + self.SPACE), \
                        self.CROSS_WIDTH)
                    pygame.draw.line(self.screen, self.PLAYER2_COLOR, \
                        (col*self.SQUARE_SIZE + self.SPACE, row*self.SQUARE_SIZE + self.SPACE), \
                        (col*self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE, row*self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE), \
                        self.CROSS_WIDTH)

    def draw_vertical_winning_line(self, col):
        posX = col*self.SQUARE_SIZE + self.SQUARE_SIZE//2
        pygame.draw.line(self.screen, self.WINNING_LINE, \
            (posX, self.LINE_WIDTH), (posX, self.HEIGHT-self.LINE_WIDTH), \
            self.LINE_WIDTH)

    def draw_horizontal_winning_line(self, row):
        posY = row*self.SQUARE_SIZE + self.SQUARE_SIZE//2
        pygame.draw.line(self.screen, self.WINNING_LINE, \
            (self.LINE_WIDTH, posY), (self.HEIGHT-self.LINE_WIDTH, posY), \
            self.LINE_WIDTH)

    def draw_asc_diagonal_winning_line(self):
        pygame.draw.line(self.screen, self.WINNING_LINE, \
            (self.LINE_WIDTH, self.HEIGHT-self.BAR-self.LINE_WIDTH), \
            (self.WIDTH-self.LINE_WIDTH, self.LINE_WIDTH), \
            self.LINE_WIDTH)

    def draw_desc_diagonal_winning_line(self):
        pygame.draw.line(self.screen, self.WINNING_LINE, \
            (self.LINE_WIDTH, self.LINE_WIDTH), \
            (self.WIDTH-self.LINE_WIDTH, self.HEIGHT-self.BAR-self.LINE_WIDTH), \
            self.LINE_WIDTH)

    def legal_move(self, player, pos):
        return not self.board.occupied_square(pos)

    def make_move(self, player, pos):
        assert self.legal_move(player, pos)
        if pos in self.board.empty_square():
            self.board.place_move(player, pos)

    def check_winning(self):
        """ Returns winner if any. """
        transform_board = self.board.transform()
        # horizontal
        for row in range(self.board.length()//3):
            if transform_board[row][0] == transform_board[row][1] \
                and transform_board[row][0] == transform_board[row][2]:
                    if transform_board[row][0] == 1:
                        self.winner = 1
                    elif transform_board[row][0] == 2:
                        self.winner = 2
        # vertical
        for col in range(self.board.length()//3):
            if transform_board[0][col] == transform_board[1][col] \
                and  transform_board[0][col] == transform_board[2][col]:
                    if transform_board[0][col] == 1:
                        self.winner = 1
                    elif transform_board[0][col] == 2:
                        self.winner = 2
        # asc
        if transform_board[2][0] == transform_board[1][1] \
            and transform_board[2][0] == transform_board[0][2]:
                if transform_board[2][0] == 1:
                    self.winner = 1
                elif transform_board[2][0] == 2:
                    self.winner = 2
        # desc
        if transform_board[0][0] == transform_board[1][1] \
            and transform_board[0][0] == transform_board[2][2]:
                if transform_board[0][0] == 1:
                    self.winner = 1
                elif transform_board[0][0] == 2:
                    self.winner = 2

        return self.winner

    def draw_winning_line(self):
        transform_board = self.board.transform()
        # horizontal
        for row in range(self.board.length()//3):
            if transform_board[row][0] == transform_board[row][1] \
                and transform_board[row][0] == transform_board[row][2] \
                and transform_board[row][0] != 0:
                    self.draw_horizontal_winning_line(row)
        # vertical
        for col in range(self.board.length()//3):
            if transform_board[0][col] == transform_board[1][col] \
                and transform_board[0][col] == transform_board[2][col] \
                and transform_board[0][col] != 0:
                    self.draw_vertical_winning_line(col)
        # asc
        if transform_board[2][0] == transform_board[1][1] \
            and transform_board[2][0] == transform_board[0][2] \
            and transform_board[2][0] != 0:
                self.draw_asc_diagonal_winning_line()
        # desc
        if transform_board[0][0] == transform_board[1][1] \
            and transform_board[0][0] == transform_board[2][2] \
            and transform_board[0][0] != 0:
                self.draw_desc_diagonal_winning_line()

    def display_winner_human(self):
        if self.winner == 1:
            print("Player1 wins!")
            pygame.time.wait(1000)
            self.screen.fill(self.BG_COLOR)
            self.draw_text("Player1 Wins", 20, self.WIDTH/2, self.HEIGHT/2)
            pygame.display.update()
            pygame.time.wait(2000)

        elif self.winner == 2:
            print("Player2 wins!")
            pygame.time.wait(1000)
            self.screen.fill(self.BG_COLOR)
            self.draw_text("Player2 Wins", 20, self.WIDTH/2, self.HEIGHT/2)
            pygame.display.update()
            pygame.time.wait(2000)

        elif self.is_tie():
            print("It's a tie!")
            pygame.time.wait(1000)
            self.screen.fill(self.BG_COLOR)
            self.draw_text("Nobody Wins", 20, self.WIDTH/2, self.HEIGHT/2)
            self.draw_text("Tie", 20, self.WIDTH/2, self.HEIGHT/2+20)
            pygame.display.update()
            pygame.time.wait(2000)

    def display_winner_human_ai(self):
        if self.winner == 1:
            print("Computer wins!")
            pygame.time.wait(1000)
            self.screen.fill(self.BG_COLOR)
            self.draw_text("Computer Wins", 20, self.WIDTH/2, self.HEIGHT/2)
            pygame.display.update()
            pygame.time.wait(2000)

        elif self.winner == 2:
            print("Human wins!")
            pygame.time.wait(1000)
            self.screen.fill(self.BG_COLOR)
            self.draw_text("Human Wins", 20, self.WIDTH/2, self.HEIGHT/2)
            pygame.display.update()
            pygame.time.wait(2000)

        elif self.is_tie():
            print("It's a tie!")
            pygame.time.wait(1000)
            self.screen.fill(self.BG_COLOR)
            self.draw_text("Nobody Wins", 20, self.WIDTH/2, self.HEIGHT/2)
            self.draw_text("Tie", 20, self.WIDTH/2, self.HEIGHT/2+20)
            pygame.display.update()
            pygame.time.wait(2000)

    def is_tie(self):
        if len(self.board.empty_square()) == 0 and self.winner == -1:
            return True
        else:
            return False

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.screen.fill(self.BG_COLOR)
            if self.main_menu.state == "Human vs. Human":
                self.draw_lines()
                self.draw_help_msg("Player 1 Turn", 11, self.bar_txt_x, self.bar_txt_y)
                pygame.display.update()
                self.human_game()
                pygame.display.update()
                self.reset_keys()
                self.reset_game()
            elif self.main_menu.state == "EasyAI vs. Human":
                self.draw_lines()
                pygame.display.update()
                self.human_easyAI_game()
                pygame.display.update()
                self.reset_keys()
                self.reset_game()
            elif self.main_menu.state == "HardAI vs. Human":
                self.draw_lines()
                pygame.display.update()
                self.human_hardAI_game()
                pygame.display.update()
                self.reset_keys()
                self.reset_game()

    def check_events(self):
        """ Check keyboard events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False

    def reset_game(self):
        self.board.reset()
        self.player = -1
        self.winner = -1

    def draw_text(self, text, size, x, y):
        """ Display text on screen. """
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.font_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_help_msg(self, text, size, x, y):
        """ Display help msg on the bottom bar. """
        pygame.draw.rect(self.screen, self.BG_COLOR, \
            (self.LINE_WIDTH, self.HEIGHT-self.BAR+self.LINE_WIDTH, self.WIDTH, self.BAR), \
            0)
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, self.font_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def turn_msg(self):
        if self.player == 1:
            msg = "Click the empty spot on the board to make move. Player 1 Turn."
        elif self.player == 2:
            msg = "Click the empty spot on the board to make move. Player 2 Turn."
        return msg

    def human_game(self):

        self.player = HumanPlayer(1).mark
        game_over = False

        while not game_over:
            if self.player == HumanPlayer(1).mark:

                pos = HumanPlayer(1).get_move(self)
                self.make_move(self.player, pos)
                self.draw_figures()
                self.board.display()
                if self.player == self.check_winning() or self.is_tie():
                    self.draw_winning_line()
                    game_over = True
                self.player = HumanPlayer(2).mark
                self.draw_help_msg(self.turn_msg(), 12, self.bar_txt_x, self.bar_txt_y)
                pygame.display.update()


            elif self.player == HumanPlayer(2).mark:
                pos = HumanPlayer(2).get_move(self)
                self.make_move(self.player, pos)
                self.draw_figures()
                self.board.display()
                if self.player == self.check_winning() or self.is_tie():
                    self.draw_winning_line()
                    game_over = True
                self.player = HumanPlayer(1).mark
                self.draw_help_msg(self.turn_msg(), 12, self.bar_txt_x, self.bar_txt_y)
                pygame.display.update()

        if game_over == True:
            self.display_winner_human()

        self.playing = False

    def human_easyAI_game(self):

        self.player = EasyAI(1).mark
        game_over = False

        while not game_over:
            if self.player == EasyAI(1).mark:
                pos = EasyAI(1).get_move(self)
                self.make_move(self.player, pos)
                self.draw_figures()
                self.board.display()
                if self.player == self.check_winning() or self.is_tie():
                    self.draw_winning_line()
                    game_over = True
                self.player = HumanPlayer(2).mark
                self.draw_help_msg(self.turn_msg(), 12, self.bar_txt_x, self.bar_txt_y)
                pygame.display.update()

            elif self.player == HumanPlayer(2).mark:
                pos = HumanPlayer(2).get_move(self)
                self.make_move(self.player, pos)
                self.draw_figures()
                self.board.display()
                if self.player == self.check_winning() or self.is_tie():
                    self.draw_winning_line()
                    game_over = True
                self.player = EasyAI(1).mark
                self.draw_help_msg(self.turn_msg(), 12, self.bar_txt_x, self.bar_txt_y)
                pygame.display.update()

        if game_over == True:
            self.display_winner_human_ai()

        self.playing = False

    def human_hardAI_game(self):

        self.player = HardAI(1).mark
        game_over = False

        while not game_over:
            if self.player == self.maximizer.mark:
                pos = self.maximizer.get_move(self)
                self.make_move(self.player, pos)
                self.draw_figures()
                self.board.display()
                if self.player == self.check_winning() or self.is_tie():
                    self.draw_winning_line()
                    game_over = True
                self.player = self.minimizer.mark
                self.draw_help_msg(self.turn_msg(), 12, self.bar_txt_x, self.bar_txt_y)
                pygame.display.update()

            elif self.player == self.minimizer.mark:
                pos = self.minimizer.get_move(self)
                self.make_move(self.player, pos)
                self.draw_figures()
                self.board.display()
                if self.player == self.check_winning() or self.is_tie():
                    self.draw_winning_line()
                    game_over = True
                self.player = self.maximizer.mark
                self.draw_help_msg(self.turn_msg(), 12, self.bar_txt_x, self.bar_txt_y)
                pygame.display.update()

        if game_over == True:
            self.display_winner_human_ai()

        self.playing = False
