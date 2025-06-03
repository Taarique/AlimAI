import google.generativeai as genai
import logging
import os

# লগিং কনফিগারেশন
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gemini_integration")

# Gemini API কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# গ্লোবাল model ও chat session
model = genai.GenerativeModel("gemini-1.5-flash")
chat_session = model.start_chat(history=[])

def get_gemini_response(prompt: str) -> str:
    global chat_session
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        logger.error(f"জেমিনি থেকে উত্তর আনতে সমস্যা হয়েছে: {e}")
        return "দুঃখিত, আমি এখন উত্তর দিতে পারছি না।"

def reset_conversation():
    global chat_session
    chat_session = model.start_chat(history=[])
    logger.info("✅ কনভারসেশন রিসেট হয়েছে।")
