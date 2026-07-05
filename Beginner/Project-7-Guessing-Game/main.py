import os
import json
import random


class GuessingGame:
    def __init__(self):
        """Initialize game settings and load records"""
        self.target = 0
        self.guesses = 0
        self.max_attempts = 10
        self.best_record = None
        self.filename = "record.json"
        self.load_record()

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_record(self):
        """Load best record from file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.best_record = data.get('best_record')
        except (FileNotFoundError, json.JSONDecodeError):
            self.best_record = None

    def save_record(self):
        """Save best record to file"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump({'best_record': self.best_record}, f, indent=4)

    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("         🎯 Number Guessing Game")
        print("="*50)
        print("1. Start New Game")
        print("2. View Best Record")
        print("3. Exit")
        print("="*50)

    def start_game(self):
        """Start a new game"""
        self.target = random.randint(1, 100)
        self.guesses = 0
        print("\n" + "="*50)
        print("🎮 New Game Started!")
        print("="*50)
        print(f"🔢 Guess a number between 1 and 100")
        print(f"📊 You have {self.max_attempts} attempts")
        print("="*50)

        while self.guesses < self.max_attempts:
            try:
                guess = int(input(f"\n➡️  Attempt {self.guesses + 1}: "))
                
                if guess < 1 or guess > 100:
                    print("❌ Please enter a number between 1 and 100!")
                    continue

                self.guesses += 1

                if guess == self.target:
                    print("\n" + "🎉" * 10)
                    print(f"✅ Congratulations! You guessed it in {self.guesses} attempts!")
                    print("🎉" * 10)
                    self.update_record()
                    break
                elif guess < self.target:
                    print("📈 Too low! Try a higher number.")
                else:
                    print("📉 Too high! Try a lower number.")

                remaining = self.max_attempts - self.guesses
                if remaining > 0:
                    print(f"💡 Remaining attempts: {remaining}")

            except ValueError:
                print("❌ Invalid input! Please enter a number.")

        else:
            print("\n" + "="*50)
            print(f"😞 Game Over! The number was: {self.target}")
            print("="*50)

        input("\n⏎ Press Enter to continue...")

    def update_record(self):
        """Update best record if current is better"""
        if self.best_record is None or self.guesses < self.best_record:
            self.best_record = self.guesses
            self.save_record()
            print(f"🏆 New Best Record: {self.guesses} attempts!")
        else:
            print(f"📋 Best Record: {self.best_record} attempts")

    def show_record(self):
        """Show the best record"""
        self.clear_screen()
        print("\n" + "="*40)
        if self.best_record:
            print(f"🏆 Best Record: {self.best_record} attempts")
        else:
            print("📭 No record yet! Play a game to set one.")
        print("="*40)
        input("\n⏎ Press Enter to continue...")

    def run(self):
        """Main program loop"""
        while True:
            self.clear_screen()
            self.show_menu()
            choice = input("➡️  Choose an option: ").strip()

            if choice == '1':
                self.start_game()
            elif choice == '2':
                self.show_record()
            elif choice == '3':
                print("\n👋 Goodbye! Thanks for playing!")
                break
            else:
                print("❌ Invalid option!")
                input("\n⏎ Press Enter to continue...")


if __name__ == "__main__":
    game = GuessingGame()
    game.run()