#!pip install python-telegram-bot
#!pip install nest_asyncio

# Import
import asyncio
import time
import requests
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes

# Enable logging
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

token = "[YOUR TOKEN HERE]"

# Workaround for nested event loops in Jupyter
# As Jupyter notebooks already have a running loop via Tornado and the asyncio lib does not allow a nested loop, we need to use a separate package called nest_asyncio
import nest_asyncio
nest_asyncio.apply()

async def manual_poll(application):
    while True:
        r = requests.get("http://206.189.92.77")
        # TODO 1 add your implementation here
        time.sleep(1) # sleep for a while, to avoid overloading the server

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    application = ApplicationBuilder().token(token).build()
    
    # Error handler
    application.add_error_handler(error)
    
    # We pass in the Telegram event loop as a nested event loop here - only for Jupyter
    # Python version < 3.7
    # loop = asyncio.get_event_loop()
    # loop.create_task()
    # Python version >= 3.7
    asyncio.run(manual_poll(application)) # TODO 2 what goes here :)
    # Note that as the library's polling loop is not being used,
    # asyncio.run() will have to be used even outside of Jupyter, unlike the previous bot

if __name__ == '__main__':
    main()
