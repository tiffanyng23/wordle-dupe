import pygame
import sys
import enchant 
import random
from wonderwords import RandomWord
from constants import LAVENDER, BEIGE, GREEN, YELLOW, RED, BOX_HEIGHT, BOX_SHIFT, BOX_WIDTH, SIZE, WIDTH, HEIGHT, BORDER_WIDTH, ROWS
from wordle import dictionary, Wordle

pygame.init() 

#screen specs
screen = pygame.display.set_mode(SIZE)
title = pygame.display.set_caption("Wordle Dupe")
font = pygame.font.Font(None, 48)

# create instance of game
game = Wordle()
num_guesses = len(game.all_guesses)
status = game.status

#game loop
def main():
    run = True
    while run:
        # game events
        for event in pygame.event.get():
            # exit game
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            # enter guess
            if event.type == pygame.KEYDOWN and len(game.all_guesses) < ROWS:
                if event.key == pygame.K_BACKSPACE:
                    game.current_guess = game.current_guess[:-1]
                # user submits the guess by clicking enter
                elif event.key == pygame.K_RETURN:
                    #only assess guess upon clicking enter if it is the same length as the wordle
                    if len(game.current_guess) == len(game.wordle):
                        #check if guess is a legit word
                        # will return as True if legit and False if not --> update valid_guess
                        game.valid_guess = dictionary.check(game.current_guess)
                        if game.valid_guess == True:
                            game.all_guesses.append(game.current_guess)
                            #compare guess with wordle for each valid guess
                            game.game_status()
                            #reset current guess
                            game.current_guess = ""
                        else:
                            border_width = 5
                else:
                    if len(game.current_guess) < len(game.wordle):
                        game.valid_guess = True # as guess is being typed out it alwaysremains valid
                        game.current_guess += event.unicode

        # background colour
        screen.fill(LAVENDER)

        # display game level
        game.game_level(screen, font)

        # assess box colour
        box_colors = game.box_fill()

        # draw boxes
        game.draw_boxes(screen, box_colors)

        # draw letter in box
        game.current_attempt(screen, font)

        # if user gets correct answer, move to next level
        if game.status == "win": 
            if game.level < 4:
                #display screen with correct answer for 2 seconds then display next level
                if pygame.time.get_ticks() - game.win_time >= 2000:
                    game.next_level()
        
        #display answer if user lost
        if game.status == "lose":
            pygame.time.delay(1000)
            game.wordle_answer(screen, font)

        pygame.display.flip()

if  __name__ == "__main__":
    main()



