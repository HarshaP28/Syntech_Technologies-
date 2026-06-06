"""Command-line password generator.

Generates a strong random password containing uppercase letters, lowercase
letters, numbers, and special characters.
"""

import random
import string


DEFAULT_LENGTH = 16
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.<>?/"


def generate_password(length=DEFAULT_LENGTH):
    """Return a random password with all required character types."""
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    required_characters = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(SPECIAL_CHARACTERS),
    ]

    all_characters = (
        string.ascii_uppercase
        + string.ascii_lowercase
        + string.digits
        + SPECIAL_CHARACTERS
    )
    remaining_characters = [
        random.choice(all_characters) for _ in range(length - len(required_characters))
    ]

    password_characters = required_characters + remaining_characters
    random.shuffle(password_characters)
    return "".join(password_characters)


def get_password_length():
    """Ask the user for a password length, using the default when blank."""
    user_input = input(f"Enter password length (default {DEFAULT_LENGTH}): ").strip()

    if not user_input:
        return DEFAULT_LENGTH

    try:
        return int(user_input)
    except ValueError as error:
        raise ValueError("Password length must be a whole number.") from error


def main():
    """Run the password generator CLI."""
    try:
        length = get_password_length()
        password = generate_password(length)
        print(f"Strong random password: {password}")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()