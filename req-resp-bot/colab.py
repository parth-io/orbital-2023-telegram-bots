#!pip install python-telegram-bot
#!pip install nest_asyncio

# Import
import asyncio
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

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

# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hi {user.mention_markdown_v2()}\!\nYou can talk to me', parse_mode=ParseMode.MARKDOWN_V2)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes the user's message."""
    # TODO 1 Get your feet wet! Try this first
    # Hint: use `text=update.message.text`
    pass
    # TODO 2 An alternative approach

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You are saved!")
    #TODO 3 Register my handlers

# Bonus content - inline mode. To test this out, type `/setinline` in @BotFather and type @<your bot's name> in any of your other chats to talk to your bot
async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Capitalises the message."""
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """In the case of an unknown command"""
    #TODO 4
    pass

# Imports for quadratic and cat
import math
from random import random
def quadratic(update, context):
    # This will give us all the words in the message, which will be something like "/quadratic 1 2 3"
    # Hint: You can use the `split()` method of a Python string
    # TODO 5
    pass
    
def cat(update, context):
    url = f"https://cataas.com/cat?id={number}"
    #Hint: You can use the `reply_photo()` method
    # TODO 6
    pass

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    application = ApplicationBuilder().token(token).build()
    
    # Create your handlers here
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # Register your handlers here
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    
    # Error handler
    application.add_error_handler(error)
    
    # Add your quadratic and cat handlers here
    # TODO 7

    # We pass in the Telegram event loop as a nested event loop here - only for Jupyter
    loop = asyncio.get_event_loop()
    loop.create_task(application.run_polling())

if __name__ == '__main__':
    main()
