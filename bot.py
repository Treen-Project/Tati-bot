import logging
import os
import sys
import telegram
from telegram.ext import Updater, CommandHandler
import random
from functions.scrapper import getTeslaActionsPrice

# config logggin
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()

# request token
TOKEN = os.environ.get("TOKEN", None)
if TOKEN is None:
    logger.info("Specify TOKEN.")
    sys.exit(1)

# request MODE
MODE = os.environ.get("MODE", None)
if MODE is None or MODE not in ["dev", "prod"]:
    logger.info("Specify MODE.")
    sys.exit(1)


def run(updater):
    """Start execution of the bot"""
    if MODE == "dev":
        updater.start_polling()
        print("Bot Ready")
        updater.idle()  # allows to end our bot with ctrl + c
    elif MODE == "prod":
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook(
            f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")


def greet(update, context):
    """Function that show random greet"""
    name = update.effective_user['first_name']
    greets = ['Hello', 'Welcome', 'Greetings!',
              'Salutatons!', 'Good day!', 'Yo!']
    update.message.reply_text(f"{random.choice(greets)}, {name}")


def tesla(update, context):
    """call getTeslaActionsPrice and show the value of this"""
    update.message.reply_text(
        f"tesla actions price: ${getTeslaActionsPrice()} USD")


if __name__ == "__main__":
    # get information from the bot
    try:
        my_bot = telegram.Bot(token=TOKEN)
    except telegram.error.InvalidToken:
        logger.info("Invalid TOKEN.")
        sys.exit(1)

    # link updater with the bot
    updater = Updater(my_bot.token, use_context=True)

    # create dispatcher
    dp = updater.dispatcher

    # create handler
    dp.add_handler(CommandHandler("hi", greet))
    dp.add_handler(CommandHandler("tesla", tesla))

    run(updater)
