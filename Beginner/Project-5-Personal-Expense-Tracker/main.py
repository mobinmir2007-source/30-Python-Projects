import os
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        """Initialize transaction list and load from file"""
        self.transactions = []
        self.filename = "transactions.json"
        self.load_transactions()

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_transactions(self):
        """Load transactions from JSON file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.transactions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.transactions = []

    def save_transactions(self):
        """Save transactions to JSON file"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.transactions, file, indent=4, ensure_ascii=False)

    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("         💰 Personal Expense Tracker")
        print("="*50)
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show All Transactions")
        print("4. Show Summary")
        print("5. Monthly Report")
        print("6. Search Transactions")
        print("7. Delete Transaction")
        print("8. Exit")
        print("="*50)

    def get_date(self):
        """Get date from user or use today's date"""
        date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date:
            return datetime.now().strftime("%Y-%m-%d")
        return date

    def get_amount(self):
        """Get amount from user with validation"""
        while True:
            try:
                amount = int(input("Enter amount (in IRR): ").strip())
                if amount < 0:
                    print("❌ Amount cannot be negative!")
                    continue
                return amount
            except ValueError:
                print("❌ Please enter a valid number!")

    def add_transaction(self, trans_type):
        """Add an income or expense transaction"""
        print(f"\n📝 Add {trans_type.capitalize()}:")
        
        amount = self.get_amount()
        if amount == 0:
            print("❌ Amount cannot be zero!")
            return

        category = input("Enter category (e.g., Food, Rent, Salary): ").strip()
        if not category:
            category = "Other"

        description = input("Enter description: ").strip()
        if not description:
            description = "No description"

        date = self.get_date()

        transaction = {
            'type': trans_type,
            'amount': amount,
            'category': category,
            'description': description,
            'date': date
        }

        self.transactions.append(transaction)
        self.save_transactions()
        print(f"\n✅ {trans_type.capitalize()} added successfully!")

    def format_amount(self, amount):
        """Format amount with comma separators"""
        return f"{amount:,}"

    def show_all(self):
        """Display all transactions"""
        if not self.transactions:
            print("\n📭 No transactions found!")
            return

        print("\n" + "="*70)
        print("📋 All Transactions")
        print("="*70)
        print(f"{'#':<4} {'Type':<8} {'Amount':<15} {'Category':<12} {'Date':<12} {'Description'}")
        print("-" * 70)

        for i, t in enumerate(self.transactions, 1):
            type_icon = "💰" if t['type'] == 'income' else "💸"
            amount = self.format_amount(t['amount'])
            print(f"{i:<4} {type_icon} {t['type']:<6} {amount:<15} {t['category']:<12} {t['date']:<12} {t['description']}")
        print("="*70)

    def show_summary(self):
        """Display summary of income, expense, and balance"""
        if not self.transactions:
            print("\n📭 No transactions found!")
            return

        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        balance = total_income - total_expense

        print("\n" + "="*50)
        print("📊 Financial Summary")
        print("="*50)
        print(f"💰 Total Income:  {self.format_amount(total_income)} IRR")
        print(f"💸 Total Expense: {self.format_amount(total_expense)} IRR")
        print("-" * 50)
        print(f"📌 Balance:       {self.format_amount(balance)} IRR")
        print("="*50)

    def monthly_report(self):
        """Display monthly report"""
        month = input("\n📅 Enter month (YYYY-MM) or press Enter for current month: ").strip()
        
        if not month:
            month = datetime.now().strftime("%Y-%m")

        filtered = [t for t in self.transactions if t['date'].startswith(month)]

        if not filtered:
            print(f"\n📭 No transactions found for {month}")
            return

        total_income = sum(t['amount'] for t in filtered if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in filtered if t['type'] == 'expense')
        balance = total_income - total_expense

        print("\n" + "="*55)
        print(f"📊 Monthly Report - {month}")
        print("="*55)
        print(f"💰 Total Income:  {self.format_amount(total_income)} IRR")
        print(f"💸 Total Expense: {self.format_amount(total_expense)} IRR")
        print("-" * 55)
        print(f"📌 Balance:       {self.format_amount(balance)} IRR")
        print("="*55)

        # Show transactions for this month
        print("\n📋 Transactions:")
        print("-" * 55)
        for t in filtered:
            type_icon = "💰" if t['type'] == 'income' else "💸"
            amount = self.format_amount(t['amount'])
            print(f"{type_icon} {t['date']} - {t['category']}: {amount} - {t['description']}")

    def search(self):
        """Search transactions by description or category"""
        query = input("\n🔍 Enter search term: ").strip().lower()
        
        if not query:
            print("❌ Search term cannot be empty!")
            return

        results = []
        for t in self.transactions:
            if query in t['description'].lower() or query in t['category'].lower():
                results.append(t)

        if not results:
            print(f"\n❌ No transactions found for '{query}'")
            return

        print("\n" + "="*70)
        print(f"📋 Search Results for '{query}' ({len(results)} found)")
        print("="*70)
        print(f"{'#':<4} {'Type':<8} {'Amount':<15} {'Category':<12} {'Date':<12} {'Description'}")
        print("-" * 70)

        for i, t in enumerate(results, 1):
            type_icon = "💰" if t['type'] == 'income' else "💸"
            amount = self.format_amount(t['amount'])
            print(f"{i:<4} {type_icon} {t['type']:<6} {amount:<15} {t['category']:<12} {t['date']:<12} {t['description']}")
        print("="*70)

    def delete(self):
        """Delete a transaction by index"""
        self.show_all()
        
        if not self.transactions:
            return

        try:
            index = int(input("\n🗑️  Enter transaction number to delete: ")) - 1

            if 0 <= index < len(self.transactions):
                removed = self.transactions.pop(index)
                self.save_transactions()
                print(f"\n✅ Transaction '{removed['description']}' deleted successfully!")
            else:
                print("❌ Error: Invalid transaction number!")

        except ValueError:
            print("❌ Error: Please enter a valid number!")

    def run(self):
        """Main program loop"""
        while True:
            self.clear_screen()
            self.show_menu()

            choice = input("➡️  Choose an option: ").strip()

            if choice == '1':
                self.add_transaction('income')
                input("\n⏎ Press Enter to continue...")

            elif choice == '2':
                self.add_transaction('expense')
                input("\n⏎ Press Enter to continue...")

            elif choice == '3':
                self.show_all()
                input("\n⏎ Press Enter to continue...")

            elif choice == '4':
                self.show_summary()
                input("\n⏎ Press Enter to continue...")

            elif choice == '5':
                self.monthly_report()
                input("\n⏎ Press Enter to continue...")

            elif choice == '6':
                self.search()
                input("\n⏎ Press Enter to continue...")

            elif choice == '7':
                self.delete()
                input("\n⏎ Press Enter to continue...")

            elif choice == '8':
                print("\n👋 Goodbye! Your transactions have been saved.")
                break

            else:
                print("\n❌ Invalid option! Please try again.")
                input("\n⏎ Press Enter to continue...")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()