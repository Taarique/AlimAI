import os
from dotenv import load_dotenv

# .env ফাইল থেকে পরিবেশ ভেরিয়েবলগুলো লোড করে
load_dotenv()

# টেলিগ্রাম বট টোকেন
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# জেমিনি এপিআই কী
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# আপনি এখানে অন্যান্য কনফিগারেশন ভেরিয়েবল যোগ করতে পারেন
# যেমন:
# DATABASE_PATH = os.getenv("DATABASE_PATH", "alimai_data.db")
# DEFAULT_WELCOME_MESSAGE = "আসসালামু আলাইকুম..."
