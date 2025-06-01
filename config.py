import os
from dotenv import load_dotenv

# .env ফাইল থেকে পরিবেশ ভেরিয়েবলগুলো লোড করে
# এটি নিশ্চিত করে যে আপনার API কীগুলো সরাসরি কোডে নেই।
load_dotenv()

# টেলিগ্রাম বট টোকেন
# এটি TELEGRAM_BOT_TOKEN নামের পরিবেশ ভেরিয়েবল থেকে মান নেয়।
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# জেমিনি এপিআই কী
# এটি GEMINI_API_KEY নামের পরিবেশ ভেরিয়েবল থেকে মান নেয়।
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# আপনি এখানে আরও অন্যান্য কনফিগারেশন ভেরিয়েবল যোগ করতে পারেন,
# যেমন ডেটাবেস পাথ বা ডিফল্ট মেসেজ।
# DATABASE_PATH = os.getenv("DATABASE_PATH", "alimai_data.db")
# DEFAULT_WELCOME_MESSAGE = "আসসালামু আলাইকুম..."
