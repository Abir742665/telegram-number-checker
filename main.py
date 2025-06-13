import telebot
import requests
from time import sleep

# Bot Token
TOKEN = '7709651915:AAHCE44EvhectlJs-tdr6SJXgZgy7MOCGjI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_numbers(message):
    try:
        # Split input into lines
        lines = [line.strip() for line in message.text.splitlines() if line.strip()]
        all_links = []
        active_accounts = []
        
        # First message - processing start
        bot.reply_to(message, "⏳ Processing numbers... Please wait.")
        
        for line in lines:
            # Clean the number
            number = line.strip().replace(" ", "").replace("+", "").replace("-", "")
            
            if not number:
                continue
            
            # Create clickable link
            link = f"[+{number}](tg://resolve?phone={number})"
            all_links.append(link)
            
            # Check if account exists
            try:
                response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getChat?chat_id={number}")
                if response.status_code == 200:
                    active_accounts.append(link)
            except:
                pass
            
            sleep(0.1)  # Avoid too many requests

        # Send all numbers
        if all_links:
            bot.reply_to(message, "📋 All Numbers:\n" + "\n".join(all_links), parse_mode='Markdown')
            
        # Send active accounts
        if active_accounts:
            bot.reply_to(message, "✅ Active Telegram Accounts:\n" + "\n".join(active_accounts), parse_mode='Markdown')
            bot.reply_to(message, f"Found {len(active_accounts)} active accounts out of {len(all_links)} numbers")
        else:
            bot.reply_to(message, "❌ No active Telegram accounts found")
            
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
