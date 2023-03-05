"""
This module implements all the game functionalities and logics
and this is independent of any GUI implementation
"""

import random
from word_loader import fetch_words, fetch_additional_words

WORDS, ADDITIONAL_WORDS = fetch_words(), fetch_additional_words()

VERDICT_HASH = {"g": "🟩", "b": "⬜", "y": "🟨"}
COLOR_HASH = {"🟩": "g", "⬜": "b", "🟨": "y"}


class Game:
    def __init__(self):
        self.target_word = self.generate_random_word()
        self.guesses_left = 6
        self.sharable_verdict = []
        self.event_handler()
        print(f"THE WORD WAS: {self.target_word}")
        self.show_sharable_verdict()

    def show_sharable_verdict(self):
        print("\n###########################################\nSHARE WITH FRIENDS!\n###########################################\n")
        for verdict in self.sharable_verdict:
            for letter in verdict:
                print(VERDICT_HASH[letter], end="")
            print()
        print("\n###########################################\n")

    def generate_random_word(self):
        return random.choice(WORDS)

    def event_handler(self):
        print(
            f"######################\nOUR TARGET WORD IS: {self.target_word}\n######################\n\n")
        while self.guesses_left > 0:
            """
            Use try except block to seperately handle 
            terminal based input and GUI based input
            """
            guessed_word = self.input_next_guess()  # terminal based input
            if self.check_word_validity(guessed_word):
                self.guesses_left -= 1
                print(f"TARGET WORD    : {self.target_word}")
                print(f"GUESSED WORD   : {guessed_word}")
                current_verdict = self.generate_verdict(guessed_word)
                self.display_verdict(current_verdict)
            else:
                print("!!! Invalid word/Outside our word list !!!")
            if guessed_word == self.target_word:
                print(f"YOU WON THE GAME!", end=" ")
                return

        print("YOU LOST THE GAME!", end=" ")

    # this function will be called when playing on the terminal
    def input_next_guess(self):
        """
        When connected to the GUI, it will take input directly from pygame window
        """
        next_guess = input(
            f"Guesses left: {self.guesses_left}\nEnter a Guess: ").upper()
        return next_guess

    def check_word_validity(self, guessed_word):
        return guessed_word in WORDS or guessed_word in ADDITIONAL_WORDS

    def generate_verdict(self, guessed_word):
        target_word_copy = [letter for letter in self.target_word]
        verdict = ['b' for i in range(5)]

        # first list out the correct letters in the correct spot
        for i in range(5):
            if target_word_copy[i] == guessed_word[i]:
                target_word_copy[i] = "*"
                verdict[i] = "g"

        # check for letters in the incorrect spots
        for i in range(5):  # outer loop for the guessed word
            if verdict[i] != "b":  # skip this letter if it's already in correct spot
                continue
            for j in range(5):  # inner loop for the target word
                if i == j or target_word_copy[j] == "*":
                    continue
                if guessed_word[i] == target_word_copy[j]:
                    target_word_copy[j] = "*"
                    verdict[i] = "y"
                    break
        self.sharable_verdict.append(verdict)
        return verdict

    def display_verdict(self, verdict):
        print("VERDICT        : ", end="")
        for letter in verdict:
            print(letter.upper(), end="")
        print()
        print("COLORED VERDICT: ", end="")
        for c in verdict:
            print(VERDICT_HASH[c], end="")
        print()


"""
Primarily test the game functionalities here
"""

# game = Game()
