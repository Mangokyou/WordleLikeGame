import pygame
from random import choice
from sys import exit

pygame.init()
pygame.display.set_caption("Wordle Game")
screen = pygame.display.set_mode((640, 1000))


clock = pygame.time.Clock()
letter_font = pygame.font.Font("letter_font.otf", 40)

boxes = []
current_row = 0
current_col = 0
current_guess = [0,0,0,0,0]
finish = False

with open("english_words.txt", "r") as f:
    words = f.read().split()

with open("english_words_valid.txt", "r") as f:
    valid = f.read().split()

word = choice(words).upper()

class Boxes:
    def __init__(self,x, y, color, letter = None):
        self.x = x
        self.y = y
        self.color = color
        self.letter = letter


    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 80, 80,))
        pygame.draw.rect(screen, "#c1cad4", (self.x, self.y, 80, 80,), width=3)
        if self.letter is not None:
            text_surface = letter_font.render(self.letter, True, "White")
            text_rect = text_surface.get_rect(centerx=self.x+40, centery=self.y+40)
            screen.blit(text_surface, text_rect)

    def color_update(self, new):
        self.color = new



def create_boxes():
    for i in range(6):
        temp = []
        for j in range(5):
            temp.append(Boxes(100+j*90, 200+i*90, "#1a1b1c"))
        boxes.append(temp)

create_boxes()

def guess(current):
        guessed = "".join(current)
        if  guessed.lower() not in valid:
            return False
        else:
            return True

def checker(correct, guessed):
    guessed = "".join(guessed)
    print(guessed)
    print(word)
    explored = ""
    for i in range(0,5):
        if guessed[i] == word[i]:
            boxes[current_col][i].color = "Green"
            explored += guessed[i]
        elif guessed[i] in word and word.count(guessed[i]) > explored.count(guessed[i]):
                boxes[current_col][i].color = "Orange"
                explored += guessed[i]
        else:
            boxes[current_col][i].color = "Red"
            explored += guessed[i]

    if guessed == correct:
        return True
    else:
        return False

def finished():
    for i in range(5):
        text_surface = letter_font.render(word[i], True, "Green")
        text_rect = text_surface.get_rect(centerx=boxes[-1][i].x + 40, centery=boxes[-1][i].y + 200)
        screen.blit(text_surface, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha() and len(event.unicode) == 1:
                boxes[current_col][current_row].letter = event.unicode.upper()
                current_guess[current_row] = event.unicode.upper()
                if current_row < 4:
                    current_row += 1
                print(current_guess)

            if event.key == pygame.K_BACKSPACE:
                if current_row > 0 and current_guess[current_row] == 0:
                    current_row -= 1
                boxes[current_col][current_row].letter = None
                current_guess[current_row] = 0
                print(current_guess)

            if event.key == pygame.K_RETURN and current_guess[current_row] != 0:
                if guess(current_guess):
                    if checker(word, current_guess) or current_col == 5:
                        finish = True
                    current_col += 1
                    current_row = 0
                    current_guess = [0,0,0,0,0]




    screen.fill("#1a1b1c")

    for row in boxes:
        for box in row:
            box.draw()

    if finish:
        finished()

    pygame.display.update()
    clock.tick(60)