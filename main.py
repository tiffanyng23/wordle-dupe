import pygame
import sys
import enchant 
import random
from wonderwords import RandomWord
from wordle import SelectWord, CurrentAttempt, BoxColor, DrawBoxes, GameStatus, WordleAnswer
pygame.init() #starts the pygame systems

#screen specs
size = width, height = 600, 600
# creates window where everything is drawn
screen = pygame.display.set_mode(size)
#game title
title = pygame.display.set_caption("Wordle Dupe")

#colour scheme
lavender = 181, 163, 207
beige = 232, 230, 216
green = 173, 217, 173
yellow = 247, 239, 163
red = 196, 96, 96

#font
font = pygame.font.Font(None, 48)

# box dimensions
box_width = 60
box_height = 60
box_shift = 70

# format to display boxes
cols = 5
rows = 6

#word dictionary
d = enchant.Dict("en_US")

#game loop
def main():
    # variables
    current_guess = ""
    guesses = []
    status = "progress"
    valid_guess = True
    border_width = 0
    wordle_length = 5

    # generate random word
    wordle = SelectWord(wordle_length)

    run = True
    while run:
        # game events
        for event in pygame.event.get():
            # exit game
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            # enter guess
            if event.type == pygame.KEYDOWN and len(guesses) < 6 and status == "progress":
                if event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]
                elif event.key == pygame.K_RETURN:
                    #add user_text to guesses list and clear variable
                    if len(current_guess) == 5:
                        #check if guess is a legit word 
                        valid_guess = d.check(current_guess)
                        if valid_guess == True:
                            guesses.append(current_guess)
                            #check game status by comparing guess with wordle
                            status = GameStatus(current_guess, guesses, wordle)
                            #reset current guess
                            current_guess = ""
                        else:
                            border_width = 5
                else:
                    if len(current_guess) < 5:
                        valid_guess = True # as guess is being typed out it remains valid
                        current_guess += event.unicode

        # background colour
        screen.fill(lavender)

        # assess box colour
        box_colors = BoxColor(wordle, guesses)

        # draw boxes
        DrawBoxes(rows, cols, guesses, current_guess, box_colors, valid_guess, border_width)

        # draw letter in box
        CurrentAttempt(wordle, current_guess, guesses, len(guesses))

        #display answer if user lost
        if status == "lose":
            pygame.time.delay(1000)
            WordleAnswer(wordle)

        pygame.display.flip()

if  __name__ == "__main__":
    main()



