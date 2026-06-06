"""A simple command-line To-Do List application."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

TASKS_FILE = Path("tasks.json")


@dataclass
class Task:
    """Represents one to-do item."""

    title: str
    completed: bool = False


class TodoList:
    """Handles task storage and task actions."""

    def __init__(self, file_path: Path = TASKS_FILE) -> None:
        self.file_path = file_path
        self.tasks: list[Task] = []
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load saved tasks from the JSON file if it exists."""
        if not self.file_path.exists():
            self.tasks = []
            return

        with self.file_path.open("r", encoding="utf-8") as file:
            saved_tasks = json.load(file)

        self.tasks = [Task(**task) for task in saved_tasks]

    def save_tasks(self) -> None:
        """Save all tasks to the JSON file."""
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump([asdict(task) for task in self.tasks], file, indent=4)

    def add_task(self, title: str) -> None:
        """Add a new task to the list."""
        self.tasks.append(Task(title=title))
        self.save_tasks()

    def show_tasks(self) -> None:
        """Print all tasks in a clean format."""
        if not self.tasks:
            print("\nNo tasks found. Add a task first!\n")
            return

        print("\nYour To-Do List:")
        for index, task in enumerate(self.tasks, start=1):
            status = "Done" if task.completed else "Pending"
            print(f"{index}. [{status}] {task.title}")
        print()

    def mark_task_done(self, task_number: int) -> bool:
        """Mark a task as completed. Returns True if successful."""
        if not self._is_valid_task_number(task_number):
            return False

        self.tasks[task_number - 1].completed = True
        self.save_tasks()
        return True

    def delete_task(self, task_number: int) -> bool:
        """Delete a task. Returns True if successful."""
        if not self._is_valid_task_number(task_number):
            return False

        self.tasks.pop(task_number - 1)
        self.save_tasks()
        return True

    def _is_valid_task_number(self, task_number: int) -> bool:
        """Check whether a task number exists in the list."""
        return 1 <= task_number <= len(self.tasks)


def show_menu() -> None:
    """Display the available actions."""
    print("To-Do List App")
    print("1. Show tasks")
    print("2. Add task")
    print("3. Mark task as done")
    print("4. Delete task")
    print("5. Exit")


def ask_task_number(message: str) -> int | None:
    """Ask the user for a task number and validate that it is numeric."""
    user_input = input(message).strip()

    if not user_input.isdigit():
        print("Please enter a valid number.\n")
        return None

    return int(user_input)


def main() -> None:
    """Start the command-line app."""
    todo_list = TodoList()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            todo_list.show_tasks()

        elif choice == "2":
            title = input("Enter task title: ").strip()
            if title:
                todo_list.add_task(title)
                print("Task added successfully!\n")
            else:
                print("Task title cannot be empty.\n")

        elif choice == "3":
            task_number = ask_task_number("Enter task number to mark as done: ")
            if task_number is not None and todo_list.mark_task_done(task_number):
                print("Task marked as done!\n")
            else:
                print("Task not found.\n")

        elif choice == "4":
            task_number = ask_task_number("Enter task number to delete: ")
            if task_number is not None and todo_list.delete_task(task_number):
                print("Task deleted successfully!\n")
            else:
                print("Task not found.\n")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose from 1 to 5.\n")


if __name__ == "__main__":
    main()