import os
import json


class FileManager:
    def __init__(self):
        """Initialize file list and load from file"""
        self.files = []
        self.filename = "files.json"
        self.load_files()

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_files(self):
        """Load file list from JSON"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.files = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.files = []

    def save_files(self):
        """Save file list to JSON"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.files, f, indent=4, ensure_ascii=False)

    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("         📁 File Manager")
        print("="*50)
        print("1. Create File")
        print("2. Write to File")
        print("3. Read File")
        print("4. Delete File")
        print("5. List Files")
        print("6. Exit")
        print("="*50)

    def create_file(self):
        """Create a new empty file"""
        name = input("\n📝 Enter file name (with .txt): ").strip()

        if not name:
            print("❌ Name cannot be empty!")
            return

        if name in self.files:
            print("❌ File already exists!")
            return

        # Create empty file
        with open(name, 'w', encoding='utf-8') as f:
            f.write("")

        self.files.append(name)
        self.save_files()
        print(f"✅ File '{name}' created successfully!")

    def write_file(self):
        """Write content to a file"""
        name = input("\n✏️  Enter file name to write: ").strip()

        if name not in self.files:
            print("❌ File not found!")
            return

        content = input("Enter content: ")
        with open(name, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Content written successfully!")

    def read_file(self):
        """Read and display file content"""
        name = input("\n📖 Enter file name to read: ").strip()

        if name not in self.files:
            print("❌ File not found!")
            return

        try:
            with open(name, 'r', encoding='utf-8') as f:
                content = f.read()

            print("\n" + "="*40)
            print(f"📄 Content of '{name}':")
            print("="*40)
            print(content if content else "(empty file)")
            print("="*40)

        except Exception as e:
            print(f"❌ Error reading file: {e}")

    def delete_file(self):
        """Delete a file"""
        name = input("\n🗑️  Enter file name to delete: ").strip()

        if name not in self.files:
            print("❌ File not found!")
            return

        confirm = input(f"⚠️ Are you sure you want to delete '{name}'? (y/n): ")
        if confirm.lower() != 'y':
            print("❌ Operation cancelled.")
            return

        os.remove(name)
        self.files.remove(name)
        self.save_files()
        print(f"✅ File '{name}' deleted successfully!")

    def list_files(self):
        """List all files"""
        if not self.files:
            print("\n📭 No files created yet!")
            return

        print("\n" + "="*40)
        print("📁 Your Files:")
        print("="*40)
        for i, name in enumerate(self.files, 1):
            # Show file size
            try:
                size = os.path.getsize(name)
                print(f"{i}. {name} ({size} bytes)")
            except:
                print(f"{i}. {name}")
        print("="*40)

    def run(self):
        """Main program loop"""
        while True:
            self.clear_screen()
            self.show_menu()

            choice = input("➡️  Choose an option: ").strip()

            if choice == '1':
                self.create_file()
            elif choice == '2':
                self.write_file()
            elif choice == '3':
                self.read_file()
            elif choice == '4':
                self.delete_file()
            elif choice == '5':
                self.list_files()
            elif choice == '6':
                print("\n👋 Goodbye! Your files are saved.")
                break
            else:
                print("❌ Invalid option! Please try again.")

            input("\n⏎ Press Enter to continue...")


if __name__ == "__main__":
    app = FileManager()
    app.run()