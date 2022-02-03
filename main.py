import pygame
import random
import string
from words import words
from words2 import five_letter_words
from cell import Cell

pygame.font.init()

font = pygame.font.Font('freesansbold.ttf', 22)


WORDS = [w.upper() for w in words]
print(len(WORDS))

WIDTH, HEIGHT = 500, 700

GREEN, YELLOW, GREY, BLACK, WHITE = (
    107, 241, 83), (228, 208, 10), (163, 163, 157), (0, 0, 0), (255, 255, 255)
AVAILABLE_LETTERS = [letter for letter in string.ascii_uppercase]


def draw(window, grid):
    window.fill((255, 255, 255))
    for row in grid:
        for cell in row:
            cell.draw(window)
    pygame.display.update()


def select_random_word():
    return random.choice(WORDS)


def show_error_message(window, error_message):
    message_screen = font.render(error_message, False, (255, 0, 0))
    window.blit(message_screen, (90, 620))
    pygame.display.update()
    pygame.time.delay(700)


def show_ending_scene(window, word, won):
    message = f"Congratulations! the word was {word}" if won else f"!!!You lost!!! the ward was {word}"
    message_screen = font.render(message, False, (255, 0, 0))
    window.blit(message_screen, (50, 620))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
            if event.type == pygame.KEYDOWN:
                pygame.time.delay(100)
                main()


def get_word_from_current_row(grid, row):
    word = ""
    for cell in grid[row]:
        word += cell.get_letter()
    return word


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SWORDLE")

    grid = [[Cell(i, j) for j in range(5)] for i in range(6)]

    run = True

    target_word = select_random_word()
    dummy_word = None
    dummy_verdict = False
    print(target_word)
    row, column = (0, 0)
    while run:
        if dummy_word is not None:
            print("Hello")
            show_ending_scene(window, target_word, dummy_verdict)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                print(column)
                if event.key == pygame.K_BACKSPACE:
                    if column > 0:
                        if grid[row][column].get_letter() != None:
                            grid[row][column].cancel_letter()
                        else:
                            grid[row][column - 1].cancel_letter()
                            column -= 1
                elif event.key == pygame.K_RETURN:
                    try:
                        current_word = get_word_from_current_row(grid, row)
                        row_verdict = []
                        for i in range(5):
                            if target_word[i] == current_word[i]:
                                row_verdict.append(GREEN)
                            elif current_word[i] in target_word:
                                row_verdict.append(YELLOW)
                            else:
                                row_verdict.append(GREY)
                    except:
                        show_error_message(
                            window, "Write a valid five letter word!")
                        print("Write a valid five letter word!")

                    if column == 4 and grid[row][column].get_letter() != None:
                        for c in range(5):
                            grid[row][c].processed = True
                            grid[row][c].set_color(row_verdict[c])
                        if current_word not in WORDS:
                            show_error_message(window, "NOT IN OUR WORD LIST!")
                            for col in range(5):
                                grid[row][col].set_color(None)
                                grid[row][col].processed = False
                        else:
                            row += 1
                            column = 0
                    try:
                        if current_word == target_word:
                            dummy_word = target_word
                            dummy_verdict = True
                        if row > 5:
                            dummy_word = current_word
                            dummy_verdict = False
                    except:
                        show_error_message(
                            window, "Write a valid five letter word!")

                else:
                    letter = event.key
                    try:
                        if chr(letter).upper() not in AVAILABLE_LETTERS:
                            error_message = "Enter a valid English Alphabet"
                            show_error_message(window, error_message)
                            raise Exception(error_message)
                        # print(chr(letter).upper())
                        if grid[row][column].get_letter() == None:
                            grid[row][column].assign_letter(
                                chr(letter).upper())

                        if column < 4:
                            column += 1
                        else:
                            pass
                    except Exception as e:
                        if (str(e) == "list index out of range"):
                            run = False
                            pygame.quit()
                        print(e)

        draw(window, grid)


if __name__ == "__main__":
    main()
