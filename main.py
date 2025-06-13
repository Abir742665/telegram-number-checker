import telebot
from time import sleep

# Bot Token
TOKEN = '7709651915:AAHCE44EvhectlJs-tdr6SJXgZgy7MOCGjI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send numbers (one per line) to check Telegram accounts.")

@bot.message_handler(func=lambda message: True)
def handle_numbers(message):
    try:
        # Split input into lines
        lines = [line.strip() for line in message.text.splitlines() if line.strip()]
        formatted_links = []

        for line in lines:
            # Clean the number
            number = line.strip().replace(" ", "").replace("+", "").replace("-", "")
            
            if not number:
                continue
                
            # Create clickable link
            link = f"[+{number}](tg://resolve?phone={number})"
            formatted_links.append(link)

        # Send in chunks
        chunk_size = 50  # Process 50 numbers at a time
        for i in range(0, len(formatted_links), chunk_size):
            chunk = formatted_links[i:i + chunk_size]
            reply = "\n".join(chunk)
            bot.reply_to(message, reply, parse_mode='Markdown')
            sleep(1)  # Wait 1 second between chunks
            
    except Exception as e:
        bot.reply_to(message, "Try again!")

# Remove webhook and clear updates
bot.remove_webhook()
sleep(1)

# Start bot
print("Bot started...")
bot.polling(none_stop=True, interval=1)
