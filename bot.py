
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
import sqlite3

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database setup
DB_PATH = "redhatcoinbot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 100
    )''')
    conn.commit()
    conn.close()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
              (user.id, user.username))
    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"Welcome {user.first_name}! You have been given 100 RedHat coins to start!"
    )

# Wallet command
async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    balance = result[0] if result else 0
    conn.close()

    await update.message.reply_text(f"Your current balance: {balance} RedHat coins.")

# Play game command
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Guess 1-3", callback_data="guess"),
            InlineKeyboardButton("Roll Dice", callback_data="dice")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Choose a game to play:", reply_markup=reply_markup
    )

# Handle game choices
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "guess":
        await query.edit_message_text(text="Guess a number between 1 and 3!")
        # Game logic to be added
    elif choice == "dice":
        await query.edit_message_text(text="Rolling the dice!")
        # Game logic to be added

# Main function to start the bot
def main() -> None:
    init_db()

    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wallet", wallet))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CallbackQueryHandler(button))

    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
