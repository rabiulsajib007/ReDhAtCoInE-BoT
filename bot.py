# Preparing the folder structure for the Lucky Draw crypto game bot project
game_project_name = "LuckyDrawRedHatCoin"
game_base_dir = f"/mnt/data/{game_project_name}"
os.makedirs(game_base_dir, exist_ok=True)

# Game bot files
game_files = {
    f"{game_base_dir}/bot.py": """
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import sqlite3

# Database setup
DB_PATH = "lucky_draw.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        spins INTEGER DEFAULT 0,
        wallet_ton REAL DEFAULT 0.0,
        wallet_gems INTEGER DEFAULT 0,
        wallet_redhat INTEGER DEFAULT 0,
        wallet_usdt REAL DEFAULT 0.0,
        wallet_token INTEGER DEFAULT 0
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
        f"Welcome {user.first_name}! Complete tasks to earn spins and win prizes!"
    )

# Lucky Draw spin command
async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT spins FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()

    if result and result[0] > 0:
        # Deduct one spin and award a random prize
        prizes = ["0.000001 TON", "5 Gems", "10 RedHat Coins", "1 USDT", "1 Token"]
        prize = random.choice(prizes)
        c.execute("UPDATE users SET spins = spins - 1 WHERE id = ?", (user_id,))
        conn.commit()

        # Update wallet based on prize
        if prize == "0.000001 TON":
            c.execute("UPDATE users SET wallet_ton = wallet_ton + 0.000001 WHERE id = ?", (user_id,))
        elif prize == "5 Gems":
            c.execute("UPDATE users SET wallet_gems = wallet_gems + 5 WHERE id = ?", (user_id,))
        elif prize == "10 RedHat Coins":
            c.execute("UPDATE users SET wallet_redhat = wallet_redhat + 10 WHERE id = ?", (user_id,))
        elif prize == "1 USDT":
            c.execute("UPDATE users SET wallet_usdt = wallet_usdt + 1 WHERE id = ?", (user_id,))
        elif prize == "1 Token":
            c.execute("UPDATE users SET wallet_token = wallet_token + 1 WHERE id = ?", (user_id,))
        conn.commit()

        await update.message.reply_text(f"Congratulations! You won {prize}!")
    else:
        await update.message.reply_text("You don't have any spins left. Complete tasks to earn more!")

    conn.close()

# Check Wallet command
async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT wallet_ton, wallet_gems, wallet_redhat, wallet_usdt, wallet_token
                 FROM users WHERE id = ?""", (user_id,))
    result = c.fetchone()
    conn.close()

    if result:
        ton, gems, redhat, usdt, token = result
        await update.message.reply_text(
            f"Your Wallet:\n"
            f"TON: {ton}\n"
            f"Gems: {gems}\n"
            f"RedHat Coins: {redhat}\n"
            f"USDT: {usdt}\n"
            f"Tokens: {token}"
        )
    else:
        await update.message.reply_text("You don't have a wallet yet. Use /start to begin!")

# Main function to start the bot
def main() -> None:
    init_db()

    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spin", spin))
    app.add_handler(CommandHandler("wallet", wallet))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
""",
    f"{game_base_dir}/requirements.txt": """
python-telegram-bot==20.0
sqlite3
""",
    f"{game_base_dir}/README.md": """
# LuckyDrawRedHatCoin Game

A Telegram bot for a fun lucky draw game with RedHat Coins and other crypto prizes.

## Features
- Spin the lucky draw to win prizes: TON, Gems, RedHat Coins, USDT, or Tokens.
- Complete tasks to earn spins (3 spins per task).
- Wallet system to track winnings.

## Setup
1. Install Python dependencies:
