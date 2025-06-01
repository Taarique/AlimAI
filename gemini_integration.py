import google.generativeai as genai
from config import GEMINI_API_KEY

# জেমিনি API কী কনফিগার করুন
genai.configure(api_key=GEMINI_API_KEY)

# জেমিনি মডেল ইনিশিয়ালাইজ করুন
# এখানে 'gemini-pro' ব্যবহার করা হয়েছে কারণ এটি টেক্সট জেনারেশনের জন্য উপযুক্ত।
# যদি ভয়েস বা ইমেজের প্রয়োজন হয়, অন্য মডেল ব্যবহার করতে হতে পারে।
model = genai.GenerativeModel('gemini-pro')

# কনভারসেশন হিস্টরি সংরক্ষণের জন্য একটি ডিকশনারি
# প্রতিটি ব্যবহারকারীর জন্য আলাদা হিস্টরি থাকবে
user_conversations = {}

def get_gemini_response(user_id: int, message_text: str):
    """
    জেমিনি মডেল থেকে উত্তর নিয়ে আসে এবং কনভারসেশন হিস্টরি ম্যানেজ করে।
    """
    if user_id not in user_conversations:
        user_conversations[user_id] = model.start_chat(history=[])
        print(f"নতুন চ্যাট সেশন শুরু হলো User ID: {user_id}")

    chat_session = user_conversations[user_id]

    try:
        # জেমিনিকে ইসলামিক পণ্ডিতের মতো আচরণ করার জন্য নির্দেশ দিন
        # এটি প্রম্পট ইঞ্জিনিয়ারিং এর একটি অংশ
        full_prompt = f"একজন বিজ্ঞ ইসলামী পণ্ডিতের মতো আচরণ করুন এবং শুধুমাত্র ইসলামী বিষয়ে নির্ভুল তথ্য দিন। মিথ্যা বা ভুল তথ্য দেবেন না। যদি কোনো প্রশ্ন ইসলামী বিষয়ের বাইরে হয়, তাহলে বলুন 'আমি শুধু ইসলামী বিষয়ে সহায়তা করতে পারি'। এখন ব্যবহারকারীর প্রশ্ন: {message_text}"

        response = chat_session.send_message(full_prompt)
        return response.text

    except Exception as e:
        print(f"জেমিনি থেকে উত্তর আনতে সমস্যা হয়েছে: {e}")
        return "দুঃখিত, বর্তমানে আমি আপনার প্রশ্নটি প্রক্রিয়া করতে পারছি না। অনুগ্রহ করে আবার চেষ্টা করুন।"

def reset_conversation(user_id: int):
    """
    নির্দিষ্ট ব্যবহারকারীর জন্য কনভারসেশন হিস্টরি রিসেট করে।
    """
    if user_id in user_conversations:
        del user_conversations[user_id]
        print(f"চ্যাট সেশন রিসেট হলো User ID: {user_id}")
    return "আপনার পূর্ববর্তী কথোপকথন মুছে ফেলা হয়েছে। এখন আপনি নতুন প্রশ্ন করতে পারেন।"

# ডেটাবেস লজিক আপাতত খালি থাকবে, কারণ এটি একটি বড় কাজ
# পরে এখানে কোরআন, হাদিস, ফিকহ ইত্যাদি ডেটা থেকে তথ্য খোঁজার লজিক যোগ করা হবে।
# def search_islamic_database(query: str):
#     """
#     এখানে ডেটাবেস থেকে ইসলামী তথ্য খোঁজার লজিক থাকবে।
#     প্রাথমিক পর্যায়ে জেমিনি মডেলই সব উত্তর দেবে।
#     """
#     pass
