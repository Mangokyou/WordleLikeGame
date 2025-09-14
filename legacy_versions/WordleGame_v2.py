from string import ascii_uppercase

import pygame
from random import choice
from sys import exit

pygame.init()
pygame.display.set_caption("Wordle Game")


width = 640
height = 1000

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
letter_font = pygame.font.Font("letter_font.otf", 40) # Font for the letters inside the guess boxes
other_font = pygame.font.Font("letter_font.otf", 25) # Font for the other letters

with open("english_words.txt", "r") as f: # can use other word files for input
    words = f.read().split()
with open("english_words_valid.txt", "r") as f:
    valid = f.read().split()

letters = {} # to keep track of already used letters
boxes = [] # to generate and update guess boxes
current_row = 0 # to iterate through the boxes
current_col = 0
current_guess = [0,0,0,0,0] # needed to validate guess
finish =  False # To keep track if the game state
word = choice(words).upper() # choose a random word from the word list

class Boxes: # class for the guess boxes
    def __init__(self,x, y, color, letter = None):
        self.x = x
        self.y = y
        self.color = color
        self.letter = letter


    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 80, 80,), width=0, border_radius=3)
        pygame.draw.rect(screen, "#c1cad4", (self.x, self.y, 80, 80,), width=3, border_radius=3)
        if self.letter is not None:
            text_surface = letter_font.render(self.letter, True, "White")
            text_rect = text_surface.get_rect(centerx=self.x+40, centery=self.y+40)
            screen.blit(text_surface, text_rect)


class Letter: # class for the letter boxes
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.letter = letter
        self.color = "#cfcaae"

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50,), width=0, border_radius=3)
        pygame.draw.rect(screen, "#403e3c", (self.x, self.y, 50, 50,), width=3, border_radius=2)
        text_surface = other_font.render(self.letter, True, "White")
        text_rect = text_surface.get_rect(centerx=self.x + 25, centery=self.y + 25)
        screen.blit(text_surface, text_rect)


def create_boxes(): # function to create guess boxes
    for i in range(6):
        temp = []
        for j in range(5):
            temp.append(Boxes(100+j*90, 150+i*90, "#1a1b1c"))
        boxes.append(temp)

def create_letter(): # function to create letter boxes
    possible = ascii_uppercase + " "
    count = 0
    for i in range(3):
        for j in range(9):
            letters[possible[count]] = Letter(55+j*60, 750+i*60, possible[count])
            count += 1
    del letters[" "]


create_boxes()
create_letter()

def guess(current): # check if the guessed word has the right parameters
        guessed = "".join(current)
        if guessed.lower() not in valid:
            print("Wrong")
        else:
            print("Correct")


def checker(correct, guessed): # compare guessed word to correct word
    guessed = "".join(guessed)
    explored = ""
    for i in range(0,5): #small loop to give every letter and box the right color while comparing
        if guessed[i] == word[i]:
            boxes[current_col][i].color = "Green"
            letters[guessed[i]].color = "Green"
            explored += guessed[i]
        elif guessed[i] in word and word.count(guessed[i]) > explored.count(guessed[i]):
            case = True
            for j in range(0,5):
                if guessed[j] == guessed[i] and j != i and guessed[j] == word[j]:
                    case = False
            if case:
                boxes[current_col][i].color = "Orange"
                if letters[guessed[i]].color != "Green":
                    letters[guessed[i]].color = "Orange"
                    explored += guessed[i]
                else:
                    boxes[current_col][i].color = "Red"
                    letters[guessed[i]].color = "Red"
                    explored += guessed[i]

        else:
            boxes[current_col][i].color = "Red"
            letters[guessed[i]].color = "Red"
            explored += guessed[i]

    if guessed == correct: # True if guessed word is correct
        return True
    else:
        return False

def finished(): # displays correct word when game is finished
    text_surface = other_font.render(word, True, "White")
    text_rect = text_surface.get_rect(centerx=width/2, centery=100)
    box_rect = text_rect.inflate(20,20)
    pygame.draw.rect(screen, "#787571", box_rect, width=0, border_radius=3)
    screen.blit(text_surface, text_rect)

while True: #main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha() and len(event.unicode) == 1 and not finish: # to get user input while guessing
                boxes[current_col][current_row].letter = event.unicode.upper()
                current_guess[current_row] = event.unicode.upper()
                if current_row < 4:
                    current_row += 1


            if event.unicode == "0": # to restart the game
                letters = {}
                boxes = []
                current_row = 0
                current_col = 0
                current_guess = [0, 0, 0, 0, 0]
                finish = False
                word = choice(words).upper()
                create_letter()
                create_boxes()


            if event.key == pygame.K_BACKSPACE: # call the guess function
                if current_row > 0 and current_guess[current_row] == 0:
                    current_row -= 1
                boxes[current_col][current_row].letter = None
                current_guess[current_row] = 0
                #print(current_guess)

            if event.key == pygame.K_RETURN and current_guess[current_row] != 0: # call the check function
                if guess(current_guess):
                    if checker(word, current_guess) or current_col == 5:
                        finish = True
                    current_col += 1
                    current_row = 0
                    current_guess = [0,0,0,0,0]




    screen.fill("#1a1b1c")

    restart = other_font.render("0 to restart", True, "White")
    restart_rect = restart.get_rect(centerx=100, centery=90)
    screen.blit(restart, restart_rect)

    enter = other_font.render("Enter to guess", True, "White")
    enter_rect = restart.get_rect(centerx=100, centery=60)
    screen.blit(enter, enter_rect)

    delete = other_font.render("Backspace to delete", True, "White")
    delete_rect = restart.get_rect(centerx=100, centery=30)
    screen.blit(delete, delete_rect)

    for row in boxes: # draws every guess box
        for box in row:
            box.draw()

    for key in letters: # draws every letter
        letters[key].draw()

    if finish:
        finished()


    pygame.display.update()
    clock.tick(60)