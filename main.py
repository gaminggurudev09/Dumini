# -*- coding: utf-8 -*-

# --- Part 1: All Imports ---
import logging
import asyncio
import os
from threading import Thread
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# --- Part 2: Initialize Bot and Web Server ---

# Get the bot token from Replit Secrets
BOT_TOKEN = os.environ.get("TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables. Please set it in Replit Secrets.")

# Initialize the Telegram Bot Application
# This is placed here so the 'webhook' function below can access it.
application = Application.builder().token(BOT_TOKEN).build()

# Initialize the Flask Web Server
app = Flask(__name__)


# --- Part 3: Web Server Logic for Webhook ---

@app.route('/', methods=['GET', 'POST'])
def webhook():
    """This function receives updates from Telegram and forwards them to the bot."""
    if request.method == 'POST':
        try:
            # Get the JSON data from the request
            update_data = request.get_json(force=True)
            
            # Create an Update object that the python-telegram-bot library understands
            update = Update.de_json(update_data, application.bot)
            
            # Process the update asynchronously
            asyncio.run(application.process_update(update))
            
        except Exception as e:
            logging.error(f"Error processing update: {e}")
        
        # Always return 'ok' to Telegram to acknowledge receipt of the update
        return "ok", 200
    else:
        # This handles GET requests (e.g., from UptimeRobot) to confirm the bot is alive
        return "Bot is alive and listening!", 200

def run_web_server():
    """Runs the Flask web server."""
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Starts the web server in a separate thread."""
    t = Thread(target=run_web_server)
    t.start()


# --- Part 4: Bot Logging and Font Definitions ---

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states for the conversation
STATE_GET_NAME, STATE_CHOOSE_FONT, STATE_GET_MESSAGE = range(3)

# Font definitions
FONT_MAPS = {
    "font_1": str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅0123456789"),
    "font_2": str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫"),
    "font_3": str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"),
    "font_4": str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ⓪①②③④⑤⑥⑦⑧⑨")
}
STYLED_CHARS = list(FONT_MAPS.keys())

def apply_font_style(text, font_name):
    """Applies a selected font style to the text."""
    if font_name in FONT_MAPS:
        return text.translate(FONT_MAPS[font_name])
    return text


# --- Part 5: Bot Command and Conversation Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks for the user's name."""
    await update.message.reply_text("✨ Welcome to Dumini Font Bot! ✨\nPlease enter your name to begin:")
    return STATE_GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the name and asks the user to choose a font."""
    user_name = update.message.text
    context.user_data["name"] = user_name
    
    keyboard = [
        [InlineKeyboardButton("Stylish Font", callback_data="font_1")],
        [InlineKeyboardButton("Cursive Font", callback_data="font_2")],
        [InlineKeyboardButton("Double Struck", callback_data="font_3")],
        [InlineKeyboardButton("Circled Font", callback_data="font_4")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(f"Hi {user_name}! Please choose a font:", reply_markup=reply_markup)
    return STATE_CHOOSE_FONT

async def choose_font(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the chosen font and asks for a message."""
    query = update.callback_query
    await query.answer()
    
    font_choice = query.data
    context.user_data["font"] = font_choice
    
    await query.edit_message_text(text=f"Font selected. Now, please send me the message you want to style.")
    return STATE_GET_MESSAGE

async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Applies the font to the message and ends the conversation."""
    user_message = update.message.text
    chosen_font = context.user_data.get("font")
    
    if chosen_font:
        styled_message = apply_font_style(user_message, chosen_font)
        await update.message.reply_text(f"Here is your styled message:\n\n`{styled_message}`", parse_mode="MarkdownV2")
    else:
        await update.message.reply_text("Something went wrong. Please /start again.")
        
    await update.message.reply_text("Thank you for using the bot! Type /start to begin again.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("Operation cancelled. Type /start to begin again.")
    return ConversationHandler.END


# --- Part 6: Set Up and Run the Bot ---

# Create the ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        STATE_GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        STATE_CHOOSE_FONT: [CallbackQueryHandler(choose_font)],
        STATE_GET_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

# Add the ConversationHandler to the application
application.add_handler(conv_handler)

# The main execution block
if __name__ == "__main__":
    # Start the web server to listen for webhook updates
    keep_alive()
    print("Bot is alive and listening for webhook updates...")