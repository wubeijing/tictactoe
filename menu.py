import pygame

class Menu:
    """
    This class creates base class for Menu.
    It draws the cursor, and blit screen to show text.
    """
    def __init__(self, tictactoe):
        self.tictactoe = tictactoe
        self.run_display = True
        self.MID_W = self.tictactoe.WIDTH/2
        self.MID_H = self.tictactoe.HEIGHT/2
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.OFFSET = -100

    def draw_cursor(self):
        self.tictactoe.draw_text("*", 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.tictactoe.screen.blit(self.tictactoe.screen, (0, 0))
        pygame.display.update()
        self.tictactoe.reset_keys()

class MainMenu(Menu):
    """
    This class is a child class of Menu.
    This class displays the main menu, moves cursor, and checks keyboard entry.
    """
    def __init__(self, tictactoe):
        Menu.__init__(self, tictactoe)
        self.state = "Human vs. Human"
        self.human_x = self.MID_W
        self.human_y = self.MID_H+30
        self.human_easyAI_x = self.MID_W
        self.human_easyAI_y = self.MID_H+50
        self.human_hardAI_x = self.MID_W
        self.human_hardAI_y = self.MID_H+70
        self.credits_x = self.MID_W
        self.credits_y = self.MID_H+90
        self.bar_x = self.MID_W
        self.bar_y = self.tictactoe.HEIGHT-30
        self.cursor_rect.midtop = (self.human_x + self.OFFSET, self.human_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.tictactoe.check_events()
            self.check_input()
            self.tictactoe.screen.fill(self.tictactoe.BG_COLOR)
            self.tictactoe.draw_text("TIC TAC TOE", 40, self.tictactoe.WIDTH/2, self.tictactoe.HEIGHT/2)
            self.tictactoe.draw_text("Human vs Human", 12, self.human_x, self.human_y)
            self.tictactoe.draw_text("Easy AI vs Human", 12, self.human_easyAI_x, self.human_easyAI_y)
            self.tictactoe.draw_text("Hard AI vs Human", 12, self.human_hardAI_x, self.human_hardAI_y)
            self.tictactoe.draw_text("Credits", 12, self.credits_x, self.credits_y)
            self.tictactoe.draw_help_msg("Press UP and DOWN to move cursor. Press ENTER to make selection", 11, self.bar_x, self.bar_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.tictactoe.DOWN_KEY:
            if self.state == "Human vs. Human":
                self.cursor_rect.midtop = (self.human_easyAI_x+self.OFFSET, self.human_easyAI_y)
                self.state = "EasyAI vs. Human"
            elif self.state == "EasyAI vs. Human":
                self.cursor_rect.midtop = (self.human_hardAI_x+self.OFFSET, self.human_hardAI_y)
                self.state = "HardAI vs. Human"
            elif self.state == "HardAI vs. Human":
                self.cursor_rect.midtop = (self.credits_x+self.OFFSET, self.credits_y)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.human_x+self.OFFSET, self.human_y)
                self.state = "Human vs. Human"
        elif self.tictactoe.UP_KEY:
            if self.state == "Human vs. Human":
                self.cursor_rect.midtop = (self.credits_x+self.OFFSET, self.credits_y)
                self.state = "Credits"
            elif self.state == "EasyAI vs. Human":
                self.cursor_rect.midtop = (self.human_x+self.OFFSET, self.human_y)
                self.state = "Human vs. Human"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.human_hardAI_x+self.OFFSET, self.human_hardAI_y)
                self.state = "HardAI vs. Human"
            elif self.state == "HardAI vs. Human":
                self.cursor_rect.midtop = (self.human_easyAI_x+self.OFFSET, self.human_easyAI_y)
                self.state = "EasyAI vs. Human"

    def check_input(self):
        self.move_cursor()
        if self.tictactoe.START_KEY:
            if self.state == "Human vs. Human":
                self.tictactoe.playing = True
            elif self.state == "EasyAI vs. Human":
                self.tictactoe.curr_menu = self.tictactoe.main_menu
                self.tictactoe.playing = True
            elif self.state == "HardAI vs. Human":
                self.tictactoe.curr_menu = self.tictactoe.main_menu
                self.tictactoe.playing = True
            elif self.state == "Credits":
                self.tictactoe.curr_menu = self.tictactoe.credits
            self.run_display = False

class CreditsMenu(Menu):
    """
    This class is a child class of Menu.
    This class displays the credits menu.
    """
    def __init__(self, tictactoe):
        Menu.__init__(self, tictactoe)
        self.bar_x = self.MID_W
        self.bar_y = self.tictactoe.HEIGHT-30

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.tictactoe.check_events()
            self.check_input()
            self.tictactoe.screen.fill((0, 0, 0))
            self.tictactoe.draw_text("Credits", 20, self.tictactoe.WIDTH/2, self.tictactoe.HEIGHT/2-20)
            self.tictactoe.draw_text("Made by Beijing", 20, self.tictactoe.WIDTH/2, self.tictactoe.HEIGHT/2+10)
            self.tictactoe.draw_help_msg("Press BACKSPACE to go back to Main Menu.", 11, self.bar_x, self.bar_y)
            self.blit_screen()

    def check_input(self):
        if self.tictactoe.BACK_KEY:
            self.tictactoe.curr_menu = self.tictactoe.main_menu
            self.run_display = False
