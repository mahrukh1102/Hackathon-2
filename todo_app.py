#!/usr/bin/env python3
"""
Todo App – In-Memory Python Console Application

A simple console-based todo application that allows users to:
- Add tasks with title and optional description
- View all tasks with their status
- Mark tasks as complete/incomplete
- Update task details
- Delete tasks

All data is stored in-memory only and will be lost when the program exits.
"""

class Task:
    """Represents a single todo task."""
    def __init__(self, task_id, title, description=None, completed=False):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"ID: {self.id} | {status} | Title: {self.title}"


class TaskList:
    """Manages a collection of tasks in memory."""
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def add_task(self, title, description=None):
        """Add a new task with a unique ID."""
        task = Task(self.next_id, title, description, completed=False)
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_all_tasks(self):
        """Return all tasks."""
        return list(self.tasks.values())

    def get_task_by_id(self, task_id):
        """Get a task by its ID."""
        return self.tasks.get(task_id)

    def update_task(self, task_id, title=None, description=None):
        """Update an existing task."""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        return True

    def delete_task(self, task_id):
        """Delete a task by ID."""
        if task_id not in self.tasks:
            return False
        del self.tasks[task_id]
        return True

    def toggle_task_completion(self, task_id):
        """Toggle the completion status of a task."""
        if task_id not in self.tasks:
            return False
        self.tasks[task_id].completed = not self.tasks[task_id].completed
        return True


def display_menu():
    """Display the main menu options."""
    print("\n" + "="*40)
    print("TODO APP - Main Menu")
    print("="*40)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task Complete/Incomplete")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Exit")
    print("-"*40)


def main():
    """Main application loop."""
    print("Welcome to the Todo App!")

    # Initialize the task list
    task_list = TaskList()

    while True:
        display_menu()

        try:
            choice = input("Enter your choice (1-6): ").strip()

            if choice == '1':
                add_task(task_list)
            elif choice == '2':
                view_tasks(task_list)
            elif choice == '3':
                mark_task_complete(task_list)
            elif choice == '4':
                update_task(task_list)
            elif choice == '5':
                delete_task(task_list)
            elif choice == '6':
                print("Thank you for using the Todo App. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\n\nThank you for using the Todo App. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


def add_task(task_list):
    """Handle adding a new task."""
    print("\n--- Add New Task ---")
    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty!")
        return

    description = input("Enter task description (optional): ").strip()
    if not description:
        description = None

    task = task_list.add_task(title, description)
    print(f"Task added successfully with ID: {task.id}")


def view_tasks(task_list):
    """Handle viewing all tasks."""
    print("\n--- All Tasks ---")
    tasks = task_list.get_all_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(task)
        if task.description:
            print(f"     Description: {task.description}")
        print()


def mark_task_complete(task_list):
    """Handle marking a task as complete/incomplete."""
    print("\n--- Mark Task Complete/Incomplete ---")

    if not task_list.get_all_tasks():
        print("No tasks available.")
        return

    task_id_str = input("Enter task ID to toggle completion status: ").strip()

    try:
        task_id = int(task_id_str)
        if task_list.toggle_task_completion(task_id):
            task = task_list.get_task_by_id(task_id)
            status = "completed" if task.completed else "incomplete"
            print(f"Task {task_id} marked as {status}!")
        else:
            print(f"Task with ID {task_id} not found.")
    except ValueError:
        print("Please enter a valid task ID (number).")


def update_task(task_list):
    """Handle updating a task."""
    print("\n--- Update Task ---")

    if not task_list.get_all_tasks():
        print("No tasks available.")
        return

    task_id_str = input("Enter task ID to update: ").strip()

    try:
        task_id = int(task_id_str)
        task = task_list.get_task_by_id(task_id)

        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        print(f"Current title: {task.title}")
        new_title = input("Enter new title (or press Enter to keep current): ").strip()

        print(f"Current description: {task.description or 'None'}")
        new_description = input("Enter new description (or press Enter to keep current): ").strip()

        # If user pressed Enter without typing anything, keep the current value
        title = new_title if new_title else None
        description = new_description if new_description else None

        # If user explicitly wants to clear the description, set it to None
        if new_description == "":
            description = None

        if task_list.update_task(task_id, title, description):
            print(f"Task {task_id} updated successfully!")
        else:
            print(f"Failed to update task {task_id}.")
    except ValueError:
        print("Please enter a valid task ID (number).")


def delete_task(task_list):
    """Handle deleting a task."""
    print("\n--- Delete Task ---")

    if not task_list.get_all_tasks():
        print("No tasks available.")
        return

    task_id_str = input("Enter task ID to delete: ").strip()

    try:
        task_id = int(task_id_str)

        # Confirmation prompt
        task = task_list.get_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        confirm = input(f"Are you sure you want to delete task '{task.title}'? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            if task_list.delete_task(task_id):
                print(f"Task {task_id} deleted successfully!")
            else:
                print(f"Failed to delete task {task_id}.")
        else:
            print("Deletion cancelled.")
    except ValueError:
        print("Please enter a valid task ID (number).")


if __name__ == "__main__":
    main()