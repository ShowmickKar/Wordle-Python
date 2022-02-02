import pygame
import random

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 40)

GREEN, YELLOW, GREY, BLACK, WHITE = (
    107, 241, 83), (228, 208, 10), (163, 163, 157), (0, 0, 0), (255, 255, 255)


class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.__color = None
        self.__assigned_letter = None
        self.x = (column + 1) * 80 - 20
        self.y = (row + 1) * 80 + 50
        self.size = 70
        self.processed = False

    def get_letter(self):
        return self.__assigned_letter

    def assign_letter(self, letter):
        self.__assigned_letter = letter

    def cancel_letter(self):
        self.__assigned_letter = None

    def set_color(self, color):
        self.__color = color

    def draw(self, window):
        color = self.__color if self.processed else GREY
        pygame.draw.rect(window, color, (self.x,
                                         self.y, self.size, self.size))
        if self.__color == None:
            pygame.draw.rect(window, WHITE, (self.x + 2,
                                             self.y + 2, self.size - 4, self.size - 4))
        if self.__assigned_letter != None:
            text_color = BLACK if self.__color == None else WHITE
            # display the letter on that box
            # print("Breakpoint" + self.__assigned_letter)
            text = font.render(self.__assigned_letter, False, text_color)
            # print(type(text))
            window.blit(text, (self.x + 20, self.y + 19))
