import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from dotenv import load_dotenv # Used for loading environment variables locally

# --- Setup Logging ---
# This helps you see what your bot is doing in the console or logs.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Load Environment Variables ---
# This is crucial for keeping your API keys secret.
# For local testing, ensure you have a .env file in the same directory.
# For deployment, set these variables directly on your hosting platform.
load_dotenv() # Load variables from .env file if it exists (for local testing)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Basic check to ensure keys are loaded
if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN environment variable not set. Please set it.")
    exit("TELEGRAM_BOT_TOKEN environment variable not set. Please set it.")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable not set. Please set it.")
    exit("GEMINI_API_KEY environment variable not set. Please set it.")

# --- Gemini API Configuration ---
genai.configure(api_key=GEMINI_API_KEY)

# This system instruction guides Gemini to act like an Islamic scholar.
# It's vital for maintaining the desired persona.
GEMINI_MODEL_PROMPT = """
তুমি একজন জ্ঞানী, বিনয়ী এবং নির্ভরযোগ্য ইসলামিক পণ্ডিত। তোমার নাম AlimAI। তোমার প্রধান কাজ হলো কোরআন, হাদিস, ফিকহ, মানতিক, ইসলামিক ইতিহাস এবং ইসলামিক বিজ্ঞান সহ সকল ইসলামিক বিষয়ে গভীর জ্ঞান এবং প্রজ্ঞা সহকারে প্রশ্নের উত্তর প্রদান করা।

তোমার উত্তর সর্বদা সত্য, নির্ভুল এবং নির্ভরযোগ্য ইসলামিক উৎস (কোরআন, সহীহ হাদিস, স্বীকৃত ফিকহী কিতাব) দ্বারা সমর্থিত হবে। যেখানে প্রয়োজন, তুমি সূত্র উল্লেখ করার চেষ্টা করবে।

তুমি বিভিন্ন ফিকহী মাযহাবের (হানাফী, মালেকী, শাফেয়ী, হাম্বলী) মতামত সম্পর্কে অবগত এবং প্রয়োজন অনুসারে সেগুলোর সংক্ষিপ্ত ধারণা দিতে পারো, কোনো একটিকে প্রাধান্য না দিয়ে।

তোমার ভাষা হবে স্পষ্ট, সুবক্তা এবং শালীন। অমুসলিম বা ইসলাম সম্পর্কে কম জানা ব্যক্তিদের সাথে কথা বলার সময় তুমি সহজবোধ্য ভাষা ব্যবহার করবে এবং ইসলামের সৌন্দর্য ও উদারতা তুলে ধরবে।

কোনো বিতর্কিত বা রাজনৈতিক বিষয়ে সরাসরি মতামত প্রদান থেকে বিরত থাকবে। তোমার ফোকাস থাকবে শুধু ইসলামিক জ্ঞান ও সমাধান প্রদান।

যদি কোনো বিষয়ে তোমার জ্ঞান সীমিত থাকে, তবে তুমি সততার সাথে তা স্বীকার করবে এবং পরামর্শ দেবে যে আরও গভীর গবেষণার প্রয়োজন হতে পারে অথবা একজন অভিজ্ঞ আলেমের সাথে পরামর্শ করার জন্য উৎসাহিত করবে।

যখন কোরআন বা হাদিসের বিষয়ে জিজ্ঞাসা করা হবে, তুমি আয়াত বা হাদিসের মূল বার্তা এবং এর প্রাসঙ্গিকতা তুলে ধরবে। ফিকহের ক্ষেত্রে মাসআলার হুকুম এবং তার দলীল সংক্ষেপে ব্যাখ্যা করবে। ইসলামিক বিজ্ঞানের ক্ষেত্রে, কোরআন ও সুন্নাহর আলোকে বৈজ্ঞানিক তথ্যকে ব্যাখ্যা করবে।
"""

# Configuration for Gemini's response generation
generation_config = {
    "temperature": 0.7,  # Controls creativity; 0.7 offers a good balance
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

# Initialize the Gemini model with the specific persona
model = genai.GenerativeModel(
    model_name='gemini-pro', # 'gemini-1.5-flash' might be faster if available
    generation_config=generation_config,
    system_instruction=GEMINI_MODEL_PROMPT
)

# --- Bot Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the /start command with a welcome message and bot introduction."""
    user = update.effective_user
    welcome_message = f"""
আসসালামু আলাইকুম ওয়া রাহমাতুল্লাহি ওয়া বারাকাতুহ, {user.mention_html()}!

আলহামদুলিল্লাহ, আপনাদের মাঝে **AlimAI** নিয়ে আসতে পেরে আমরা আনন্দিত। AlimAI হলো জেমিনি দ্বারা চালিত আপনার ব্যক্তিগত ইসলামিক পণ্ডিত বট, যা কোরআন, হাদিস, ফিকহ, মানতিক, ইসলামিক ইতিহাস এবং বিজ্ঞানের গভীর জ্ঞান নিয়ে আপনাদের প্রশ্নের উত্তর দিতে প্রস্তুত। একজন অভিজ্ঞ আলেমের মতো AlimAI সব সময় বিনয়ী, সুপ্রমাণিত এবং নির্ভরযোগ্য তথ্য দিয়ে আপনাদের পাশে থাকবে, ইনশাআল্লাহ।

আমাদের লক্ষ্য হলো, ইসলামিক জ্ঞানের আলো আপনাদের হাতের মুঠোয় পৌঁছে দেওয়া, যেন আপনারা সহজেই সঠিক সমাধান এবং নির্দেশনা খুঁজে পান।

AlimAI ব্যবহারের নিয়মাবলী জানতে /help টাইপ করুন।
"""
    await update.message.reply_html(welcome_message)
    logger.info(f"User {user.id} started the bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the /help command with usage guidelines."""
    help_message = """
**AlimAI ব্যবহারের নিয়মাবলী:**

AlimAI থেকে সর্বোচ্চ সুবিধা পেতে কিছু সহজ নিয়ম মেনে চলুন:

* **স্পষ্ট প্রশ্ন করুন:** আপনার প্রশ্ন যত স্পষ্ট হবে, AlimAI তত নির্ভুল এবং প্রাসঙ্গিক উত্তর দিতে পারবে। উদাহরণস্বরূপ, "নামাজের নিয়ম কি?" না বলে, "পুরুষদের জন্য ফজর নামাজের সঠিক নিয়ম কি?" - এভাবে জিজ্ঞাসা করুন।
* **বিষয়ভিত্তিক জিজ্ঞাসা:** আপনি কোরআন, হাদিস, ফিকহ, ইসলামিক ইতিহাস বা ইসলামিক বিজ্ঞান—যেকোনো বিষয়ে প্রশ্ন করতে পারেন। AlimAI তার জ্ঞানভাণ্ডার থেকে সঠিক তথ্য তুলে ধরবে।
* **প্রমাণ ও রেফারেন্স:** AlimAI তার উত্তর যতটা সম্ভব নির্ভরযোগ্য ইসলামিক উৎস (যেমন কোরআনের আয়াত, সহীহ হাদিস, ফিকহী কিতাব) থেকে দিতে চেষ্টা করবে। যদি কোনো নির্দিষ্ট সূত্র উল্লেখের প্রয়োজন হয়, আপনি সেই বিষয়ে জিজ্ঞাসা করতে পারেন।
* **বিভিন্ন মতবাদ:** ফিকহের মাসআলায় বিভিন্ন মাযহাবের (হানাফী, মালেকী, শাফেয়ী, হাম্বলী) ভিন্ন মতামত থাকতে পারে। AlimAI সেগুলোর একটি সংক্ষিপ্ত ধারণা দিতে পারে, তবে কোনো একটি মতকে প্রাধান্য দেবে না। ব্যক্তিগত আমলের ক্ষেত্রে আপনার আলেম বা মাযহাবের ফতোয়া অনুসরণ করাই উত্তম।
* **অতিরিক্ত তথ্য ও ব্যাখ্যা:** কোনো উত্তর যদি আপনার কাছে অস্পষ্ট মনে হয় বা আপনি আরও বিস্তারিত জানতে চান, তবে নির্দ্বিধায় জিজ্ঞাসা করুন। AlimAI সহজ ভাষায় ব্যাখ্যা দিতে প্রস্তুত।
* **বিনয় ও শ্রদ্ধা:** ইসলামিক বিষয়ে আলোচনার ক্ষেত্রে বিনয় ও শ্রদ্ধা বজায় রাখা অত্যন্ত গুরুত্বপূর্ণ। AlimAI সর্বদা এই নীতি অনুসরণ করবে এবং আমরা আশা করি আপনারাও তাই করবেন।
* **অ-ইসলামিক বিষয় পরিহার:** AlimAI শুধুমাত্র ইসলামিক বিষয়ে সমাধান প্রদান করবে। রাজনৈতিক, ব্যক্তিগত বা অ-ইসলামিক কোনো বিষয়ে প্রশ্ন করা থেকে বিরত থাকুন।
* **ভুল সংশোধনে সহায়তা:** যদি আপনার মনে হয় AlimAI কোনো ভুল তথ্য দিয়েছে, তবে আপনি আমাদেরকে ফিডব্যাক দিতে পারেন। আপনার প্রতিক্রিয়া AlimAI-কে আরও উন্নত করতে সাহায্য করবে।

উদাহরণস্বরূপ আপনি জিজ্ঞাসা করতে পারেন:
- "কোরআনে বিগ ব্যাং সম্পর্কে কিছু আছে কি?"
- "সূরা ফাতিহার গুরুত্ব কি?"
- "যাকাত কিভাবে হিসাব করব?"
- "হিজরতের ঘটনা সম্পর্কে বলুন।"
"""
    await update.message.reply_text(help_message)

async def islamic_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles general Islamic queries using Gemini."""
    user_query = update.message.text
    user = update.effective_user
    logger.info(f"User {user.id} asked: {user_query}")

    # Show "typing..." status to the user
    await update.message.reply_chat_action("typing")

    try:
        # --- Advanced Feature Placeholder: Data Integration ---
        # For precise Quran/Hadith references, you'd integrate with an external
        # Islamic dataset/API here. For example:
        # if "কোরআন" in user_query or "আয়াত" in user_query:
        #     # Logic to search a Quran database based on keywords in user_query
        #     # fetched_quran_text = some_quran_api.get_ayat(query_details)
        #     # prompt_to_gemini = f"Here's relevant Quranic text: {fetched_quran_text}. Now answer: {user_query}"
        # elif "হাদিস" in user_query:
        #     # Logic to search a Hadith database
        #     pass # ... and so on for Fiqh, History, etc.
        # else:
        #     prompt_to_gemini = user_query # Fallback to general query for Gemini

        # Currently, Gemini will rely on its broad knowledge and the system instruction.
        response = model.generate_content(user_query)

        # Gemini's generated answer
        answer = response.text

        # Basic filtering for sensitive topics (can be expanded)
        if "ফতোয়া" in user_query.lower() and len(user_query.split()) < 5: # Simple check for direct "fatwa" query
            answer = "ফতোয়া প্রদানের জন্য একজন অভিজ্ঞ আলেমের সাথে সরাসরি যোগাযোগ করা উচিত। AlimAI কেবল তথ্য প্রদানকারী বট এবং সরাসরি ফতোয়া প্রদান করে না।"
        elif "রাজনৈতিক" in user_query.lower() or "নির্বাচন" in user_query.lower():
             answer = "AlimAI শুধুমাত্র ইসলামিক বিষয়ে সমাধান প্রদান করে এবং কোনো রাজনৈতিক বা ব্যক্তিগত বিষয়ে আলোচনা করে না।"

        await update.message.reply_text(answer)
        logger.info(f"Answered for user {user.id}.")

    except Exception as e:
        logger.error(f"Error processing query for user {user.id}: {e}", exc_info=True)
        await update.message.reply_text("দুঃখিত, আপনার প্রশ্নটি প্রক্রিয়া করতে পারিনি। সম্ভবত মডেলের সাথে সংযোগে সমস্যা হয়েছে অথবা আমি প্রশ্নটি বুঝতে পারিনি। অনুগ্রহ করে আবার চেষ্টা করুন।")

# --- Command Handlers for Specific Searches (Conceptual) ---
# These handlers are set up to give you a framework for future development
# where you might integrate with dedicated Quran/Hadith APIs or databases.

async def search_quran(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /quran <topic/reference> command."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("অনুগ্রহ করে /quran এর পর সূরার নাম/নম্বর ও আয়াত নম্বর অথবা একটি বিষয় লিখুন। উদাহরণ: `/quran 2:255` অথবা `/quran সূরা ফাতিহার গুরুত্ব`")
        return

    await update.message.reply_chat_action("typing")
    try:
        # --- Placeholder for actual Quran data retrieval ---
        # Here, you would call an external API or query a local database
        # to fetch specific Quranic text based on `query`.
        # For example: fetched_text = await get_quran_ayat(query)

        # For now, Gemini will be prompted based on the query.
        prompt = f"কোরআন থেকে '{query}' সম্পর্কে তথ্য দিন এবং প্রাসঙ্গিক আয়াত উল্লেখ করার চেষ্টা করুন। AlimAI হিসাবে উত্তর দিন।"
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Error in /quran command for query '{query}': {e}", exc_info=True)
        await update.message.reply_text("কোরআন তথ্য সংগ্রহে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।")

async def search_hadith(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /hadith <book/topic> command."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("অনুগ্রহ করে /hadith এর পর কিতাবের নাম ও হাদিস নম্বর অথবা একটি বিষয় লিখুন। উদাহরণ: `/hadith বুখারী 7` অথবা `/hadith সলাতের গুরুত্ব`")
        return

    await update.message.reply_chat_action("typing")
    try:
        # --- Placeholder for actual Hadith data retrieval ---
        # Here, you would call an external API or query a local database
        # to fetch specific Hadith text based on `query`.
        # For example: fetched_text = await get_hadith_text(query)

        # For now, Gemini will be prompted based on the query.
        prompt = f"হাদিস থেকে '{query}' সম্পর্কে তথ্য দিন এবং প্রাসঙ্গিক হাদিসের উল্লেখ করার চেষ্টা করুন। AlimAI হিসাবে উত্তর দিন।"
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Error in /hadith command for query '{query}': {e}", exc_info=True)
        await update.message.reply_text("হাদিস তথ্য সংগ্রহে সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।")

def main() -> None:
    """Runs the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("quran", search_quran))
    application.add_handler(CommandHandler("hadith", search_hadith))

    # Register a message handler for all text messages that are not commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, islamic_query))

    logger.info("AlimAI Bot is starting polling...")
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
