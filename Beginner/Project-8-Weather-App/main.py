import os
import json
import requests
from datetime import datetime


class WeatherApp:
    def __init__(self):
        self.api_key = "YOUR_API_KEY"   
        self.base_url = "https://api.openweathermap.org/data/2.5/weather" 
        self.history = []
        self.filename = "weather_history.json"
        self.load_history()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_history(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []

    def save_history(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    def show_menu(self):
        print("\n" + "="*50)
        print("         🌤️  Weather App")
        print("="*50)
        print("1. Get Weather by City")
        print("2. Show History")
        print("3. Clear History")
        print("4. Exit")
        print("="*50)

    def get_weather(self, city):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                weather_info = {
                    "city": data['name'],
                    "country": data['sys']['country'],
                    "temperature": data['main']['temp'],
                    "feels_like": data['main']['feels_like'],
                    "humidity": data['main']['humidity'],
                    "description": data['weather'][0]['description'].capitalize(),
                    "wind_speed": data['wind']['speed'],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                return weather_info
                
            elif response.status_code == 404:
                print(f"❌ City '{city}' not found!")
                return None
            elif response.status_code == 401:
                print("❌ Invalid API key! Please check your key.")
                return None
            else:
                print(f"❌ Error: {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError:
            print("❌ No internet connection!")
            return None
        except requests.exceptions.Timeout:
            print("❌ Request timed out!")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None
        except ValueError:
            print("❌ Invalid response from server!")
            return None

    def display_weather(self, weather):
        print("\n" + "="*50)
        print(f"🌍 Weather in {weather['city']}, {weather['country']}")
        print("="*50)
        print(f"🌡️  Temperature: {weather['temperature']}°C")
        print(f"🤔 Feels like: {weather['feels_like']}°C")
        print(f"💧 Humidity: {weather['humidity']}%")
        print(f"🌤️  Condition: {weather['description']}")
        print(f"💨 Wind Speed: {weather['wind_speed']} m/s")
        print("="*50)

    def add_to_history(self, weather):
        self.history.append(weather)
        self.save_history()

    def show_history(self):
        if not self.history:
            print("\n📭 History is empty!")
            return
        print("\n" + "="*60)
        print("📜 Weather History")
        print("="*60)
        for i, entry in enumerate(self.history, 1):
            print(f"{i}. {entry['city']}, {entry['country']}")
            print(f"   🌡️  {entry['temperature']}°C | 💧 {entry['humidity']}%")
            print(f"   🌤️  {entry['description']}")
            print(f"   🕐 {entry['timestamp']}")
            print("-" * 60)

    def clear_history(self):
        if not self.history:
            print("\n📭 History is already empty!")
            return
        confirm = input("\n⚠️ Are you sure? (y/n): ")
        if confirm.lower() == 'y':
            self.history = []
            self.save_history()
            print("✅ History cleared!")
        else:
            print("❌ Cancelled.")

    def run(self):
        while True:
            self.clear_screen()
            self.show_menu()
            choice = input("➡️  Choose an option: ").strip()

            if choice == '1':
                city = input("\n🏙️  Enter city name: ").strip()
                if not city:
                    print("❌ City name cannot be empty!")
                    input("\n⏎ Press Enter to continue...")
                    continue
                print(f"\n⏳ Fetching weather for {city}...")
                weather = self.get_weather(city)
                if weather:
                    self.display_weather(weather)
                    self.add_to_history(weather)
                    print("\n💾 Weather data saved to history!")
                input("\n⏎ Press Enter to continue...")

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
    app = WeatherApp()
    app.run()