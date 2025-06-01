# AlimAI_bot/gemini_integration.py

import google.generativeai as genai
from config import GEMINI_API_KEY # নিশ্চিত করুন যে GEMINI_API_KEY ঠিকভাবে ইম্পোর্ট হচ্ছে
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)

# এখানে মডেলের নাম পরিবর্তন করুন:
# model = genai.GenerativeModel('gemini-pro') # এই লাইনটি পরিবর্তন করুন

# Gemini 2.5 Flash ব্যবহার করার জন্য:
# প্রথমে এটি চেষ্টা করুন (যদি GA হয়ে থাকে):
# model = genai.GenerativeModel('gemini-2.5-flash')

# যদি উপরেরটি কাজ না করে, তাহলে প্রিভিউ সংস্করণটি ব্যবহার করুন:
model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

def get_gemini_response(user_id: int, message_text: str):
    """
    জেমিনি মডেল থেকে উত্তর নিয়ে আসে এবং কনভারসেশন হিস্টরি ম্যানেজ করে।
    """
    if user_id not in user_conversations:
        # নতুন চ্যাট সেশন শুরু করুন
        # মডেলকে ইসলামী পণ্ডিতের মতো আচরণ করার জন্য প্রাথমিক নির্দেশনা দিন
        initial_prompt = (
            "আপনি AlimAI, একজন বিজ্ঞ ইসলামী পণ্ডিত। আপনার জ্ঞান কোরআন, হাদিস, ফিকহ, মানতিক, ইতিহাস এবং বিজ্ঞান সহ ইসলামী জ্ঞানের বিভিন্ন শাখায় বিস্তৃত। "
            "আপনার প্রতিটি উত্তর নির্ভুল, নির্ভরযোগ্য এবং শরয়ী দৃষ্টিকোণ থেকে হওয়া উচিত। শুধুমাত্র ইসলামী বিষয়ে সহায়তা করুন। "
            "যদি কোনো প্রশ্ন ইসলামী বিষয়ের বাইরে হয় বা আপনি জানেন না, তাহলে বলুন 'আমি শুধু ইসলামী বিষয়ে সহায়তা করতে পারি' অথবা 'এই বিষয়ে আমার কাছে পর্যাপ্ত তথ্য নেই'। "
            "কখনো মিথ্যা বা অনুমানভিত্তিক তথ্য দেবেন না।"
        )
        user_conversations[user_id] = model.start_chat(history=[
            {'role':'user', 'parts':[initial_prompt]},
            {'role':'model', 'parts':['আমি আপনার যেকোনো ইসলামী প্রশ্নের উত্তর দিতে প্রস্তুত।']} # মডেলের একটি প্রারম্ভিক উত্তর
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
# ভবিষ্যতে এখানে কোরআন, হাদিস, ফিকহ ইত্যাদি ডেটা থেকে তথ্য খোঁজার লজিক যোগ করা হবে।
# def search_islamic_database(query: str):
#     """
#     এখানে ডেটাবেস থেকে ইসলামী তথ্য খোঁজার লজিক থাকবে।
#     """
#     pass
