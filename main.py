# --- Part 1: All the necessary imports ---
import logging
import asyncio 
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
# --- Part 2: Web Server Imports (to keep the bot alive on Replit) ---
from flask import Flask, request 
from threading import Thread

# --- Part 3: Web Server Setup ---
app = Flask('')

@app.route('/', methods=['GET', 'POST'])
def webhook():
   if request.method == 'POST':
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))

    return "ok", 200

    else:
        return "I'm alive and ready for messages!"

def run_web_server():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()

# --- Part 4: The Rest of Your Bot Code (with the typo fixed) ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

STATE_GET_NAME, STATE_CHOOSE_FONT = range(2)

NORMAL_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
FONTS = {
    "Normal Text": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "Bold Fraktur": "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
    "Cursive": "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫",
    "Double Struck": "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞🟟𝟠𝟡",
    # --- THIS LINE IS NOW FIXED ---
    "Monospace": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
    "Serif Bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    "Sans-Serif Bold": "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
    "Circled": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨",
}

FONT_MAPS = { name: str.maketrans(NORMAL_CHARS, styled_chars) for name, styled_chars in FONTS.items() }

def apply_font(text: str, style_name: str) -> str:
    if style_name in FONT_MAPS: return text.translate(FONT_MAPS[style_name])
    return text

async def tag_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("✨ Hey! Enter Your name For Tag of the GC:")
    return STATE_GET_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_name = update.message.text
    context.user_data["name"] = user_name
    keyboard = []
    prefix = "𝕯𝖚𝖒𝖎𝖓 𝕩 "
    suffix = "♛"
    for style_name in FONT_MAPS.keys():
        styled_name = apply_font(user_name, style_name)
        full_text = f"{prefix}{styled_name}{suffix}"
        button = InlineKeyboardButton(full_text, callback_data=style_name)
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👇 Choose your desired style:", reply_markup=reply_markup)
    return STATE_CHOOSE_FONT

async def choose_font(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    chosen_style = query.data
    user_name = context.user_data.get("name")
    prefix = "𝕯𝖚𝖒𝖎𝖓 𝕩 "
    suffix = "♛"
    styled_name = apply_font(user_name, chosen_style)
    final_text = f"{prefix}{styled_name}{suffix}"
    await query.edit_message_text(text=f"✅ Style '{chosen_style}' selected!")
    await context.bot.send_message(
        chat_id=query.message.chat_id, text=f"`{final_text}`", parse_mode='MarkdownV2'
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main() -> None:
    keep_alive() # Starts the web server
    
    # Get the token from Replit Secrets
    TOKEN = os.environ.get('BOT_TOKEN')
    if not TOKEN:
        print("CRITICAL ERROR: 'BOT_TOKEN' not found in Replit Secrets!")
        return
        
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("tag", tag_command)],
        states={
            STATE_GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            STATE_CHOOSE_FONT: [CallbackQueryHandler(choose_font)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    # --- THE NEW, CORRECTED CODE ---
    if __name__ == "__main__":
        # Start the web server to listen for messages from Telegram
        keep_alive()
        print("Bot is alive and listening for webhook updates...") 
# End Of file  
