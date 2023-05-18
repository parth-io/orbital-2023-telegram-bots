#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
# Import
import asyncio
from telegram import Update
from telegram.constants import ParseMode
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler

# Enable logging
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#token = "[YOUR TOKEN HERE]"
token = "6077444129:AAHv9tb5g-Ixd6XPcybGOfZB9D-OJBZreW8"

# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hi {user.mention_markdown_v2()}\!\nYou can talk to me', parse_mode=ParseMode.MARKDOWN_V2)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes the user's message."""
    # Get your feet wet! Try this first
    # Either of the two lines work well
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    #await update.message.reply_text(f"you said {update.message.text}")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You are saved!")

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

import math
from random import random
import datetime
async def quadratic(update, context) -> None:
    # This will give us all the words in the message, which will be something like "/quadratic 1 2 3"
    all_words = update.message.text.split(" ")

    # We convert terms from index 1 to 3 to an array of integers
    terms = list(map(lambda x: int(x), all_words[1:]))
    a = terms[0]
    b = terms[1]
    c = terms[2]

    # discriminant
    disc = math.sqrt(b ** 2 - 4 * a * c)

    sol1 = (-b + disc) / 2 * a
    sol2 = (-b - disc) / 2 * a

    reply = f"Your roots are {sol1} and {sol2}"

    await update.message.reply_text(reply)


async def cat(update, context) -> None:
    timestamp = datetime.datetime.now().isoformat()
    url = f"https://cataas.com/cat?a={timestamp}" # As Telegram caches the URL

    await update.message.reply_photo(photo=url)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    application = ApplicationBuilder().token(token).build()
    
    # Create your handlers here
    #Command handlers
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    #Message handlers
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # Register your handlers here
    application.add_handler(start_handler)
    application.add_handler(help_handler) # beware of the order
    application.add_handler(echo_handler)
    application.add_handler(inline_caps_handler)
    
    # Add your quadratic and cat handlers here
    application.add_handler(CommandHandler("quadratic", quadratic))
    application.add_handler(CommandHandler("cat", cat))
    
    application.add_handler(unknown_handler) # beware of the order
    
    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()
