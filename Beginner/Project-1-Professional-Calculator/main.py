import math
import os

class ProfessionalCalculator:
    def __init__(self):
        self.history = []          # Calculation history list
        self.memory = 0            # Memory
        self.result = 0            # Latest result

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        # Show Menu
        print("\n" + "="*50)
        print("         🧮 Professional calculator")
        print("="*50)
        print("1. sum (+)         2. Subtraction (-)")
        print("3. Multiplication (*)         4. Division (/)")
        print("5. Power (^)        6. Square root  (√)")
        print("7. Percentage (%)        8.  View history")
        print("9. Memory (M+)     10. Clear memory (MC)")
        print("11. Exit")
        print("="*50)
        print(f"📌 Latest result: {self.result}")
        print(f"💾 Memory: {self.memory}")
        print("="*50)

    def get_number(self, prompt="Enter the Number: "):
        # Error Handling
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("❌ Error: Please enter a valid number.!")

    def add_to_history(self, operation, expression, result):
        # Add calculation to history
        self.history.append({
            'operation': operation,
            'expression': expression,
            'result': result
        })

    def show_history(self):
        # View calculation history
        if not self.history:
            print("\n📭 History is empty!")
            return
        
        print("\n" + "="*50)
        print("📜  History of Computing:")
        print("="*50)
        for i, item in enumerate(self.history, 1):
            print(f"{i}. {item['expression']} = {item['result']}")
        print("="*50)

    def run(self):
        # The main loop of the program
        while True:
            self.clear_screen()
            self.show_menu()
            
            choice = input("➡️  Choose the Number :").strip()

            # Exit the program            
            if choice == '11':
                print("\n👋 Goodbye! Thank you for using it.")
                break

            # Show history
            if choice == '8':
                self.show_history()
                input("\n⏎ Click to continue...")
                continue

            # Clear memory
            if choice == '10':
                self.memory = 0
                print("\n✅ Memory erased!")
                input("\n⏎ Click to continue...")
                continue

            # Memory operations (M+)
            if choice == '9':
                print(f"\n The number {self.result} was added to memory.")
                self.memory += self.result
                input("\n⏎ Click to continue...")
                continue

            # Perform mathematical operations
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                try:
                    # Get numbers (except square root and percentage which take a number)
                    if choice in ['6', '7']:
                        num = self.get_number("Enter the Number: ")
                        num2 = None
                    else:
                        num = self.get_number("one number: ")
                        num2 = self.get_number("two number: ")

                    # Perform calculation                    
                    if choice == '1':  # Sum
                        result = num + num2
                        expression = f"{num} + {num2}"
                        op_name = "Sum"
                    elif choice == '2':  # Subtraction
                        result = num - num2
                        expression = f"{num} - {num2}"
                        op_name = "Subtraction"
                    elif choice == '3':  # Multiplication
                        result = num * num2
                        expression = f"{num} * {num2}"
                        op_name = "Multiplication"
                    elif choice == '4':  # Division
                        if num2 == 0:
                            print("❌ Error: Division by zero is not possible!")
                            input("\n⏎ Click to continue...")
                            continue
                        result = num / num2
                        expression = f"{num} / {num2}"
                        op_name = "Division"
                    elif choice == '5':  # Power
                        result = num ** num2
                        expression = f"{num} ^ {num2}"
                        op_name = "Power"
                    elif choice == '6':  # Power
                        if num < 0:
                            print("❌ Error: Root of negative numbers is not possible!")
                            input("\n⏎ Click to continue...")
                            continue
                        result = math.sqrt(num)
                        expression = f"√{num}"
                        op_name = "Power"
                    elif choice == '7':  # Percentage
                        result = num / 100
                        expression = f"{num}%"
                        op_name = "Percentage"

                    # save to history and memory
                    self.result = result
                    self.add_to_history(op_name, expression, result)

                    # view result
                    print("\n" + "="*50)
                    print(f"✅ result: {expression} = {result}")
                    print("="*50)
                    
                except Exception as e:
                    print(f"\n❌ Unexpected error: {e}")                
                input("\n⏎ Click to continue...")
            
            else:
                print("\n❌ Invalid option! Please try again.")
                input("\n⏎ Click to continue...")

# Run the program
if __name__ == "__main__":
    calculator = ProfessionalCalculator()
    calculator.run()