import os
import sys
import subprocess
import logging

# ============================================================
# Install dependency automatically
# ============================================================

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, ContextTypes
except ImportError:
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "python-telegram-bot==22.5"
    ])

    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, ContextTypes


# ============================================================
# SETTINGS
# ============================================================

YOUTUBE_CHANNEL = "https://youtube.com/@rcastillo520"

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing. Add your Telegram bot token "
        "as a Railway environment variable."
    )


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# ============================================================
# /start
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "▶️ Watch My YouTube Channel",
                url=YOUTUBE_CHANNEL
            )
        ],
        [
            InlineKeyboardButton(
                "🔔 Subscribe on YouTube",
                url=YOUTUBE_CHANNEL
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "🎬 <b>Welcome!</b>\n\n"
        "Thanks for joining my Telegram bot! 👋\n\n"
        "📺 Check out my YouTube channel for "
        "videos, updates, and new content.\n\n"
        "👇 Click below to check it out!"
    )

    await update.message.reply_text(
        message,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


# ============================================================
# /youtube
# ============================================================

async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "📺 Visit YouTube Channel",
                url=YOUTUBE_CHANNEL
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "🎥 <b>My YouTube Channel</b>\n\n"
        "Check out my latest videos and subscribe "
        "so you don't miss new content! 🔔\n\n"
        "👇 Tap the button below:"
    )

    await update.message.reply_text(
        message,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


# ============================================================
# /help
# ============================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = (
        "🤖 <b>Bot Commands</b>\n\n"
        "/start - Welcome message\n"
        "/youtube - Visit my YouTube channel\n"
        "/help - Show available commands"
    )

    await update.message.reply_text(
        message,
        parse_mode="HTML"
    )


# ============================================================
# ERROR HANDLER
# ============================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "An error occurred:",
        exc_info=context.error
    )


# ============================================================
# START BOT
# ============================================================

def main():

    logger.info("Starting Telegram YouTube bot...")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("youtube", youtube)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_error_handler(error_handler)

    logger.info("Bot is running!")

    application.run_polling()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()

