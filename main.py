import os
import json
import asyncio
import random
from threading import Thread
from flask import Flask
from google import genai
from telethon import TelegramClient, events

# ==========================================
# --- 1. CONFIGURATION ---
# ==========================================
API_ID = 34012656
API_HASH = "267f6fe3e9d163e735ad912344a529e7"
PHONE_NUMBER = "+919250751630" 
IG_USERNAME = "adititiwari99877"

# 🔥 TERI 7 NAYI GEMINI API KEYS 🔥
GEMINI_KEYS = [
    "AIzaSyDXmhizAGzHeWRheLmoCFNooYNkXHHPNjM",
    "AIzaSyCt4A2rXecpXJdZiiFM1hQYg3-yMhjjD1U",
    "AIzaSyAFAPS53T4w9eRs1lfYA5E1y_6W7wDmKYU",
    "AIzaSyBn2a16hWa9Za_oL87kmz1XIZNB42-OQKs",
    "AIzaSyC0ZFNCzrEzsM35fdCxo1z0KIX_Tt4Jnhs",
    "AIzaSyBrKgXl5mhM-tylHooBloXT9MP1xzCca6E",
    "AIzaSyBiLOtQdgxu3PMBWX-TWgc0Uf4naa7oxNI"
]
current_key_index = 0
ai_client = genai.Client(api_key=GEMINI_KEYS[current_key_index])

# ==========================================
# --- 2. LONG TERM MEMORY SYSTEM ---
# ==========================================
user_memory = {}
MEMORY_FILE = "tg_memory.json"

if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r") as f:
            user_memory = json.load(f)
    except:
        user_memory = {}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(user_memory, f)

# ==========================================
# --- 3. ANTI-SLEEP WEB SERVER ---
# ==========================================
app = Flask(__name__)
@app.route('/')
def home(): 
    return "Aditi ka Telegram Bot 24/7 Live Hai! 🔥😎"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ==========================================
# --- 4. ADVANCED AI LOGIC (Aditi ka Dimag) ---
# ==========================================
def get_aditi_reply(user_id, user_name, user_text):
    global current_key_index, ai_client, user_memory
    
    user_id_str = str(user_id)
    if user_id_str not in user_memory:
        user_memory[user_id_str] = []
        
    # Sirf pichli 10 baatein yaad rakhegi
    if len(user_memory[user_id_str]) > 10:
        user_memory[user_id_str] = user_memory[user_id_str][-10:]
        
    history_text = "\n".join(user_memory[user_id_str])
    
    # 🎯 TARGET: Ladko ko baaton mein uljhakar Instagram par bhejna
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
            
            # Message save karo
            user_memory[user_id_str].append(f"{user_name}: {user_text}")
            user_memory[user_id_str].append(f"Aditi: {reply}")
            save_memory()
            
            return reply
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
                current_key_index = (current_key_index + 1) % len(GEMINI_KEYS)
                ai_client = genai.Client(api_key=GEMINI_KEYS[current_key_index])
                print(f"🔄 Key Switched to Index {current_key_index}")
            else:
                print(f"❌ AI Error: {e}")
                break 
                
    return f"Yaar mera net rula raha hai... tum ek kaam karo mujhe Insta pe hi msg kar do: @{IG_USERNAME}"

# ==========================================
# --- 5. TELETHON ENGINE (Natural Typing) ---
# ==========================================
client = TelegramClient('aditi_session', API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_new_message(event):
    sender = await event.get_sender()
    
    # Agar message khud ka hai, toh ignore karo
    if sender.is_self: 
        return
        
    user_id = sender.id
    user_name = sender.first_name or "Yaar"
    user_text = event.raw_text

    print(f"📩 Naya message {user_name} se: {user_text}")

    # 🔥 1. NATURAL READ DELAY (1 se 3 second wait)
    await asyncio.sleep(random.randint(1, 3))
    
    # 🔥 2. TYPING SIMULATION (5 se 10 second)
    typing_delay = random.randint(5, 10)
    async with client.action(user_id, 'typing'):
        print(f"✍️ Aditi is typing for {typing_delay}s...")
        await asyncio.sleep(typing_delay)
        
        # 🔥 3. GET AI REPLY (Bina bot hang kiye)
        ai_reply = await asyncio.to_thread(get_aditi_reply, user_id, user_name, user_text)
        
    # 🔥 4. SEND REPLY
    await event.reply(ai_reply)

# ==========================================
# --- 6. MAIN EXECUTION ---
# ==========================================
if __name__ == "__main__":
    Thread(target=run_server, daemon=True).start()
    
    print("🤖 Aditi Telegram Userbot is starting...")
    client.start(phone=PHONE_NUMBER)
    print("✅ BHOOM! Aditi ka asli Telegram account LIVE hai!")
    client.run_until_disconnected()
    
