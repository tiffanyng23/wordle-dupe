import enchant 
import pygame
from wonderwords import RandomWord
from constants import LAVENDER, BEIGE, GREEN, YELLOW, RED, BOX_HEIGHT, BOX_SHIFT, BOX_WIDTH, WIDTH, HEIGHT, BORDER_WIDTH, ROWS

#word dictionary
dictionary = enchant.Dict("en_US")

#game logic
class Wordle:
    def __init__(self):
        #variables at the start of the game
        self.wordle_length = 5
        self.current_guess = ""
        self.all_guesses = []
        self.status = "progress"
        self.valid_guess = True
        self.level = 1
        self.win_time = None

        # generate random word and store in variable
        self.wordle = self.select_word()

    def select_word(self):
        '''randomnly generates a word of a customizable length'''
        r = RandomWord()
        return r.word(word_min_length=self.wordle_length, word_max_length=self.wordle_length)

    def current_attempt(self, screen, font):
        '''user can type guess and it will populate the boxes on display'''

        #always 6 guesses so rows will be 6, cols will depend on word length
        cols = len(self.wordle) # length of current wordle = num columns
        col_count = 0
        row_count = 0

        # loop through previous guesses
        for guess in self.all_guesses:

            guess = guess.upper()

            for letter in guess:
                #create surface of letter
                letter_surface = font.render(letter, True, (0,0,0))

                # get coordinates of the centre of each box
                # middle of display - half num of cols * box shift  + half of one box + shift based on col
                center_x = (WIDTH/2 - cols/2 * BOX_SHIFT) + BOX_WIDTH/2 + (col_count * BOX_SHIFT)
                center_y = (HEIGHT/2 - ROWS/2 * BOX_SHIFT) + BOX_HEIGHT/2 + (row_count * BOX_SHIFT)

                col_count += 1

                # use get rect to centre each letter_surface at the centre of each box 
                letter_rect = letter_surface.get_rect(center=(center_x, center_y))

                #blit letter
                screen.blit(letter_surface, letter_rect)
                    
            col_count = 0 #reset column count to 0
            row_count += 1 #row count increase by 1

        # draw active guess
        active_guess = self.current_guess.upper()

        for letter in active_guess:
            #create surface of letter
            letter_surface = font.render(letter, True, (0,0,0))

            # get coordinates of the centre of each box
            # middle of display - half num of cols * box shift  + half of one box + shift based on col
            center_x = (WIDTH/2 - cols/2 * BOX_SHIFT) + BOX_WIDTH/2 + (col_count * BOX_SHIFT)
            center_y = (HEIGHT/2 - ROWS/2 * BOX_SHIFT) + BOX_HEIGHT/2 + (len(self.all_guesses) * BOX_SHIFT)

            col_count += 1

            # use get rect to centre each letter_surface at the centre of each box 
            letter_rect = letter_surface.get_rect(center=(center_x, center_y))

            #blit letter
            screen.blit(letter_surface, letter_rect)

    def box_fill(self):
        '''determine which letters in guess are green or yellow'''
        
        # store box colours
        box_colors = []

        # go through each guess and each letter to determine box colour
        for guess in self.all_guesses:
            # length of colour list will be the same as word length of guess 
            # create list to store colours for each letter in the guess, then add this list into the box_colors
            colors = [None] * len(guess) 
            remaining_letters = list(self.wordle) #convert wordle to a list of letters 

            # check each letter in each guess against each letter in wordle
            for i, letter in enumerate(guess):
                # correct letter in correct spot
                if letter == self.wordle[i]:
                    # store colour for letter
                    colors[i] = GREEN

                    #remove from remaining letters
                    remaining_letters[i] = None

            # check for yellow and beige boxes
            for i, letter in enumerate(guess):
                if colors[i] == GREEN:
                    continue
                
                # if letter is still in word
                if letter in remaining_letters:
                    colors[i] = YELLOW
                    # remove letter from remaining letters
                    # get index of letter in remaining letters to remove it
                    remaining_letters[remaining_letters.index(letter)] = None
                else:
                    colors[i] = BEIGE

            #update box_colors with colour for that letter guess
            box_colors.append(colors)

        return box_colors

    def draw_boxes(self, screen, box_colors):
        '''draw boxes onto display'''
        num_cols = len(self.wordle)
        # go through each box and apply the correct colour
        for row in range(ROWS):
            for col in range(num_cols):
                if row < len(self.all_guesses):
                    guess = self.all_guesses[row]
                    final_color = box_colors[row][col]
                else:
                    #indicates rows that have no previous or active guesses yet
                    final_color  = BEIGE

                #draw boxes onto screen
                pygame.draw.rect(screen, final_color, 
                    ((WIDTH/2 - num_cols/2 * BOX_SHIFT) + (col * BOX_SHIFT), 
                    (HEIGHT/2 - ROWS/2 * BOX_SHIFT) + (row * BOX_SHIFT), 
                    BOX_WIDTH, BOX_HEIGHT))
                
                #invalid word red border
                # if current guess isn't a valid word --> make boxes of that row have a red border
                # if its not a valid guess, the row number and all guesses will be the same
                # e.g. 3 legit words but 4th word is not legit --> len(all_guesses) = 3 and row index = 3
                if row == len(self.all_guesses) and len(self.current_guess) == num_cols and self.valid_guess == False:
                    final_color = RED
                    pygame.draw.rect(screen, RED, 
                        ((WIDTH/2 - num_cols/2 * BOX_SHIFT) + (col * BOX_SHIFT), 
                        (HEIGHT/2 - ROWS/2 * BOX_SHIFT) + (row * BOX_SHIFT), 
                        BOX_WIDTH, BOX_HEIGHT), BORDER_WIDTH)
    
    def game_level(self, screen, font):
        '''returns title depicting game level'''
        level_surface = font.render(f"Level {self.level}", True, (0,0,0))
        level_rect = level_surface.get_rect(center=(WIDTH/2, HEIGHT/12))
        screen.blit(level_surface, level_rect)
        
    def game_status(self):
        '''determine users game status based on each current and complete guess'''
        if self.current_guess == self.wordle:
            # start timer to show wordle for 2000ms
            self.win_time = pygame.time.get_ticks()
            self.status = "win"
        elif len(self.all_guesses) == 6:
            self.status = "lose"
        else:
            self.status = "progress"
            

    def next_level(self):
        '''configure variables for the next level'''
        #reset guess variables
        self.all_guesses = []
        self.current_guess = ""
        self.valid_guess = True

        # increase difficulty
        self.level += 1
        self.wordle_length += 1

        # generate new wordle 
        self.wordle = self.select_word()

        #reset status
        self.status = "progress"

    def wordle_answer(self, screen, font):
        '''displays answer if user cannot get the wordle'''

        #create surface of wordle text
        answer = self.wordle.upper()
        wordle_surface = font.render(answer, True, (0,0,0))

        # get coordinates of the centre of popup box
        center_x = WIDTH/2
        center_y = HEIGHT/2

        #get rect to get rectangular coordinates
        wordle_rect = wordle_surface.get_rect(center=(center_x, center_y))

        #blit word
        screen.fill(LAVENDER)
        screen.blit(wordle_surface, wordle_rect)
