import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN, GEMINI_API_KEY
from gemini_integration import get_gemini_response, reset_conversation

# লগিং সেটআপ করুন
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)  # HTTPX লাইব্রেরির লগিং লেভেল কমানো
logger = logging.getLogger(__name__)

# --- কমান্ড এবং মেসেজ হ্যান্ডলার ফাংশনগুলো এখানে সংজ্ঞায়িত করুন (main() ফাংশনের আগে) ---

async def start(update: Update, context):
    """বট শুরু হলে স্বাগতম বার্তা পাঠায়।"""
    user_name = update.effective_user.first_name
    welcome_message = (
        f"আসসালামু আলাইকুম ওয়া রাহমাতুল্লাহ, {user_name}!\n\n"
        "আমি AlimAI, আপনার ইসলামী জ্ঞান অর্জনের ডিজিটাল সঙ্গী। "
        "কোরআন, হাদিস, ফিকহ, মানতিক, ইতিহাস এবং বিজ্ঞান সহ ইসলামী জ্ঞানের বিভিন্ন বিষয়ে আপনাকে সহায়তা করতে আমি প্রস্তুত।\n\n"
        "আপনি যে প্রশ্ন করতে চান তা পাঠান। \n\n/restart বা /reset দিয়ে কনভারসেশন পুনরায় শুরু করতে পারেন।"
    )
    await update.message.reply_text(welcome_message)

async def reset(update: Update, context):
    """কনভারসেশন রিসেট করে।"""
    reset_conversation()
    await update.message.reply_text("♻️ কনভারসেশন রিসেট হয়েছে। এখন আপনি নতুন প্রশ্ন করতে পারেন ইনশাআল্লাহ।")

async def handle_message(update: Update, context):
    """ব্যবহারকারীর মেসেজের উত্তর দেয়।"""
    user_input = update.message.text
    response = get_gemini_response(user_input)
    await update.message.reply_text(response)

def main():
    """মূল বট চালানোর ফাংশন"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("restart", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 AlimAI Bot শুরু হয়েছে...")
    app.run_polling()

if __name__ == "__main__":
    main()
