import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from gemini_integration import get_gemini_response, reset_conversation

# লগিং সেটআপ করুন
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING) # HTTPX লাইব্রেরির লগিং লেভেল কমানো
logger = logging.getLogger(__name__)

# --- কমান্ড হ্যান্ডলার্স ---

async def start(update: Update, context):
    """বট শুরু হলে স্বাগতম বার্তা পাঠায়।"""
    user_name = update.effective_user.first_name
    welcome_message = (
        f"আসসালামু আলাইকুম ওয়া রাহমাতুল্লাহ, {user_name}!\n\n"
        "আমি AlimAI, আপনার ইসলামী জ্ঞান অর্জনের ডিজিটাল সঙ্গী। "
        "কোরআন, হাদিস, ফিকহ, মানতিক, ইতিহাস এবং বিজ্ঞান সহ ইসলামী জ্ঞানের বিভিন্ন বিষয়ে আপনাকে সহায়তা করতে আমি প্রস্তুত।\n\n"
        "যেকোনো ইসলামী বিষয়ে জানতে আমাকে প্রশ্ন করুন। "
        "আপনি যদি নতুন প্রশ্ন করতে চান, তাহলে `/reset` কমান্ড ব্যবহার করতে পারেন।"
    )
    await update.message.reply_text(welcome_message)
    logger.info(f"User {user_name} started the bot (ID: {update.effective_user.id}).")

async def ask_command(update: Update, context):
    """/ask কমান্ড ব্যবহার করে প্রশ্ন গ্রহণ করে এবং AlimAI থেকে উত্তর দেয়।"""
    user_id = update.effective_user.id
    query = " ".join(context.args) # /ask এর পরে যা আছে তা প্রশ্ন হিসেবে নেয়

    if not query:
        await update.message.reply_text(
            "অনুগ্রহ করে `/ask` এর পরে আপনার প্রশ্নটি লিখুন।\n"
            "উদাহরণ: `/ask সালাতের ফরয কয়টি?`"
        )
        return

    logger.info(f"User {user_id} asked (via /ask): {query}")
    await update.message.reply_text("আপনার প্রশ্ন প্রক্রিয়া করা হচ্ছে... একটু অপেক্ষা করুন।")

    response_text = get_gemini_response(user_id, query)

    await update.message.reply_text(response_text + "\n\nআপনার কি এই বিষয়ে আরও কিছু জানার আছে, নাকি অন্য কোনো প্রশ্ন আছে?")
    logger.info(f"Answered for user {user_id}: {response_text[:100]}...") # প্রথম ১০০ অক্ষর দেখাবে

async def reset_command(update: Update, context):
    """ব্যবহারকারীর জন্য কথোপকথন ইতিহাস রিসেট করে।"""
    user_id = update.effective_user.id
    response = reset_conversation(user_id)
    await update.message.reply_text(response + "\nএখন আপনি নতুন প্রশ্ন করতে পারেন।")
    logger.info(f"User {user_id} reset the conversation.")

# --- মেসেজ হ্যান্ডলার্স ---

async def handle_message(update: Update, context):
    """সাধারণ মেসেজ (টেক্সট) গ্রহণ করে এবং AlimAI থেকে উত্তর দেয়।"""
    user_id = update.effective_user.id
    message_text = update.message.text

    if not message_text:
        return # খালি মেসেজ উপেক্ষা করুন

    logger.info(f"User {user_id} sent message: {message_text}")
    await update.message.reply_text("আপনার প্রশ্ন প্রক্রিয়া করা হচ্ছে... একটু অপেক্ষা করুন।")

    response_text = get_gemini_response(user_id, message_text)

    await update.message.reply_text(response_text + "\n\nআপনার কি এই বিষয়ে আরও কিছু জানার আছে, নাকি অন্য কোনো প্রশ্ন আছে?")
    logger.info(f"Answered for user {user_id}: {response_text[:100]}...")


def main():
    """বট শুরু করার মূল ফাংশন।"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set. Please set it in your .env file.")
        return
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY environment variable is not set. Please set it in your .env file.")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # কমান্ড হ্যান্ডলার যোগ করুন
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", ask_command))
    application.add_handler(CommandHandler("reset", reset_command))

    # সাধারণ টেক্সট মেসেজ হ্যান্ডলার যোগ করুন (কমান্ড ব্যতীত)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # বটের জন্য পোলিং শুরু করুন
    logger.info("AlimAI Bot started polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
