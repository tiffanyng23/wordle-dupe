import pygame
import sys
import enchant 
import random
from wonderwords import RandomWord
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
red = 224, 70, 70

#font
font = pygame.font.Font(None, 48)

# box dimensions
box_width = 60
box_height = 60
box_shift = 70

#word dictionary
d = enchant.Dict("en_US")

#game logic
def GameLevel(level_num):
    '''returns title depicting game level'''
    level_surface = font.render(f"Level {level_num}", True, (0,0,0))
    level_rect = level_surface.get_rect(center=(width/2, height/12))
    screen.blit(level_surface, level_rect)

def SelectWord(num_letters):
    '''randomnly generates a word of a customizable length'''
    r = RandomWord()
    return r.word(word_min_length=num_letters, word_max_length=num_letters)

def CurrentAttempt(wordle, current_guess, all_guesses, guess_row):
    '''user can type guess and it will populate the boxes on display'''

    #always 6 guesses so rows will be 6, cols will depend on word length
    rows = 6
    cols = len(wordle) # length of word = num columns
    col_count = 0
    row_count = 0

    # loop through previous guesses
    for guess in all_guesses:

        guess = guess.upper()

        for letter in guess:
            #create surface of letter
            letter_surface = font.render(letter, True, (0,0,0))

            # get coordinates of the centre of each box
            # middle of display - half num of cols * box shift  + half of one box + shift based on col
            center_x = (width/2 - cols/2 * box_shift) + box_width/2 + (col_count * box_shift)
            center_y = (height/2 - rows/2 * box_shift) + box_height/2 + (row_count * box_shift)

            col_count += 1

            # use get rect to centre each letter_surface at the centre of each box 
            letter_rect = letter_surface.get_rect(center=(center_x, center_y))

            #blit letter
            screen.blit(letter_surface, letter_rect)
                
        col_count = 0 #reset column count to 0
        row_count += 1 #row count increase by 1

    # draw active guess
    current_guess = current_guess.upper()

    for letter in current_guess:
        #create surface of letter
        letter_surface = font.render(letter, True, (0,0,0))

        # get coordinates of the centre of each box
        # middle of display - half num of cols * box shift  + half of one box + shift based on col
        center_x = (width/2 - cols/2 * box_shift) + box_width/2 + (col_count * box_shift)
        center_y = (height/2 - rows/2 * box_shift) + box_height/2 + (guess_row * box_shift)

        col_count += 1

        # use get rect to centre each letter_surface at the centre of each box 
        letter_rect = letter_surface.get_rect(center=(center_x, center_y))

        #blit letter
        screen.blit(letter_surface, letter_rect)

def BoxColor(wordle, all_guesses):
    '''determine which letters in guess are green or yellow'''
    
    # store box colours
    box_colors = {}

    # go through each guess and each letter to determine box colour
    for guess in all_guesses:
        colors = [None] * len(guess) # create list to store colours for each guess
        remaining_letters = list(wordle) #convert wordle to a list of letters 

        for i, letter in enumerate(guess):
            # check each letter in each guess for green boxes
            if letter == wordle[i]:
                # store colour for letter
                colors[i] = green

                #remove from remaining letters
                remaining_letters[i] = None

        # check for yellow and beige boxes
        for i, letter in enumerate(guess):
            if colors[i] == green:
                continue
            
            # if letter is still in word
            if letter in remaining_letters:
                colors[i] = yellow
                # remove letter from remaining letters
                # get index of letter in remaining letters to remove it
                remaining_letters[remaining_letters.index(letter)] = None
            else:
                colors[i] = beige

        #update box_colors with colours for that guess
        box_colors[guess] = colors

    return box_colors

def DrawBoxes(num_rows, num_cols, all_guesses, current_guess, box_colors, valid_guess, border_width):
    '''draw boxes onto display'''
    # go through each box and apply the correct colour
    for row in range(num_rows):
        for col in range(num_cols):
            if row < len(all_guesses):
                guess = all_guesses[row]
            
                if col < len(box_colors[guess]):
                    final_color = box_colors[guess][col]
                else: # when level increases, column count increases
                    final_color = beige 
            else:
                #indicates rows that have no previous or active guesses yet
                final_color  = beige

            #draw boxes onto screen
            pygame.draw.rect(screen, final_color, 
                ((width/2 - num_cols/2 * box_shift) + (col * box_shift), 
                (height/2 - num_rows/2 * box_shift) + (row * box_shift), 
                box_width, box_height))
            
            #invalid word red border
            # if current guess isn't a valid word --> make boxes of that row have a red border
            # if its not a valid guess, the row number and all guesses will be the same
            # e.g. 3 legit words but 4th word is not legit --> len(all_guesses) = 3 and row index = 3
            if row == len(all_guesses) and len(current_guess) == num_cols and valid_guess == False:
                final_color = red
                pygame.draw.rect(screen, red, 
                    ((width/2 - num_cols/2 * box_shift) + (col * box_shift), 
                    (height/2 - num_rows/2 * box_shift) + (row * box_shift), 
                    box_width, box_height), border_width)
      
def GameStatus(current_guess, all_guesses, wordle):
    '''determine users game status'''
    if current_guess == wordle:
        return "win"
    elif len(all_guesses) == 6:
        return "lose"
    else:
        return "progress"

def WordleAnswer(wordle):
    '''displays answer if user cannot get the wordle'''

    #create surface of wordle text
    wordle = wordle.upper()
    wordle_surface = font.render(wordle, True, (0,0,0))

    # get coordinates of the centre of popup box
    center_x = width/2
    center_y = height/2

    #get rect to get rectangular coordinates
    wordle_rect = wordle_surface.get_rect(center=(center_x, center_y))

    #blit word
    screen.fill(lavender)
    screen.blit(wordle_surface, wordle_rect)

if __name__ == "__main__":
    wordle = SelectWord(5)
    print(wordle)