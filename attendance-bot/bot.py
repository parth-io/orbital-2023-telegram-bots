import json
import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler

token = "[YOUR TOKEN HERE]"

# ConversationHandler stuff
CLASS = range(1)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Class defining an attendance session
from typing import Dict, List

class AttendanceSession:
    def __init__(self, chat_id: int, message_id: int, message: str) -> None:
        self.chat_id = chat_id
        self.message_id = message_id
        self.message = message

    def to_json(self) -> Dict:
        json_data = {
            'chat_id': self.chat_id,
            'message_id': self.message_id,
            'message': self.message
        }
        return json.dumps(json_data)


# Store JSONs as separate maps in memory. These variables should
# eventually be persisted to a database of some sort, but for now
# we store it all in the program's runtime memory.
CLASS_TO_STUDENTS = {
    "MKT3702": {
        "Teh Kari": "gparth26"
    }
}
STUDENTS_TO_CLASS = {}
CLASS_TO_SESSION = {}
USERNAME_TO_IDS = {}
SESSION_TO_ATTENDANCE = {}

########################################
########### COMMON COMMANDS ############
########################################


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    global USERNAME_TO_IDS
    USERNAME_TO_IDS[update.message.from_user.username] = update.message.from_user.id
    await update.message.reply_text(
        'Welcome! Your username has been stored in our very secure servers.')


########################################
####### COMMANDS FOR THE TEACHER #######
########################################


async def start_attendance_session(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    # Keyboard for choosing class
    keyboard = [
        [class_str for class_str in CLASS_TO_STUDENTS.keys()]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Choose class:', reply_markup=reply_markup)

    return CLASS


async def class_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create attendance session
    chat_id = update.message.from_user.id
    classname = update.message.text
    message_text = f'Attendance session for {classname}:'
    message = await update.message.reply_text(message_text)
    session = AttendanceSession(
        chat_id=chat_id, message_id=message.message_id, message=message_text)

    # Save session in dictionary
    CLASS_TO_SESSION[classname] = session.to_json()

    # Send message to students in class
    class_list = CLASS_TO_STUDENTS[classname].values()
    await update.message.reply_text('Sending attendance messages...')
    await send_attendance_messages(context, class_list, classname)

    return ConversationHandler.END


# Command to cancel ConversationHandler
async def cancel(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Attendance session creation has been canceled.')


# Send messages to all users in usernames
async def send_attendance_messages(context: ContextTypes.DEFAULT_TYPE, usernames: List[str], classname: str) -> None:
    for username in usernames:
        chat_id = USERNAME_TO_IDS[username]
        await context.bot.send_message(
            chat_id=chat_id,
            text=f'Mark attendance for {classname}!'
        )


########################################
####### COMMANDS FOR THE STUDENT #######
########################################


async def mark_attendance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get attendance session
    classname = STUDENTS_TO_CLASS[update.message.from_user.username]
    session = json.loads(CLASS_TO_SESSION[classname])

    session_chat_id = session.get('chat_id')
    user_name = f'{update.message.from_user.first_name}' 
    await context.bot.edit_message_text(
        text=update_attendance_message(
            session, user_name),
        chat_id=session_chat_id,
        message_id=session['message_id']
    )

    if SESSION_TO_ATTENDANCE.get(session_chat_id) is None:
        SESSION_TO_ATTENDANCE[session_chat_id] = []

    SESSION_TO_ATTENDANCE[session_chat_id].append(user_name)
    await update.message.reply_text("Attendance marked!")

async def show_attendance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(str(SESSION_TO_ATTENDANCE))

def update_attendance_message(session: dict, username: str) -> str:
    session['message'] += '\n' + username
    return session['message']


########################################
############# BOT SETUP ################
########################################


def init_data() -> None:
    for classname, students in CLASS_TO_STUDENTS.items():
        for _, student_id in students.items():
            STUDENTS_TO_CLASS[student_id] = classname


def main() -> None:
    # Init data
    init_data()

    """Start the bot."""
    application = ApplicationBuilder().token(token).build()
    
    #Command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('mark_attendance', mark_attendance))
    application.add_handler(CommandHandler('show_attendance', show_attendance))
    
    # Add conversation handler with to start attendance session
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            'start_attendance', start_attendance_session)],
        states={
            CLASS: [MessageHandler(filters.TEXT, class_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    # start > start_attendance > show_attendance
    main()
