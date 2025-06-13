import telebot
from time import sleep

# Bot Token
TOKEN = '7709651915:AAHCE44EvhectlJs-tdr6SJXgZgy7MOCGjI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_numbers(message):
    try:
        # Split input into lines
        lines = [line.strip() for line in message.text.splitlines() if line.strip()]
        formatted_links = []

        for line in lines:
            # Clean the number
            number = line.strip().replace(" ", "").replace("+", "").replace("-", "")
            
            # Skip empty numbers
            if not number:
                continue
                
            # Create clickable link
            link = f"[+{number}](tg://resolve?phone={number})"
            formatted_links.append(link)

        # Send in chunks of 4000 characters
        current_chunk = []
        current_length = 0
        
        for link in formatted_links:
            if current_length + len(link) + 1 > 4000:
                # Send current chunk
                reply = "\n".join(current_chunk)
                bot.reply_to(message, reply, parse_mode='Markdown')
                sleep(0.5)
                
                # Start new chunk
                current_chunk = [link]
                current_length = len(link)
            else:
                current_chunk.append(link)
                current_length += len(link) + 1

        # Send remaining links
        if current_chunk:
            reply = "\n".join(current_chunk)
            bot.reply_to(message, reply, parse_mode='Markdown')
            
    except Exception as e:
        bot.reply_to(message, "Try again!")

# Keep bot running
while True:
    try:
        print("Bot started...")
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        sleep(3)
