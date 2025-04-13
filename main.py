from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from datetime import datetime, timedelta
import random, re
from keep_alive import keep_alive

# ✅ Keep the bot alive
keep_alive()

# 🔐 Credentials
api_id = 21257362
api_hash = "f78ef122fe20632d49584992705f4e90"
bot_token = "7815608776:AAHgN0HtPsXbjY7W1czbGuWZCjbf1gWjXQk"

app = Client("crayon_guardian", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# 🚨 Trigger words
TRIGGER_WORDS = [
    "rug pull", "rug token", "scam coin", "scam token", "scam project", 
    "scam", "pump and dump", "fake coin", "rug"
]

user_warnings = {}

# 👋 Welcome messages (no "rug" included)
WELCOME_MESSAGES = [
    "Welcome {mention}! Hope you brought crayons 🖍️",
    "Yo {mention}, welcome to the chaos!",
    "Glad you joined us, {mention}!",
    "Hey {mention}, let’s get vibin’ 🎨",
    "Big welcome to {mention}! 🚀"
]

@app.on_message(filters.new_chat_members)
async def welcome(client, message):
    for user in message.new_chat_members:
        mention = user.mention
        msg = await message.reply_text(random.choice(WELCOME_MESSAGES).format(mention=mention))
        await msg.delete(delay=10)

# 🧼 Message Monitor
@app.on_message(filters.text & filters.group)
async def monitor(client, message):
    if message.from_user is None or message.sender_chat:
        return

    user_id = message.from_user.id
    text = message.text.lower()

    # 👑 Ignore admins
    member = await client.get_chat_member(message.chat.id, user_id)
    if member.status in ["administrator", "creator"]:
        return

    # 📛 Ignore messages with @mentions
    if "@" in text:
        return

    # 🔗 Link detection
    if re.search(r"(https?://\S+|t\.me/\S+)", text):
        await message.delete()
        user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
        count = user_warnings[user_id]
        if count >= 3:
            until = datetime.utcnow() + timedelta(days=2)
            await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False), until_date=until)
            await message.reply_text(f"{message.from_user.mention} has been muted for 2 days due to repeated links.")
        else:
            await message.reply_text(f"{message.from_user.mention}, links aren’t allowed! ⚠️ Warning {count}/3.")
        return

    # 🚫 Trigger word detection
    for word in TRIGGER_WORDS:
        if word in text:
            await message.delete()
            user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
            count = user_warnings[user_id]
            if count >= 3:
                until = datetime.utcnow() + timedelta(days=2)
                await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=False), until_date=until)
                await message.reply_text(f"{message.from_user.mention} muted for 2 days due to repeated violations.")
            else:
                await message.reply_text(f"{message.from_user.mention}, that word’s not allowed here. ⚠️ Warning {count}/3.")
            return

    # 👋 Greetings
    casual_greetings = ["hi", "hello", "hey", "yo", "heyy"]
    morning_greetings = ["gm", "good morning", "morning", "good morening"]
    night_greetings = ["gn", "good night", "night", "nite"]

    if any(word in text for word in casual_greetings):
        replies = ["Heyy 🤙", "Hi there 👋", "Yo! 😎", "Hello hello!", "What’s up! 🔥"]
        await message.reply_text(random.choice(replies))
    elif any(word in text for word in morning_greetings):
        replies = ["Good morning ☀️", "Rise and shine 🌅", "Wakey wakey 😄", "GM fam 🚀"]
        await message.reply_text(random.choice(replies))
    elif any(word in text for word in night_greetings):
        replies = ["Good night 🌙", "Sweet dreams 😴", "Sleep well 💫", "Rest up for tomorrow 💤"]
        await message.reply_text(random.choice(replies))

# 🎯 /vibecheck command
@app.on_message(filters.command("vibecheck") & filters.group)
async def vibecheck(client, message):
    vibes = [
        "You’re vibing high today 🚀",
        "Lowkey chillin' 🧊",
        "Energy's peaking 🔥",
        "Vibes are immaculate ✨",
        "Stay hydrated 💧",
        "Solid DAO energy ⚡",
        "You need more caffeine ☕",
        "Vibe level: Legendary 🧙‍♂️",
        "Crypto vibes only 🪙",
        "Stablecoin mode: Activated 😎"
    ]
    await message.reply_text(random.choice(vibes))

# ✅ Launch bot
app.run()

