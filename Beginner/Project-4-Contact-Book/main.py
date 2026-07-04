"""
Project No. 4: Contact Book Manager
Features: Add, Show, Search, Edit, Delete Contacts
"""

import os
import json


class ContactBook:
    def __init__(self):
        """Initialize contact list and load from file"""
        self.contacts = []
        self.filename = "contacts.json"
        self.load_contacts()

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_contacts(self):
        """Load contacts from JSON file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.contacts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.contacts = []

    def save_contacts(self):
        """Save contacts to JSON file"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.contacts, file, indent=4, ensure_ascii=False)

    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("         📇 Contact Book Manager")
        print("="*50)
        print("1. Add New Contact")
        print("2. Show All Contacts")
        print("3. Search Contact")
        print("4. Edit Contact")
        print("5. Delete Contact")
        print("6. Exit")
        print("="*50)

    def get_contact_info(self):
        """Get contact information from user"""
        name = input("Enter name: ").strip()
        if not name:
            print("❌ Error: Name cannot be empty!")
            return None

        phone = input("Enter phone number: ").strip()
        email = input("Enter email (optional): ").strip()
        address = input("Enter address (optional): ").strip()

        contacts_info = {
            'name' : name,
            'phone' : phone if phone else 'N/A',
            'email' : email if email else 'N/A',
            'address' : address if address else 'N/A'
        }
        return contacts_info

    def add_contact(self):
        """Add a new contact"""
        contact = self.get_contact_info()
        if not contact:
            return

        self.contacts.append(contact)
        self.save_contacts()
        print(f"\n✅ Contact '{contact['name']}' added successfully!")

    def show_contacts(self):
        """Display all contacts"""
        if not self.contacts:
            print("\n📭 Contact list is empty!")
            return

        print("\n" + "="*60)
        print("📇 Contact List")
        print("="*60)

        for i, contact in enumerate(self.contacts, 1):
            print(f"{i}. {contact['name']}")
            print(f"   📞 {contact['phone']}")
            print(f"   📧 {contact['email']}")
            print(f"   📍 {contact['address']}")
            print("-" * 60)

    def search_contact(self):
        """Search for a contact by name"""
        query = input("\n🔍 Enter name to search: ").strip().lower()

        if not query:
            print("❌ Error: Search query cannot be empty!")
            return

        results = []
        for contact in self.contacts:
            if query in contact['name'].lower():
                results.append(contact)

        if not results:
            print(f"\n❌ No contacts found for '{query}'")
            return

        print("\n" + "="*60)
        print(f"📇 Search Results for '{query}' ({len(results)} found)")
        print("="*60)

        for i, contact in enumerate(results, 1):
            print(f"{i}. {contact['name']}")
            print(f"   📞 {contact['phone']}")
            print(f"   📧 {contact['email']}")
            print(f"   📍 {contact['address']}")
            print("-" * 60)

    def edit_contact(self):
        """Edit a contact's information"""
        self.show_contacts()

        if not self.contacts:
            return

        try:
            index = int(input("\n✏️  Enter contact number to edit: ")) - 1

            if 0 <= index < len(self.contacts):
                current = self.contacts[index]
                print(f"\nEditing: {current['name']}")
                print("Press Enter to keep current value.")

                name = input(f"Name ({current['name']}): ").strip()
                phone = input(f"Phone ({current['phone']}): ").strip()
                email = input(f"Email ({current['email']}): ").strip()
                address = input(f"Address ({current['address']}): ").strip()

                if name:
                    current['name'] = name
                if phone:
                    current['phone'] = phone
                if email:
                    current['email'] = email
                if address:
                    current['address'] = address

                self.save_contacts()
                print(f"\n✅ Contact updated successfully!")
            else:
                print("❌ Error: Invalid contact number!")

        except ValueError:
            print("❌ Error: Please enter a valid number!")

    def delete_contact(self):
        """Delete a contact"""
        self.show_contacts()

        if not self.contacts:
            return

        try:
            index = int(input("\n🗑️  Enter contact number to delete: ")) - 1

            if 0 <= index < len(self.contacts):
                removed = self.contacts.pop(index)
                self.save_contacts()
                print(f"\n✅ Contact '{removed['name']}' deleted successfully!")
            else:
                print("❌ Error: Invalid contact number!")

        except ValueError:
            print("❌ Error: Please enter a valid number!")

    def run(self):
        """Main program loop"""
        while True:
            self.clear_screen()
            self.show_menu()

            choice = input("➡️  Choose an option: ").strip()

            if choice == '1':
                self.add_contact()
                input("\n⏎ Press Enter to continue...")

            elif choice == '2':
                self.show_contacts()
                input("\n⏎ Press Enter to continue...")

            elif choice == '3':
                self.search_contact()
                input("\n⏎ Press Enter to continue...")

            elif choice == '4':
                self.edit_contact()
                input("\n⏎ Press Enter to continue...")

            elif choice == '5':
                self.delete_contact()
                input("\n⏎ Press Enter to continue...")

            elif choice == '6':
                print("\n👋 Goodbye! Your contacts have been saved.")
                break

            else:
                print("\n❌ Invalid option! Please try again.")
                input("\n⏎ Press Enter to continue...")


if __name__ == "__main__":
    book = ContactBook()
    book.run()