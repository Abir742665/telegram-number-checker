import telebot

# Bot Token
TOKEN = '7709651915:AAHCE44EvhectlJs-tdr6SJXgZgy7MOCGjI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_numbers(message):
    try:
        # Split input into lines
        lines = message.text.strip().splitlines()
        formatted_links = []

        for line in lines:
            # Clean the number (remove spaces and any existing +)
            number = line.strip().replace(" ", "").replace("+", "")
            
            # Create clickable link
            link = f"[+{number}](tg://resolve?phone={number})"
            formatted_links.append(link)

        # Join all links
        reply = "\n".join(formatted_links)
        
        # Send message
        bot.reply_to(message, reply, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, "Try again!")

print("Bot started...")
bot.polling()
