#!/usr/bin/env python3

"""
A simple command-line task tracker that stores tasks in a JSON file.

Usage:
  python task_tracker.py list
  python task_tracker.py add "Your new task description"
  python task_tracker.py complete <task_number>
  python task_tracker.py remove <task_number>
  python task_tracker.py help
"""

import sys
import json
import os
from typing import List, Dict, Union

# Define the file where tasks will be stored
JSON_FILE = "tasks.json"

Task = Dict[str, Union[str, str]]  # Type hint for a task dictionary

def load_tasks() -> List[Task]:
    """
    Loads tasks from the JSON_FILE.
    If the file doesn't exist or is empty, returns an empty list.
    """
    if not os.path.exists(JSON_FILE):
        return []
    
    try:
        with open(JSON_FILE, 'r') as f:
            tasks = json.load(f)
            # Ensure it's a list, handle empty file case
            return tasks if isinstance(tasks, list) else []
    except json.JSONDecodeError:
        # Handle case where file is empty or corrupt
        return []

def save_tasks(tasks: List[Task]) -> None:
    """
    Saves the given list of tasks to the JSON_FILE.
    """
    try:
        with open(JSON_FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
    except IOError as e:
        print(f"Error: Could not save tasks to {JSON_FILE}. {e}")

def show_help() -> None:
    """
    Prints the help message with usage instructions.
    """
    print("--- Task Tracker Help ---")
    print("Usage:")
    print("  python task_tracker.py list                : Show all tasks")
    print("  python task_tracker.py add \"<description>\" : Add a new task")
    print("  python task_tracker.py complete <number>   : Mark a task as complete")
    print("  python task_tracker.py remove <number>     : Remove a task")
    print("  python task_tracker.py help                : Show this help message")
    print("\nExamples:")
    print("  python task_tracker.py add \"Buy milk and eggs\"")
    print("  python task_tracker.py complete 3")

def add_task(description: str) -> None:
    """
    Adds a new task with the given description.
    """
    if not description:
        print("Error: Cannot add an empty task.")
        return

    tasks = load_tasks()
    new_task = {
        "description": description,
        "status": "pending"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added: \"{description}\"")

def list_tasks() -> None:
    """
    Lists all tasks with their status and 1-based index.
    """
    tasks = load_tasks()
    if not tasks:
        print("No tasks found. Add one with the 'add' command!")
        return

    print("--- Your Tasks ---")
    for i, task in enumerate(tasks, 1):
        status_icon = "[x]" if task.get('status') == 'complete' else "[ ]"
        print(f"  {i}. {status_icon} {task.get('description', 'No description')}")
    print("------------------")

def _update_task(task_index_str: str, action: str) -> None:
    """
    A helper function to either complete or remove a task.
    """
    try:
        # Convert to a 0-based index
        task_index = int(task_index_str) - 1
    except ValueError:
        print(f"Error: Invalid task number '{task_index_str}'. Must be an integer.")
        return

    tasks = load_tasks()

    if 0 <= task_index < len(tasks):
        if action == "complete":
            if tasks[task_index]["status"] == "complete":
                print(f"Task {task_index + 1} is already marked as complete.")
            else:
                tasks[task_index]["status"] = "complete"
                save_tasks(tasks)
                print(f"Task {task_index + 1} marked as complete: \"{tasks[task_index]['description']}\"")
        elif action == "remove":
            removed_task = tasks.pop(task_index)
            save_tasks(tasks)
            print(f"Task {task_index + 1} removed: \"{removed_task['description']}\"")
    else:
        print(f"Error: Task number {task_index + 1} not found.")
        if not tasks:
            print("You have no tasks.")
        else:
            print(f"Valid task numbers are 1 to {len(tasks)}.")

def complete_task(task_index_str: str) -> None:
    """
    Marks a task as complete given its 1-based index.
    """
    _update_task(task_index_str, "complete")

def remove_task(task_index_str: str) -> None:
    """
    Removes a task from the list given its 1-based index.
    """
    _update_task(task_index_str, "remove")

def main() -> None:
    """
    Main function to parse command-line arguments and route to the correct function.
    """
    # sys.argv[0] is the script name, sys.argv[1] is the command
    if len(sys.argv) < 2:
        print("Error: No command provided.")
        show_help()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "list":
        list_tasks()
    elif command == "add":
        if len(sys.argv) < 3:
            print("Error: 'add' command requires a task description.")
            print("Example: python task_tracker.py add \"Buy groceries\"")
        else:
            # Join all arguments after 'add' to form the task description
            description = " ".join(sys.argv[2:])
            add_task(description)
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Error: 'complete' command requires a task number.")
            print("Example: python task_tracker.py complete 2")
        else:
            complete_task(sys.argv[2])
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Error: 'remove' command requires a task number.")
            print("Example: python task_tracker.py remove 1")
        else:
            remove_task(sys.argv[2])
    elif command == "help":
        show_help()
    else:
        print(f"Error: Unknown command '{command}'")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()