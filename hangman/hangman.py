from random import randint
from random import seed
from itertools import chain

standard_letters = chain(range(97, 123), range(65, 91))
special_letters = "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"
legal_letters = [chr(letter) for letter in standard_letters]
legal_letters += list(special_letters)


def get_word():
    words = []
    with open("countries.txt", "r") as file:
        for line in file:
            words.append(line)
    seed(None)
    word = words[randint(0, len(words) - 1)]
    word = word.strip()
    return list(word)


def get_correct_char():
    c = input()
    while len(c) != 1:
        print("Enter exactly one letter")
        c = input()
    while c not in legal_letters:
        print("You have to enter a letter")
        c = input()
        while len(c) != 1:
            print("Enter exactly one letter")
            c = input()
    return c


def game(word):
    to_guess = list(word)
    wrong_letters = []
    for i in range(len(word)):
        if word[i] == " ":
            to_guess[i] = " "
        elif word[i] == "-":
            to_guess[i] = "-"
        else:
            to_guess[i] = "_"
    guessed = False
    mistakes = 0
    while not guessed and mistakes < 3:
        print(" ".join(to_guess) + "   mistakes: %d/3" % mistakes)
        guess = get_correct_char()
        letter_in_word = False
        if guess.lower() in to_guess or guess.upper() in to_guess \
                or guess.upper() in wrong_letters or guess.lower() in wrong_letters:
            print("This letter has already been entered")
        else:
            for i in range(len(word)):
                if guess.lower() == word[i].lower() and guess.upper() not in to_guess and guess.lower() not in to_guess:
                    to_guess[i] = word[i]
                    for j in range(i + 1, len(word)):
                        if word[j].lower() == word[i].lower():
                            to_guess[j] = word[j]
                    letter_in_word = True
            if not letter_in_word:
                wrong_letters.append(guess)
                mistakes += 1
            if to_guess == word:
                guessed = True
    print(" ".join(to_guess) + "   mistakes: %d/3" % mistakes)
    if guessed:
        print("YOU WON")
    else:
        print("YOU LOST. THE CORRECT WORD WAS \"%s\"" % "".join(word))


def main():
    game(get_word())


main()
