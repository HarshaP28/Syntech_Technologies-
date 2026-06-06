def add(first_number: float, second_number: float) -> float:
    """Return the sum of two numbers."""
    return first_number + second_number


def subtract(first_number: float, second_number: float) -> float:
    """Return the difference between two numbers."""
    return first_number - second_number


def multiply(first_number: float, second_number: float) -> float:
    """Return the product of two numbers."""
    return first_number * second_number


def divide(first_number: float, second_number: float) -> float:
    """Return the division result of two numbers."""
    if second_number == 0:
        raise ValueError("Cannot divide by zero.")
    return first_number / second_number


def power(first_number: float, second_number: float) -> float:
    """Return the first number raised to the power of the second number."""
    return first_number**second_number


def show_menu() -> None:
    """Display the calculator menu."""
    print("\nSimple Calculator")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Power (**)")
    print("6. Exit")


def get_number(message: str) -> float:
    """Ask the user for a number until a valid number is entered."""
    while True:
        user_input = input(message)

        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def calculate(choice: str, first_number: float, second_number: float) -> float:
    """Perform the selected calculation and return the result."""
    if choice == "1":
        return add(first_number, second_number)
    if choice == "2":
        return subtract(first_number, second_number)
    if choice == "3":
        return multiply(first_number, second_number)
    if choice == "4":
        return divide(first_number, second_number)
    if choice == "5":
        return power(first_number, second_number)

    raise ValueError("Invalid menu choice.")


def run_calculator() -> None:
    """Run the calculator until the user chooses to exit."""
    while True:
        show_menu()
        choice = input("Choose an option from 1 to 6: ").strip()

        if choice == "6":
            print("Thank you for using the calculator. Goodbye!")
            break

        if choice not in {"1", "2", "3", "4", "5"}:
            print("Invalid choice. Please select a number from 1 to 6.")
            continue

        first_number = get_number("Enter the first number: ")
        second_number = get_number("Enter the second number: ")

        try:
            result = calculate(choice, first_number, second_number)
        except ValueError as error:
            print(error)
        else:
            print(f"Result: {result}")


if __name__ == "__main__":
    run_calculator()