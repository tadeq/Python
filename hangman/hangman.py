from random import randint
from random import seed
from itertools import chain
from os import system

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
    lines_back = 1
    while len(c) != 1:
        print(lines_back * ("\033[F" + "\033[K") + "Enter exactly one letter")
        c = input()
        lines_back = 2
    while c not in legal_letters:
        print(lines_back * ("\033[F" + "\033[K") + "You have to enter a letter")
        c = input()
        lines_back = 2
        while len(c) != 1:
            print(lines_back * ("\033[F" + "\033[K") + "Enter exactly one letter")
            c = input()
            lines_back = 2
    return c


def print_gamefield(word, mistakes_no):
    print(" ".join(word) + "   mistakes: {}/3".format(mistakes_no))


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
        print_gamefield(to_guess, mistakes)
        guess = get_correct_char()
        letter_in_word = False
        if guess.lower() in to_guess or guess.upper() in to_guess \
                or guess.upper() in wrong_letters or guess.lower() in wrong_letters:
            system('clear')
            print("Letter {} has already been entered".format(guess.lower()))
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
            system('clear')
    print_gamefield(to_guess, mistakes)
    if guessed:
        print("YOU WON")
    else:
        print("YOU LOST. THE CORRECT WORD WAS \"{}\"".format("".join(word)))


def main():
    game(get_word())


if __name__ == "__main__":
    system('clear')
    main()
