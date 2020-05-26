import functools
import random
from functools import reduce
import time
import Graphics

def get_words(filename):
    text = open(filename, "r", encoding="utf-8")

    return text

def set_game_mode():
    game_mode = input("What type of game you wanna play? (Manual / Auto) ").lower()

    if game_mode == "manual":
        print("Manual game mode requires to interact with PC !")
    elif game_mode == "auto":
        print("Auto game mode allows just to watch the flow")

    return game_mode

def guess_counter(guesses):

    if guesses == 9:
        print("You have last try left...!")
    elif guesses == 10:
        print("Out of tries, you've lost!")

    return guesses


def choose_word(text):

    words = text
    randomize = input("Do you want to choose word by yourself or select a word randomly? (Choose / Random)...").lower()
    wordlist = [word.lower().strip() for word in words.readlines()]

    if randomize == 'choose':
        word_to_guess =  input("Choose the word from to be guessed from a list")
    elif randomize == 'random':
        word_to_guess = random.choice(wordlist)

    return word_to_guess


def counter(letter_freq, char):

    if char.isalpha() == True:
        letter_freq[char] = letter_freq.get(char, 0) + 1

    return letter_freq


def get_letter_freq(text):

    text.seek(0)
    characters = text.read()

    return reduce (counter, characters, {})


def pick_up_letter(letters_freq):

    letter = ''
    most_frequent = {k: v for k, v in sorted(letters_freq.items(), key=lambda item: item[1])}
    for char, freq in most_frequent.items():
        letter = char

    return letter


def letter_appearance(game_mode, word_to_guess, letter):

    if game_mode == 'manual':
        letter_approval = input("Is there a letter '%s' in a word? (Y / N) " % (letter))
    elif game_mode == 'auto':
        word_letters = set([ch for ch in word_to_guess])
        print("PC: Is there a letter '%s' in a word? (Y / N) " % (letter))
        if letter in word_letters:
            letter_approval ='Y'
            print("Player: ", "'", letter_approval , "'"," Correct, you've guessed the letter!", '\n')
        elif letter not in word_letters:
            letter_approval = 'N'
            print("Player: ", "'", letter_approval , "'"," Nope, there's no such letter in that word! Try again...", '\n')
    else:
        raise ValueError("Player: What? Choose coorect mode!")

    return letter_approval


def initial_mask(word_to_guess):
    letters_num = len(word_to_guess)
    word_placeholder = [' __' for letter in range(letters_num)]

    return word_placeholder


def draw_mask(word_to_guess, letter_approval, guesses, placeholder, letter):

    word_placeholder = placeholder
    letters_to_guess = [letter for letter in word_to_guess]
    if letter_approval == 'Y':
        letter_indices = [ind for ind, character in enumerate(letters_to_guess) if character == letter]
        for i in letter_indices:
            word_placeholder[i] = ' ' + letter + ' '
    mask = '\n' + ' '.join(word_placeholder) + '\n'
    print(mask)

    return word_placeholder


def play_game(filename):


    game_mode = set_game_mode()
    image = Graphics.get_image()
    words = get_words(filename)
    characters = words
    word_to_guess = choose_word(words)
    letter_freq = get_letter_freq(characters)

    guesses = 0
    fail_counter = 0
    word_placeholder = initial_mask(word_to_guess)

    while guesses <= 10:
        print("Word to guess: ", word_to_guess)
        print("Guess try #", guesses, '\n')
        letter = pick_up_letter(letter_freq)
        letter_approval = letter_appearance(game_mode, word_to_guess, letter)
        letter_freq.pop(letter)

        guesses = guess_counter(guesses)
        time.sleep(1.5)
        draw_mask(word_to_guess, letter_approval, guesses, word_placeholder, letter)

        if letter_approval == "Y":
            for i in image[fail_counter]:
                print(i)
        elif letter_approval == "N":
            fail_counter += 1
            for i in  image[fail_counter]:
                print(i)
        if guesses == 10 and word_placeholder != [ch for ch in word_to_guess]:
            print("You couldn't guess the word!")
        elif word_placeholder == [ch for ch in word_to_guess]:
            print("Hooray, congrats, you've guessed the word!")
        guesses += 1
        print("=================================================")
        time.sleep(5)


play_game("words.txt")
