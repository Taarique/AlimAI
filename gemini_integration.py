# AlimAI_bot/gemini_integration.py

import google.generativeai as genai
from config import GEMINI_API_KEY
import logging

logger = logging.getLogger(__name__)

# জেমিনি API কী কনফিগার করুন
genai.configure(api_key=GEMINI_API_KEY)

# মডেল ইনিশিয়ালাইজ করুন (আপনার প্রয়োজন অনুযায়ী Gemini Pro বা 2.5 Flash ব্যবহার করুন)
# আপনার পছন্দের মডেলের নাম এখানে দিন, যেমন 'gemini-2.5-flash' বা 'gemini-pro'
# 'list_available_models_for_debug()' ফাংশনটি ব্যবহার করে নিশ্চিত হয়ে নিন সঠিক নামটি।
model = genai.GenerativeModel('gemini-2.5-flash') # উদাহরণ হিসেবে এটি রাখা হলো

# --- গুরুত্বপূর্ণ পরিবর্তন: user_conversations এখানে থাকতে হবে ---
user_conversations = {} # এই লাইনটি এখানে রাখুন, ফাংশনের বাইরে

def get_gemini_response(user_id: int, message_text: str):
    """
    জেমিনি মডেল থেকে উত্তর নিয়ে আসে এবং কনভারসেশন হিস্টরি ম্যানেজ করে।
    """
    # এখানে 'global user_conversations' লেখার প্রয়োজন নেই কারণ এটি ইতিমধ্যেই গ্লোবাল স্কোপে আছে
    # এবং আপনি সরাসরি ডিকশনারি পরিবর্তন করছেন।

    if user_id not in user_conversations:
        # নতুন চ্যাট সেশন শুরু করুন
        initial_prompt = (
            "আপনি AlimAI, একজন বিজ্ঞ ইসলামী পণ্ডিত। আপনার জ্ঞান কোরআন, হাদিস, ফিকহ, মানতিক, ইতিহাস এবং বিজ্ঞান সহ ইসলামী জ্ঞানের বিভিন্ন শাখায় বিস্তৃত। "
            "আপনার প্রতিটি উত্তর নির্ভুল, নির্ভরযোগ্য এবং শরয়ী দৃষ্টিকোণ থেকে হওয়া উচিত। শুধুমাত্র ইসলামী বিষয়ে সহায়তা করুন। "
            "যদি কোনো প্রশ্ন ইসলামী বিষয়ের বাইরে হয় বা আপনি জানেন না, তাহলে বলুন 'আমি শুধু ইসলামী বিষয়ে সহায়তা করতে পারি' অথবা 'এই বিষয়ে আমার কাছে পর্যাপ্ত তথ্য নেই'। "
            "কখনো মিথ্যা বা অনুমানভিত্তিক তথ্য দেবেন না।"
        )
        user_conversations[user_id] = model.start_chat(history=[
            {'role':'user', 'parts':[initial_prompt]},
            {'role':'model', 'parts':['আমি আপনার যেকোনো ইসলামী প্রশ্নের উত্তর দিতে প্রস্তুত।']}
        ])
        logger.info(f"নতুন চ্যাট সেশন শুরু হলো User ID: {user_id}")

    chat_session = user_conversations[user_id]

    try:
        response = chat_session.send_message(message_text)
        return response.text

    except Exception as e:
        logger.error(f"জেমিনি থেকে উত্তর আনতে সমস্যা হয়েছে: {e}")
        return "দুঃখিত, বর্তমানে আমি আপনার প্রশ্নটি প্রক্রিয়া করতে পারছি না। অনুগ্রহ করে আবার চেষ্টা করুন।"

def reset_conversation(user_id: int):
    """
    নির্দিষ্ট ব্যবহারকারীর জন্য কনভারসেশন হিস্টরি রিসেট করে।
    """
    if user_id in user_conversations:
        del user_conversations[user_id]
        logger.info(f"চ্যাট সেশন রিসেট হলো User ID: {user_id}")
    return "আপনার পূর্ববর্তী কথোপকথন মুছে ফেলা হয়েছে। এখন আপনি নতুন প্রশ্ন করতে পারেন।"

# ডেটাবেস লজিক আপাতত খালি থাকবে, কারণ এটি একটি বড় কাজ
# ...
