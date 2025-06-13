import telebot
from telebot.handler_backends import State, StatesGroup
from time import sleep

# Bot Token
TOKEN = '7709651915:AAHCE44EvhectlJs-tdr6SJXgZgy7MOCGjI'
bot = telebot.TeleBot(TOKEN)

class NumberStates(StatesGroup):
    checking = State()

@bot.message_handler(func=lambda message: True)
def handle_numbers(message):
    try:
        # Split input into lines
        lines = [line.strip() for line in message.text.splitlines() if line.strip()]
        formatted_links = []
        active_links = []
        
        # Process numbers
        for line in lines:
            # Clean the number
            number = line.strip().replace(" ", "").replace("+", "").replace("-", "")
            
            if not number:
                continue
                
            # Create clickable link
            link = f"[+{number}](tg://resolve?phone={number})"
            formatted_links.append(link)

        # Send in chunks of 4000 characters
        chunks = []
        current_chunk = []
        current_length = 0
        
        for link in formatted_links:
            if current_length + len(link) + 1 > 4000:
                chunks.append("\n".join(current_chunk))
                current_chunk = [link]
                current_length = len(link)
            else:
                current_chunk.append(link)
                current_length += len(link) + 1

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        # Send all chunks
        for i, chunk in enumerate(chunks):
            if i == 0:
                bot.reply_to(message, f"📱 Numbers ({len(formatted_links)} total):\n{chunk}", parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, chunk, parse_mode='Markdown')
            sleep(0.5)  # Avoid flood limits

    except Exception as e:
        bot.reply_to(message, "Try again!")

# Initialize bot with error handling
while True:
    try:
        print("Bot started...")
        bot.infinity_polling(timeout=20, long_polling_timeout=5)
    except Exception as e:
        print(e)
        sleep(3)
