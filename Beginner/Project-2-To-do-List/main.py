import os
import json

class TodoList:
    def __init__(self):
        """Initialize: task list and storage file"""
        self.tasks = []  # List of tasks (each task is a dictionary)
        self.filename = "tasks.json"  # File name for storage
        self.load_tasks()  # Load tasks from file

    def clear_screen(self):
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_tasks(self):
        # Load tasks from JSON file
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            # If file doesn't exist, start with empty list
            self.tasks = []
        except json.JSONDecodeError:
            # If file is corrupted, start with empty list
            self.tasks = []

    def save_tasks(self):
        # Save tasks to JSON file
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, indent=4, ensure_ascii=False)

    def show_menu(self):
        # Display the main menu
        print("\n" + "="*50)
        print("         📋 To-Do List Manager")
        print("="*50)
        print("1. Show all tasks")
        print("2. Add new task")
        print("3. Edit task")
        print("4. Delete task")
        print("5. Mark as done")
        print("6. Task statistics")
        print("7. Exit")
        print("="*50)

    def show_tasks(self):
        # Display all tasks with numbers
        if not self.tasks:
            print("\n📭 Task list is empty!")
            return
        
        print("\n" + "="*50)
        print("📌 Task List:")
        print("="*50)
        for i, task in enumerate(self.tasks, 1):
            # Show task status (done or not done)
            status = "✅" if task['done'] else "⬜"
            print(f"{i}. {status} {task['title']}")
        print("="*50)

    def add_task(self):
        # Add a new task
        title = input("\n📝 Enter task title: ").strip()
        
        # Validation: title cannot be empty
        if not title:
            print("❌ Error: Task title cannot be empty!")
            return
        
        # Create new task (dictionary)
        new_task = {
            'title': title,
            'done': False
        }
        
        self.tasks.append(new_task)
        self.save_tasks()  # Save to file
        print(f"✅ Task '{title}' added successfully!")

    def edit_task(self):
        # Edit a task's title
        self.show_tasks()
        
        if not self.tasks:
            return
        
        try:
            # Get task number from user
            task_num = int(input("\n✏️  Enter task number to edit: "))
            
            # Check if task number is valid
            if 1 <= task_num <= len(self.tasks):
                new_title = input("Enter new title: ").strip()
                
                if not new_title:
                    print("❌ Error: Title cannot be empty!")
                    return
                
                # Store old title for feedback message
                old_title = self.tasks[task_num - 1]['title']
                self.tasks[task_num - 1]['title'] = new_title
                self.save_tasks()
                print(f"✅ Task '{old_title}' updated to '{new_title}'!")
            else:
                print("❌ Error: Invalid task number!")
                
        except ValueError:
            print("❌ Error: Please enter a valid number!")

    def delete_task(self):
        # Delete a task
        self.show_tasks()
        
        if not self.tasks:
            return
        
        try:
            task_num = int(input("\n🗑️  Enter task number to delete: "))
            
            if 1 <= task_num <= len(self.tasks):
                # Remove task from list
                removed_task = self.tasks.pop(task_num - 1)
                self.save_tasks()
                print(f"✅ Task '{removed_task['title']}' deleted successfully!")
            else:
                print("❌ Error: Invalid task number!")
                
        except ValueError:
            print("❌ Error: Please enter a valid number!")

    def mark_done(self):
        # Mark a task as done
        self.show_tasks()
        
        if not self.tasks:
            return
        
        try:
            task_num = int(input("\n✅ Enter task number to mark as done: "))
            
            if 1 <= task_num <= len(self.tasks):
                # Change task status to done
                self.tasks[task_num - 1]['done'] = True
                self.save_tasks()
                print(f"✅ Task '{self.tasks[task_num - 1]['title']}' marked as done!")
            else:
                print("❌ Error: Invalid task number!")
                
        except ValueError:
            print("❌ Error: Please enter a valid number!")

    def show_count(self):
        # Display task statistics
        total = len(self.tasks)
        done = sum(1 for task in self.tasks if task['done'])
        pending = total - done
        
        print("\n" + "="*50)
        print("📊 Task Statistics:")
        print("="*50)
        print(f"📌 Total tasks: {total}")
        print(f"✅ Done: {done}")
        print(f"⏳ Pending: {pending}")
        print("="*50)

    def run(self):
        # Main program loop
        while True:
            self.clear_screen()
            self.show_menu()
            
            choice = input("➡️  Choose an option: ").strip()
            
            if choice == '1':
                self.show_tasks()
                input("\n⏎ Press Enter to continue...")
            
            elif choice == '2':
                self.add_task()
                input("\n⏎ Press Enter to continue...")
            
            elif choice == '3':
                self.edit_task()
                input("\n⏎ Press Enter to continue...")
            
            elif choice == '4':
                self.delete_task()
                input("\n⏎ Press Enter to continue...")
            
            elif choice == '5':
                self.mark_done()
                input("\n⏎ Press Enter to continue...")
            
            elif choice == '6':
                self.show_count()
                input("\n⏎ Press Enter to continue...")
            
            elif choice == '7':
                print("\n👋 Goodbye! Your tasks have been saved.")
                break
            
            else:
                print("\n❌ Invalid option! Please try again.")
                input("\n⏎ Press Enter to continue...")


# Run the program
if __name__ == "__main__":
    todo = TodoList()
    todo.run()