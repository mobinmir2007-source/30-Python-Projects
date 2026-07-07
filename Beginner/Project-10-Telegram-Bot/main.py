import os
import json
import re
import requests
from datetime import datetime


class TelegramBot:
    def __init__(self):
        # ===== Data =====
        self.history = []
        self.filename = "chat_history.json"
        self.last_update_id = 0
        self.load_data()
        
        # ===== Bot Settings =====
        self.token = "YOUR_BOT_TOKEN_HERE"  # ← Replace with your bot token
        self.bot_url = f"https://api.telegram.org/bot{self.token}"
        
        # ===== Regex Patterns (for command detection) =====
        self.patterns = {
            'start': re.compile(r'^/start$'),
            'help': re.compile(r'^/help$'),
            'weather': re.compile(r'^/weather\s+(.+)$'),
            'name': re.compile(r'^/name\s+(.+)$'),
            'phone': re.compile(r'09\d{9}'),
            'email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
        }

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_data(self):
        """Load chat history from JSON file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []

    def save_data(self):
        """Save chat history to JSON file"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    def show_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("         🤖 Telegram Bot")
        print("="*50)
        print("1. Run Bot")
        print("2. Show History")
        print("3. Clear History")
        print("4. Exit")
        print("="*50)

    # ==========================================
    # Telegram API Methods
    # ==========================================
    def bot_send_message(self, chat_id, text):
        """
        Send a message using the Telegram bot API
        
        Args:
            chat_id: User's chat ID
            text: Message text to send
        
        Returns:
            API response or None if error
        """
        url = f"{self.bot_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.json()
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def bot_get_updates(self, offset=None):
        """
        Get new messages from Telegram API
        
        Args:
            offset: Last update ID to fetch messages after
        
        Returns:
            List of new updates or empty list if error
        """
        url = f"{self.bot_url}/getUpdates"
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset
        
        try:
            response = requests.get(url, params=params, timeout=35)
            return response.json().get('result', [])
        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    # ==========================================
    # Message Processing
    # ==========================================
    def process_message(self, message):
        """
        Process incoming message and generate response
        
        Args:
            message: Message object from Telegram
        
        Returns:
            Response text or None
        """
        text = message.get('text', '')
        chat_id = message['chat']['id']
        username = message.get('from', {}).get('username', 'Unknown')
        
        # Save to history
        self.history.append({
            "username": username,
            "text": text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_data()
        
        print(f"📩 {username}: {text}")
        
        # ===== Command Detection using Regex =====
        
        # 1. /start command
        if self.patterns['start'].match(text):
            return f"👋 Hello {username}! Welcome to the bot!"
        
        # 2. /help command
        if self.patterns['help'].match(text):
            return """📖 Help:
/start - Start the bot
/help - Show this help
/weather [city] - Get weather
/name [name] - Save your name"""
        
        # 3. /weather command
        weather_match = self.patterns['weather'].match(text)
        if weather_match:
            city = weather_match.group(1)
            return f"🌤️ Weather in {city}: 25°C, Sunny"
        
        # 4. /name command
        name_match = self.patterns['name'].match(text)
        if name_match:
            name = name_match.group(1)
            return f"✅ Your name: {name}"
        
        # 5. Detect phone number
        phone = self.patterns['phone'].search(text)
        if phone:
            return f"📱 Your phone number: {phone.group()}"
        
        # 6. Detect email
        email = self.patterns['email'].search(text)
        if email:
            return f"📧 Your email: {email.group()}"
        
        # 7. Default response
        return "🤔 I didn't understand! Type /help for commands."

    # ==========================================
    # Bot Main Loop
    # ==========================================
    def run_bot(self):
        """Main bot loop - keeps the bot running"""
        print("\n" + "="*50)
        print("🤖 Bot is running... Press Ctrl+C to stop")
        print("="*50)
        
        while True:
            try:
                updates = self.bot_get_updates(offset=self.last_update_id + 1)
                
                for update in updates:
                    message = update.get('message')
                    if message and message.get('text'):
                        chat_id = message['chat']['id']
                        response = self.process_message(message)
                        if response:
                            self.bot_send_message(chat_id, response)
                        self.last_update_id = update['update_id']
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    # ==========================================
    # History Management
    # ==========================================
    def show_history(self):
        """Display chat history"""
        if not self.history:
            print("\n📭 History is empty!")
            return
        
        print("\n" + "="*60)
        print("📜 Chat History")
        print("="*60)
        for i, entry in enumerate(self.history[-10:], 1):
            print(f"{i}. [{entry['username']}]: {entry['text'][:50]}")
        print("="*60)

    def clear_history(self):
        """Clear all chat history with confirmation"""
        confirm = input("\n⚠️ Clear history? (y/n): ")
        if confirm.lower() == 'y':
            self.history = []
            self.save_data()
            print("✅ History cleared!")

    # ==========================================
    # Main Program Loop
    # ==========================================
    def run(self):
        """Main program loop"""
        while True:
            self.clear_screen()
            self.show_menu()
            
            choice = input("➡️  Choose an option: ").strip()
            
            if choice == '1':
                self.run_bot()
            elif choice == '2':
                self.show_history()
                input("\n⏎ Press Enter to continue...")
            elif choice == '3':
                self.clear_history()
                input("\n⏎ Press Enter to continue...")
            elif choice == '4':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid option!")
                input("\n⏎ Press Enter to continue...")


if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()