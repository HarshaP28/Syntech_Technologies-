"""A simple number guessing game written in one Python file."""

import random


MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_ATTEMPTS = 10


def show_welcome_message():
    """Display the game title and rules."""
    print("=" * 45)
    print("          NUMBER GUESSING GAME")
    print("=" * 45)
    print(f"Guess a number between {MIN_NUMBER} and {MAX_NUMBER}.")
    print(f"You have {MAX_ATTEMPTS} attempts to find the correct number.")
    print("Type 'q' anytime to quit the game.")
    print("=" * 45)


def get_player_guess(attempts_left):
    """Ask the player for a valid guess and return it as an integer."""
    while True:
        guess = input(f"Enter your guess ({attempts_left} attempts left): ").strip()

        if guess.lower() == "q":
            return None

        if not guess.isdigit():
            print("Please enter a whole number only.")
            continue

        guess = int(guess)

        if guess < MIN_NUMBER or guess > MAX_NUMBER:
            print(f"Please enter a number from {MIN_NUMBER} to {MAX_NUMBER}.")
            continue

        return guess


def give_hint(player_guess, secret_number):
    """Tell the player whether the guess is too low or too high."""
    if player_guess < secret_number:
        print("Your guess is too low. Try a bigger number!")
    else:
        print("Your guess is too high. Try a smaller number!")


def play_game():
    """Run one complete round of the number guessing game."""
    secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts_left = MAX_ATTEMPTS
    previous_guesses = []

    show_welcome_message()

    while attempts_left > 0:
        player_guess = get_player_guess(attempts_left)

        if player_guess is None:
            print("Thanks for playing. Goodbye!")
            return

        previous_guesses.append(player_guess)
        attempts_left -= 1

        if player_guess == secret_number:
            print(f"Congratulations! {player_guess} is correct.")
            print(f"You won in {len(previous_guesses)} attempt(s)!")
            return

        give_hint(player_guess, secret_number)
        print("Previous guesses:", ", ".join(str(number) for number in previous_guesses))
        print()

    print("Game over! You used all your attempts.")
    print(f"The correct number was {secret_number}.")


if __name__ == "__main__":
    play_game()