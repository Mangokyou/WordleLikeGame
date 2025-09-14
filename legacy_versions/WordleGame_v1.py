from random import choice
from string import ascii_lowercase, ascii_uppercase

#word_list = input("Enter the name of your words file: ")
word_list = "english_words.txt"

with open(word_list, "r") as f:
    words = f.read().split()

with open("english_words_valid.txt", "r") as f:
    valid = f.read().split()

def checker(word, guess):
    output = []
    explored = ""
    for i in range(0,5):
        if guess[i] == word[i]:
            output.append("+")
            explored += guess[i]
        elif guess[i] in word and word.count(guess[i]) > explored.count(guess[i]):
                output.append("*")
                explored += guess[i]
        else:
            output.append("-")
            explored += guess[i]

    return output


def guesser():
    while True:
        word = input("Guess a word: ")
        if len(word) != 5:
            print("The word must be 5 characters long.")
        elif word.lower() not in valid:
            print("The word you entered is not a possible word.")
        else:
            return word

def main():
    while True:
        word = choice(words).upper()
        #word = "APPLE"
        counter = False
        for i in range(1,6):
            guess = guesser().upper()
            if guess == word:
                counter = i
                break
            correct = checker(word, guess)
            print(" ".join(guess))
            print(" ".join(correct))

        print("The word was: " + word)
        if counter:
            print("You needed " + str(counter) + " guesses.")
        else:
            print("You did not guess the word in 5 tries")

        if input("Do you want to play again? (y/n): ") != "y":
            break


print("Explanation: ")
print("+ = Correct letter in correct position\n* = Correct letter in wrong position\n- = Wrong letter")
main()
print("Thank you for playing!")