"""
Implements a 2D 5x6 Grid like Data Structure that holds the necessary information needed for the game
"""

import pygame
from colors import GREEN, YELLOW, GREY, BLACK, WHITE
import string

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 40)

AVAILABLE_LETTERS = [letter for letter in string.ascii_uppercase]

"""
Implement a Grid class to add one more layer of abstraction
"""


class Grid:
    def __init__(self):
        self.matrix = [[Cell(i, j) for j in range(5)] for i in range(6)]
        self.current_row, self.current_column = 0, 0

    def enter_letter(self, letter):
        letter = chr(letter).upper()
        print(f"Request to enter letter: {letter}....")
        if letter in AVAILABLE_LETTERS:
            if self.current_column == 5:  # user has already entered 5 letters
                print("Sorry Request cannot be processed")
                return
            self.matrix[self.current_row][self.current_column].assign_letter(
                letter)
            self.current_column += 1

    def backspace(self):
        """
        !!! This method is not functioning. NEEDS DEBUGGING !!!
        """
        # Checks call for valid backspace operation at removes letter from cell
        print(f"REQUESTING A BACKSPACEs....")
        if self.current_column < 1:
            return
        if self.matrix[self.current_row][self.current_column - 1].get_letter() != None:
            self.matrix[self.current_row][self.current_column -
                                          1].remove_letter()
            if self.current_column > 0:
                self.current_column -= 1

    def retrieve_word(self):
        word = ""
        for cell in self.matrix[self.current_row]:
            try:
                word += cell.get_letter()
            except:
                return word
        return word

    def submit_word(self, verdict):
        hash = {"g": GREEN, "b": GREY, "y": YELLOW}
        for j, cell in enumerate(self.matrix[self.current_row]):
            cell.process_associated_row(hash[verdict[j]])
        self.current_row += 1
        self.current_column = 0

    def draw(self, window):
        for row in self.matrix:
            for cell in row:
                cell.draw(window)


class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.__assigned_letter = None
        self.__background_color = None
        self.x = (column + 1) * 80 - 20
        self.y = (row + 1) * 80 + 50
        self.size = 70

        # keeps track of whether the user is done with the row yet
        self.__processed_row = False

    def get_letter(self):
        return self.__assigned_letter

    def assign_letter(self, letter):  # assign the block a letter upon user input
        self.__assigned_letter = letter

    def remove_letter(self):  # removes the letter from the cell if the user presses backspace
        self.__assigned_letter = None

    def process_associated_row(self, verdict_color):
        self.__processed_row = True
        self.__background_color = verdict_color

    def draw(self, window):
        background_color = self.__background_color if self.__processed_row else GREY
        pygame.draw.rect(window, background_color,
                         (self.x, self.y, self.size, self.size))

        # if the associated row isn't processed yet, the cell should be white colored with grey borders
        if not self.__processed_row:
            pygame.draw.rect(window, WHITE, (self.x + 2, self.y +
                                             2, self.size - 4, self.size - 4))
        # display the letter on the cell
        # if the row is yet to be processed, meaning the user is currently
        # guessing on the associated row the text color should be black and white otherwise
        if self.__assigned_letter != None:
            text_color = BLACK if not self.__processed_row else WHITE
            text = font.render(self.__assigned_letter, False, text_color)
            window.blit(text, (self.x + 20, self.y + 19))
