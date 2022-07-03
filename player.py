import pygame
import sys
import random
import math

class Player:
    """
    This class creates a player.
    """
    def __init__(self, mark):
        self.mark = mark

    def get_move(self):
        pass

class HumanPlayer(Player):
    """
    This class is a child class of player.
    This class creates a human player.
    It can get move from the human player by the position
    where the mouse is clicked.
    """

    def __init__(self, mark):
        super().__init__(mark)

    def get_move(self, tictactoe):
        valid_square = False
        pos = 100

        while not valid_square:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]

                    click_row = int(mouseY // tictactoe.SQUARE_SIZE)
                    click_col = int(mouseX // tictactoe.SQUARE_SIZE)

                    pos = click_row * (tictactoe.board.size//3) + click_col
                    try:
                        pos = int(pos)
                        if pos not in tictactoe.board.empty_square():
                            raise ValueError
                        valid_square = True
                    except ValueError:
                        tictactoe.draw_help_msg("Invalid Square.", 12, tictactoe.bar_txt_x, tictactoe.bar_txt_y)
                        pygame.display.update()
                        print("Invalid Square.")

        return pos


class EasyAI(Player):
    """
    This class is a child class of player.
    This class creates a computer player.
    This computer player makes a move by
    randomly choosing an empty square on the board.
    """
    def __init__(self, mark):
        super().__init__(mark)

    def get_move(self, tictactoe):
        pos = 100
        pos = random.choice(tictactoe.board.empty_square())
        return pos

class HardAI(Player):
    """
    This class is a child class of player.
    This class creates a computer player.
    This computer player choose the best move on the board.
    """
    def __init__(self, mark):
        super().__init__(mark)

    def get_move(self, tictactoe):
        if len(tictactoe.board.empty_square()) == 9:
            best_pos = random.choice(tictactoe.board.empty_square())
        else:
            best_pos = self.minimax(tictactoe, self.mark)["position"]
        return best_pos

    def minimax(self, tictactoe, player):
        max_player = self.mark
        min_player = tictactoe.minimizer.mark if player == self.mark else self.mark

        if tictactoe.check_winning() == min_player:
            return {"position": -1, "score": 1*(len(tictactoe.board.empty_square()) + 1) \
                if min_player == max_player \
                else -1 * (len(tictactoe.board.empty_square()) + 1)}
        elif len(tictactoe.board.empty_square()) == 0:
            return {"position": -1, "score": 0}

        if player == max_player:
            best = {"position": -1, "score": -math.inf}
        else:
            best = {"position": -1, "score": math.inf}

        for pos in tictactoe.board.empty_square():
            tictactoe.make_move(player, pos)
            sim_score = self.minimax(tictactoe, min_player)
            tictactoe.board.undo_move(pos)
            tictactoe.winner = -1
            sim_score["position"] = pos

            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score

        return best
