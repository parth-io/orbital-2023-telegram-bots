import logging
import asyncio
import time
import requests
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

token = "[YOUR TOKEN HERE]"

async def manual_poll(application):
    while True:
        r = requests.get("http://206.189.92.77")
        if "Blue" in str(r.content):
            await application.bot.send_message(chat_id="1113648650", text="The sky is meant to be blue for us Earthies")
            time.sleep(60 * 60 * 24 - 1) # wait for the next day's colour
        time.sleep(1) # sleep for a while, to avoid overloading the server

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    application = ApplicationBuilder().token(token).build()
    
    # Error handler
    application.add_error_handler(error)

    asyncio.run(manual_poll(application))
    
if __name__ == '__main__':
    main()
