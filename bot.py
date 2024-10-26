import os
import telebot
from dotenv import load_dotenv
import logging
import requests
import re


load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

bot = telebot.TeleBot(API_TOKEN)


# Function to extract the verse reference from the user's message
def extract_verse(message):
    match = re.search(r'(\w+\s\d+:\d+)', message, re.IGNORECASE)
    return match.group(0) if match else None 

@bot.message_handler(func=lambda message: True)
def send_message(message):
    user_id = str(message.from_user.id) 
    user_message = message.text

    verse_reference = extract_verse(user_message)

    if verse_reference:
        response = requests.post("http://127.0.0.1:8000/generate_commentary", json={"verse": verse_reference, "user_id": user_id})

        if response.status_code == 200:
            commentary = response.json()
            
            # Construct the reply message using the correct keys
            reply_message = (
                f"**Commentary for {verse_reference}:**\n\n"
                f"**Geographical:** {commentary['geographical']}\n"
                f"**Historical:** {commentary['historical']}\n"
                f"**Theological:** {commentary['theological']}"
            )
            bot.reply_to(message, reply_message, parse_mode='Markdown')
        else:
            bot.reply_to(message, "Sorry, there was an error processing your request.")
    else:
        bot.reply_to(message, "Please provide a valid verse reference.")

# Start the bot
if __name__ == "__main__":
    bot.polling()
