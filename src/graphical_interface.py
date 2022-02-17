import pygame
from game import Game
from grid import AVAILABLE_LETTERS, Grid
from colors import WHITE

pygame.init()
pygame.font.init()

FONT = pygame.font.Font('freesansbold.ttf', 22)


class GraphicalInterface(Game):
    WIDTH, HEIGHT = (500, 700)

    def __init__(self):
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("WORDLE REDEEMED")
        self.target_word = self.generate_random_word()
        self.guesses_left = 6
        self.sharable_verdict = []
        self.grid = Grid()
        self.event_handler()

    def show_error_message(self, message):
        message_screen = FONT.render(message, False, (255, 0, 0))
        self.window.blit(message_screen, (90, 620))
        pygame.display.update()
        pygame.time.delay(500)

    def load_ending_screen(self, win=True):
        self.show_sharable_verdict()
        message = ("YOU WON!" if win else "YOU LOST!") + \
            f" THE WORD WAS: {self.target_word}"
        message_screen = FONT.render(message, False, (255, 0, 0))
        self.window.blit(message_screen, (65, 620))
        self.window.blit(FONT.render(
            "PRESS ANY KEY TO RESTART", False, (255, 191, 0)), (85, 80))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    pygame.time.delay(500)
                    new_game = GraphicalInterface()

    def render_graphics(self):
        self.window.fill(WHITE)
        self.grid.draw(self.window)
        pygame.display.update()

    def event_handler(self):
        print(f"TARGET WORD: {self.target_word}")
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.grid.backspace()
                    elif event.key == pygame.K_RETURN:
                        # This block will work as a word submission block from user
                        # based on the accuracy of the word, the game states and variables will change
                        # this is the main block which directly inherits from the terminal based implemention of the game
                        guessed_word = self.grid.retrieve_word()
                        if self.check_word_validity(guessed_word):
                            current_verdict = self.generate_verdict(
                                guessed_word)
                            self.grid.submit_word(current_verdict)
                            self.guesses_left -= 1
                        else:
                            """
                            Raise exception/show error message or screen
                            """
                            self.show_error_message(
                                "Incomplete or Invalid word!")
                            pass
                        if self.target_word == guessed_word:
                            """
                            Render ending screen and restart the game
                            """
                            self.render_graphics()
                            self.load_ending_screen()
                    else:
                        # Take letter input from user and handle errors
                        input_letter = event.key
                        self.grid.enter_letter(input_letter)

            if self.guesses_left == 0:
                """
                The player has lost
                Load the ending screen and restart the game                
                """
                self.render_graphics()
                self.load_ending_screen(False)

            self.render_graphics()
