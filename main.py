দেখছি দুটি এরর আসছে:
1. "Conflict: terminated by other getUpdates request"
2. "Port scan timeout reached"

চলো এই সমস্যাগুলো ঠিক করি। নতুন কোড:

```python
import telebot
import os
from time import sleep

# Bot Token
TOKEN = '7709651915:AAHCE44EvhectlJs-tdr6SJXgZgy7MOCGjI'
bot = telebot.TeleBot(TOKEN)

# Add port configuration
port = int(os.environ.get('PORT', 8080))

@bot.message_handler(func=lambda message: True)
def handle_numbers(message):
    try:
        # Split input into lines and remove empty lines
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

        # Split links into chunks of 4000 characters
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

# Use webhook instead of polling
bot.remove_webhook()
sleep(1)
bot.set_webhook(url=f"https://telegram-number-checker.onrender.com:{port}")

# Start Flask server
import flask
app = flask.Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://telegram-number-checker.onrender.com:{port}/" + TOKEN)
    return "!", 200

# Start server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
```

এই আপডেটেড কোড:
1. Webhook ব্যবহার করে (polling এর বদলে)
2. পোর্ট কনফিগারেশন যোগ করা হয়েছে
3. Flask সার্ভার যোগ করা হয়েছে

আপডেট করার জন্য:
1. Settings এ যাও
2. main.py তে এই কোড পেস্ট করো
3. Save করো
4. Manual Deploy → Clear build cache & deploy

Settings এ যাবে?
