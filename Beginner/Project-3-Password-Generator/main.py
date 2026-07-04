import random
import string
import os

class PasswordGenerator:
    def __init__(self):
        """Initialize default settings"""
        self.length = 12
        self.use_uppercase = True
        self.use_lowercase = True
        self.use_digits = True
        self.use_symbols = True
        self.generated_password = ""

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("         🔐 Password Generator")
        print("="*50)
        print(f"1. Generate Password")
        print(f"2. Set Password Length (Current: {self.length})")
        print(f"3. Toggle Uppercase (Current: {'✅' if self.use_uppercase else '❌'})")
        print(f"4. Toggle Lowercase (Current: {'✅' if self.use_lowercase else '❌'})")
        print(f"5. Toggle Digits (Current: {'✅' if self.use_digits else '❌'})")
        print(f"6. Toggle Symbols (Current: {'✅' if self.use_symbols else '❌'})")
        print("7. Show Password Strength")
        print("8. Exit")
        print("="*50)

    def toggle_option(self, option_name):
        """Toggle a boolean setting on/off"""
        if option_name == 'uppercase':
            self.use_uppercase = not self.use_uppercase
        elif option_name == 'lowercase':
            self.use_lowercase = not self.use_lowercase
        elif option_name == 'digits':
            self.use_digits = not self.use_digits
        elif option_name == 'symbols':
            self.use_symbols = not self.use_symbols

    def set_length(self):
        """Set the password length"""
        try:
            length = int(input("\n📏 Enter password length (minimum 4): "))
            if length < 4:
                print("❌ Length must be at least 4!")
                return
            self.length = length
            print(f"✅ Password length set to {length}")
        except ValueError:
            print("❌ Please enter a valid number!")

    def get_character_pool(self):
        """Build the character pool based on settings"""
        pool = ""

        if self.use_uppercase:
            pool += string.ascii_uppercase  # A-Z
        if self.use_lowercase:
            pool += string.ascii_lowercase  # a-z
        if self.use_digits:
            pool += string.digits            # 0-9
        if self.use_symbols:
            pool += string.punctuation       # !@#$%...

        return pool

    def generate_password(self):
        """Generate a random password"""
        pool = self.get_character_pool()

        if not pool:
            print("\n❌ Error: No character types selected!")
            print("Please enable at least one character type.")
            return ""

        # Generate random password
        password = ''.join(random.choice(pool) for _ in range(self.length))
        self.generated_password = password
        return password

    def calculate_strength(self, password):
        """Calculate password strength (Weak/Medium/Strong)"""
        score = 0

        # Length check
        if len(password) >= 12:
            score += 3
        elif len(password) >= 8:
            score += 2
        else:
            score += 1

        # Character diversity check
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)

        diversity = sum([has_upper, has_lower, has_digit, has_symbol])
        score += diversity

        # Determine strength
        if score >= 6:
            return "Strong 💪"
        elif score >= 4:
            return "Medium 👍"
        else:
            return "Weak ⚠️"

    def show_strength(self):
        """Display the strength of the last generated password"""
        if not self.generated_password:
            print("\n⚠️ No password generated yet!")
            print("Please generate a password first (Option 1).")
            return

        strength = self.calculate_strength(self.generated_password)
        print("\n" + "="*50)
        print("🔐 Password Strength Analysis")
        print("="*50)
        print(f"Password: {self.generated_password}")
        print(f"Length: {len(self.generated_password)} characters")
        print(f"Strength: {strength}")
        print("="*50)

    def run(self):
        """Main program loop"""
        while True:
            self.clear_screen()
            self.show_menu()

            choice = input("➡️  Choose an option: ").strip()

            if choice == '1':
                password = self.generate_password()
                if password:
                    print("\n" + "="*50)
                    print("🔑 Your Generated Password:")
                    print("="*50)
                    print(f"🔐 {password}")
                    print("="*50)
                    strength = self.calculate_strength(password)
                    print(f"Strength: {strength}")
                    print("="*50)
                input("\n⏎ Press Enter to continue...")

            elif choice == '2':
                self.set_length()
                input("\n⏎ Press Enter to continue...")

            elif choice == '3':
                self.toggle_option('uppercase')
                print(f"\n✅ Uppercase toggled to {'ON' if self.use_uppercase else 'OFF'}")
                input("\n⏎ Press Enter to continue...")

            elif choice == '4':
                self.toggle_option('lowercase')
                print(f"\n✅ Lowercase toggled to {'ON' if self.use_lowercase else 'OFF'}")
                input("\n⏎ Press Enter to continue...")

            elif choice == '5':
                self.toggle_option('digits')
                print(f"\n✅ Digits toggled to {'ON' if self.use_digits else 'OFF'}")
                input("\n⏎ Press Enter to continue...")

            elif choice == '6':
                self.toggle_option('symbols')
                print(f"\n✅ Symbols toggled to {'ON' if self.use_symbols else 'OFF'}")
                input("\n⏎ Press Enter to continue...")

            elif choice == '7':
                self.show_strength()
                input("\n⏎ Press Enter to continue...")

            elif choice == '8':
                print("\n👋 Goodbye! Stay secure!")
                break

            else:
                print("\n❌ Invalid option! Please try again.")
                input("\n⏎ Press Enter to continue...")


if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.run()