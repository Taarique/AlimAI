import google.generativeai as genai
import logging
import os

# লগিং কনফিগারেশন
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gemini_integration")

# API কী কনফিগারেশন
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(prompt: str) -> str:
    try:
        # সঠিক মডেল এবং API ভার্সন ব্যবহার
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"জেমিনি থেকে উত্তর আনতে সমস্যা হয়েছে: {e}")
        return "দুঃখিত, আমি এখন উত্তর দিতে পারছি না।"
