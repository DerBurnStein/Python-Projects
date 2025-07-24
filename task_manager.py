#!/usr/bin/env python3
"""
Interactive Task Manager
========================

This script implements a simple command‑line task manager. Tasks are
persisted to a JSON file between runs. Each task has a unique ID,
title, optional description, creation timestamp and completion status.

Features:

* List all tasks with their status and creation date
* Add a new task with a title and description
* Mark a task as completed
* Delete a task by its ID
* Save tasks to disk automatically on exit

Usage:
    python task_manager.py

The program will present a menu of options. Enter the number
corresponding to the desired action. Press Ctrl+C to exit at any time.
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional


DATA_FILE = 'tasks.json'


@dataclass
class Task:
    """Represent a single to‑do task."""

    id: int
    title: str
    description: str
    created_at: str
    completed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


class TaskManager:
    """Manage a collection of tasks, persisting them to a JSON file."""

    def __init__(self, filename: str = DATA_FILE) -> None:
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self._load()

    def _load(self) -> None:
        """Load tasks from the JSON file if it exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        task = Task(
                            id=item['id'],
                            title=item['title'],
                            description=item.get('description', ''),
                            created_at=item['created_at'],
                            completed=item.get('completed', False),
                        )
                        self.tasks.append(task)
                        self.next_id = max(self.next_id, task.id + 1)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: failed to load tasks from {self.filename}: {e}")

    def _save(self) -> None:
        """Save tasks to the JSON file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([t.to_dict() for t in self.tasks], f, indent=2)
        except IOError as e:
            print(f"Error: could not save tasks to {self.filename}: {e}")

    def add_task(self, title: str, description: str) -> Task:
        """Create a new task and add it to the list."""
        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            created_at=datetime.now().isoformat(timespec='seconds'),
        )
        self.tasks.append(task)
        self.next_id += 1
        self._save()
        return task

    def list_tasks(self) -> List[Task]:
        """Return a list of all tasks."""
        return list(self.tasks)

    def find_task(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def mark_completed(self, task_id: int) -> bool:
        """Mark the specified task as completed.

        Returns:
            True if the task was found and marked completed, False otherwise.
        """
        task = self.find_task(task_id)
        if task:
            task.completed = True
            self._save()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Remove a task from the list.

        Returns:
            True if the task was removed, False if it was not found.
        """
        for idx, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[idx]
                self._save()
                return True
        return False


def print_tasks(tasks: List[Task]) -> None:
    """Pretty print a list of tasks."""
    if not tasks:
        print("No tasks found.")
        return
    print(f"{'ID':<4} {'Completed':<10} {'Created':<20} Title")
    print('-' * 60)
    for task in tasks:
        status = '✔' if task.completed else '✖'
        print(f"{task.id:<4} {status:<10} {task.created_at:<20} {task.title}")


def prompt(text: str) -> str:
    """Prompt the user for input and return the stripped string."""
    return input(text).strip()


def menu() -> None:
    """Display the menu options."""
    print("\nTask Manager")
    print("1. List tasks")
    print("2. Add task")
    print("3. Mark task completed")
    print("4. Delete task")
    print("5. Exit")


def main() -> None:
    manager = TaskManager()
    while True:
        menu()
        choice = prompt("Select an option (1‑5): ")
        if choice == '1':
            print()
            print_tasks(manager.list_tasks())
        elif choice == '2':
            title = prompt("Enter task title: ")
            description = prompt("Enter task description (optional): ")
            task = manager.add_task(title, description)
            print(f"Task #{task.id} added.")
        elif choice == '3':
            task_id_input = prompt("Enter task ID to mark completed: ")
            try:
                task_id = int(task_id_input)
            except ValueError:
                print("Invalid ID. Please enter a number.")
                continue
            if manager.mark_completed(task_id):
                print(f"Task #{task_id} marked as completed.")
            else:
                print(f"Task #{task_id} not found.")
        elif choice == '4':
            task_id_input = prompt("Enter task ID to delete: ")
            try:
                task_id = int(task_id_input)
            except ValueError:
                print("Invalid ID. Please enter a number.")
                continue
            if manager.delete_task(task_id):
                print(f"Task #{task_id} deleted.")
            else:
                print(f"Task #{task_id} not found.")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 5.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
