import pygame
from random import choice
from sys import exit

# Set Up Pygame
pygame.init()
pygame.display.set_caption("Wordle Game")
clock = pygame.time.Clock()

# Set Up Display
width =  600
height = 900
screen = pygame.display.set_mode((width, height))

# Variables
possible_guesses = "english_words_valid.txt" # Change the variable to use other languages
with open("english_words_valid.txt", "r") as f:
    valid = f.read().split()

possible_words = "english_words.txt" # Subset of english_words_valid which only includes very common words
with open("english_words.txt", "r") as f:
    words = f.read().split()


boxes = []
letter_boxes = {}

boxes_font = pygame.font.Font("letter_font.otf", 40) # Font for the 6 rows of boxes
letter_font = pygame.font.Font("letter_font.otf", 25) # Font for the different letter_boxes

current_row = 0 # To put user typed letters in the right box
current_col = 0
current_guess = [0,0,0,0,0] # Keeps track of the users current guess
game_over = False  # Current Game state
word = choice(words).upper() # Chooses the random word for the current round


# Colors
background_color = "#1a1b1c" # Color for the guess boxes
letter_box_color = "#eeeee4" # Color for the letter boxes

# Classes

class Boxes:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = background_color
        self.letter = ""

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 70, 70,), width=0, border_radius=2)
        if self.color == background_color:
            pygame.draw.rect(screen, "#c1cad4", (self.x, self.y, 70, 70,), width=3, border_radius=2)

        text_surface = boxes_font.render(self.letter, True, "White")
        text_rect = text_surface.get_rect(centerx=self.x +35, centery=self.y + 35)
        screen.blit(text_surface, text_rect)


    def reset(self):
        self.color = background_color
        self.letter = ""

class LetterBoxes:
    def __init__(self, x, y, letter, length):
        self.x = x
        self.y = y
        self.color = letter_box_color
        self.letter = letter
        self.length = length

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, 55), width=0, border_radius=2)
        text_surface = letter_font.render(self.letter, True, "Black")
        if self.letter not in ["Enter", "Back"]:
            text_rect = text_surface.get_rect(centerx=self.x + 23, centery=self.y + 28)
        else:
            text_rect = text_surface.get_rect(centerx=self.x + 35, centery=self.y + 28)
        screen.blit(text_surface, text_rect)

    def reset(self):
        self.color = letter_box_color


def create_boxes(): # Create the initial set of guess boxes
    x_offset = 100
    y_start = 150
    y_step = 80
    for i in range(6):
        temp = []
        for j in range(5):
            temp.append(Boxes(x_offset + j*80,  y_start + i*y_step))
        boxes.append(temp)


def create_letter_boxes(): # Create the initial set of letter boxes
    letters = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O","P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Enter", "Z", "X", "C", "V", "B", "N", "M","Back"]
    ]
    x_offset = [50,75,50]
    y_start = 700
    y_step = 60

    for row_index, row in enumerate(letters):
        for col_index, letter in enumerate(row):
            x = x_offset[row_index] + col_index*50
            y = y_start + row_index * y_step
            if letter in ("Enter", "Back"):
                x_offset[2] += 25
                length = 70
            else:
                length = 45

            letter_boxes[letter] = LetterBoxes(x, y, letter, length)

def add_letter(letter): # Adds user inputted letter to the current guess
    global game_over, current_guess, current_row, current_col
    boxes[current_row][current_col].letter = letter.upper()
    current_guess[current_col] = letter.upper()
    if current_col < 4:
        current_col += 1

def del_letter(): # Deletes the last inputted letter
    global game_over, current_guess, current_row, current_col
    if current_col > 0 and current_guess[current_col] == 0:
        current_col -= 1
    boxes[current_row][current_col].letter = ""
    current_guess[current_col] = 0

def click_letter(x1, x2): # Checks if a letter was clicked
    for letter in letter_boxes:
        if x1 in range(letter_boxes[letter].x, letter_boxes[letter].x + letter_boxes[letter].length):
            if x2 in range(letter_boxes[letter].y, letter_boxes[letter].y + 55):
                if letter_boxes[letter].letter == "Back":
                    del_letter()
                elif letter_boxes[letter].letter == "Enter":
                    guess(current_guess)
                else:
                    add_letter(letter)

def guess(current): # check if the guessed word has the right parameters
    if 0 not in current:
        guessed = "".join(current)
        if guessed.lower() in valid:
            checker(word, guessed)

def checker(correct, guess): # Compares guessed word to correct word and gives appropriate output
    global current_row, current_guess, current_col
    explored = ""
    for index, letter in enumerate(guess):
        if letter == correct[index]:
            boxes[current_row][index].color = "Green"
            explored += letter
            letter_boxes[letter].color = "Green"
        elif letter in correct and correct.count(letter) > explored.count(letter):
            case = True
            for j, other_letter in enumerate(guess):
                if other_letter == letter and index != j and letter == correct[j]:
                    case = False

            if case:
                letter_boxes[letter].color = "Orange"
                boxes[current_row][index].color = "Orange"
                explored += letter
            else:
                if letter_boxes[letter].color != "Green":
                    letter_boxes[letter].color = "Orange"
                boxes[current_row][index].color = "Red"
                explored += letter
        else:
            letter_boxes[letter].color = "Red"
            boxes[current_row][index].color = "Red"


    current_guess = [0,0,0,0,0]
    if current_row <= 5:
        current_row += 1
        current_col = 0

    if guess == correct or current_row == 6:
        global game_over
        game_over = True

def finished(): # Displays correct word when game is finished
    text_surface = boxes_font.render(word, True, "White")
    text_rect = text_surface.get_rect(centerx=width / 2, centery=75)
    box_rect = text_rect.inflate(20, 20)
    pygame.draw.rect(screen, "#787571", box_rect, width=0, border_radius=4)
    screen.blit(text_surface, text_rect)
    restart = letter_font.render("R to restart", True, "White")
    restart_rect = restart.get_rect(centerx=75, centery=30)
    screen.blit(restart, restart_rect)

create_boxes()
create_letter_boxes()

while True: #main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            print(word)
            if event.unicode.isalpha() and len(event.unicode) == 1 and not game_over:
                add_letter(event.unicode)
            if event.key == pygame.K_BACKSPACE and not game_over:
                del_letter()
            if event.key == pygame.K_RETURN and not game_over:
                guess(current_guess)
            if event.key == pygame.K_r and game_over:
                current_row = 0
                current_col = 0
                current_guess = [0, 0, 0, 0, 0]
                game_over = False
                word = choice(words).upper()
                for letter in letter_boxes:
                    letter_boxes[letter].reset()
                for row in boxes:
                    for box in row:
                        box.reset()


        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse1, mouse2 = pygame.mouse.get_pos()
            click_letter(mouse1, mouse2)

    screen.fill(background_color)

    for row in boxes:
        for box in row:
            box.draw()

    for letter in letter_boxes:
        letter_boxes[letter].draw()

    if game_over:
        finished()

    pygame.display.update()
    clock.tick(60)