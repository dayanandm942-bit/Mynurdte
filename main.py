import time
import os
import asyncio
from google import genai
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# ==========================================
# --- 1. CONFIGURATION (SUJEET KI DETAILS) ---
# ==========================================
API_ID = 34012656
API_HASH = "267f6fe3e9d163e735ad912344a529e7"
PHONE_NUMBER = "+919250751630" 

# 🔥 ADITI KI INSTA ID 🔥
IG_USERNAME = "adititiwari99877"

# 🚀 TERE GEMINI API KEYS (FOR 24/7 UNSTOPPABLE AI)
GEMINI_KEYS = [
    "AIzaSyCot0onrt2TUWUlmwRdEMa9lBneE7PPimE",
    "AIzaSyC1f4XwpTzfyvDz5nVIsOZ56NfoAFn2Eao",
    "AIzaSyDVvcRRvqJ5A2ufciPszIDK2Bnh-AIalpE",
    "AIzaSyDtQWasKFN60nnob04dkLdRTwBqbxw8eUo",
    "AIzaSyCnRZYWyRDiUJqQAUhWJBcMmDi6gT4Hz4Y",
    "AIzaSyAJbqJvR26OepEaziS5qBFoMXyH-ij5MLE",
    "AIzaSyAtdbx_IGjK9zzgOBsuR3ZDcnIBZgCJIcM"
]
current_key_index = 0
ai_client = genai.Client(api_key=GEMINI_KEYS[current_key_index])

user_memory = {}

# ==========================================
# --- 2. ANTI-SLEEP WEB SERVER ---
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Aditi ka Telegram Bot 24/7 Live Hai! 🔥😎"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.start()

# ==========================================
# --- 3. ADVANCED AI LOGIC (Aditi ka Mastermind) ---
# ==========================================
def get_aditi_reply(user_id, user_name, user_text):
    global current_key_index, ai_client, user_memory
    
    user_id_str = str(user_id)
    if user_id_str not in user_memory:
        user_memory[user_id_str] = []
        
    if len(user_memory[user_id_str]) > 10:
        user_memory[user_id_str] = user_memory[user_id_str][-10:]
        
    history_text = "\n".join(user_memory[user_id_str])
    
    prompt = f"""
    Tumhara naam Aditi hai. Tum ek 18 saal ki normal, cute aur friendly ladki ho.
    Tumhara EK HI MAIN MOTIVE hai: Samne wale ladke ko baaton mein uljha kar apne Instagram (@{IG_USERNAME}) par lana aur wahan follow karwana.

    STRICT RULES:
    1. ZERO AI VIBES: Tum ek asli ladki ho. Kabhi mat bolna ki tu AI ya bot hai.
    2. CHATTING STYLE: Ekdum natural (hmm, achha, haha, yaar, sahi hai). Short messages likho (1-2 lines).
    3. THE INSTA TRAP: Pehle 2-3 message normal baat karo. Fir bolo: "Yaar yahan TG pe main zyada active nahi rehti, tum Insta chalate ho? Wahan aa jao: @{IG_USERNAME}"
    4. FOCUS: Baaton ko ghuma kar hamesha Instagram follow karwane par le jao.

    --- PURANI BAATEIN ---
    {history_text}

    --- NAYA MESSAGE ---
    {user_name}: {user_text}
    Aditi ka natural reply:
    """
    
    for attempt in range(len(GEMINI_KEYS)):
        try:
            response = ai_client.models.generate_content(
                model='gemini-1.5-flash-latest',
                contents=prompt,
            )
            reply = response.text.strip()
            
            user_memory[user_id_str].append(f"{user_name}: {user_text}")
            user_memory[user_id_str].append(f"Aditi: {reply}")
            return reply
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                current_key_index = (current_key_index + 1) % len(GEMINI_KEYS)
                ai_client = genai.Client(api_key=GEMINI_KEYS[current_key_index])
            else:
                break 
                
    return f"Yaar mera net rula raha hai... tum ek kaam karo mujhe Insta pe hi msg kar do: @{IG_USERNAME}"

# ==========================================
# --- 4. TELETHON ENGINE ---
# ==========================================
# Ye file 'aditi_session.session' ko use karega jo tune upload ki hai
client = TelegramClient('aditi_session', API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_new_message(event):
    sender = await event.get_sender()
    if sender.is_self: return
        
    user_id = sender.id
    user_name = sender.first_name or "Yaar"
    user_text = event.raw_text

    async with client.action(user_id, 'typing'):
        await asyncio.sleep(4)
        ai_reply = get_aditi_reply(user_id, user_name, user_text)
        
    await event.reply(ai_reply)

# ==========================================
# --- 5. RUN ---
# ==========================================
if __name__ == "__main__":
    keep_alive() 
    print("🤖 Real Account Userbot is starting...")
    client.start(phone=PHONE_NUMBER)
    print("✅ BHOOM! Aditi ka asli Telegram account LIVE hai!")
    client.run_until_disconnected()
    
