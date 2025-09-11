from wordfreq import top_n_list
from string import ascii_lowercase
#Currently it works only with words which are solely of letters in ascii_lowercase
print("Information about supported languages are in languages.txt")
language = input("Enter the language you wish to use: ")
print("Keep in mind it is not the total amount because the program will filter out every word with len != 5 afterwards")
size = int(input("Enter the number of words you wish to generate: "))
file = input("Enter the filename of your wordlist: ")

top_words = top_n_list(language, size)

with open(file + ".txt" , 'w') as f:
    for word in top_words:
        if len(word) == 5:
            if set(word) - set(ascii_lowercase):
                continue
            f.write(word + "\n")

