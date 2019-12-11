import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from config import *
from instance.config import *

import pygsheets
import pandas as pd
import numpy as np

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#authorization
gc = pygsheets.authorize(service_file=GOOGLE_SERVICE_KEY)

sh = gc.open(GOOGLE_SPREADSHEET_NAME)
wks = sh.worksheet('title','student_list')
stu_list_df = wks.get_as_df()

user_message_map = {}
user_status_map = {}

def update_dataframe():
    wks = sh.worksheet('title','student_list')
    df = pd.DataFrame('', index=[], columns=[])

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    menu = ""
    menu += "Hello, I am tutorsim.\n"
    menu += "Followings are the menu which you can select.\n"
    menu += "/daily : Check Daily Commit Results\n"
    update.message.reply_text(menu)


def help(update, context):
    menu = ""
    menu += "tutorsim Menu\n"
    menu += "/daily : Check Daily Commit Results\n"
    menu += "/mid01 : Check Midterm01 Results\n"
    update.message.reply_text(menu)

def verify_get_functor(command, sheet, header, states):

    def initiator(update, context):
        user_status_map[update.effective_user.id] = states[0]
        res = ""
        res += "Please Reply Your ID."
        update.message.reply_text(res)
        return states[1]

    def get_id(update, context):
        user_status_map[update.effective_user.id] = states[1]
        if update.effective_user.id not in user_message_map:
            user_message_map[update.effective_user.id] = [update.message.text]
        else:
            user_message_map[update.effective_user.id].append(update.message.text)

        res = ""
        res += "Please Reply Your Password."
        update.message.reply_text(res)
        return states[2]

    def check_and_get(update, context):
        user_status_map[update.effective_user.id] = states[2]
        if not user_message_map[update.effective_user.id][-1].isdecimal():
            update.message.reply_text('Invaild User')
            user_message_map[update.effective_user.id] = []
            response = ""
            response += "You may start over\n"
            response += "Press /help"
            update.message.reply_text(res)
            return ConversationHandler.END

        res = stu_list_df.loc[ stu_list_df['ID'] == int(user_message_map[update.effective_user.id][-1]), "PW"]
        if len(res.values) > 0:
            query_res = res.values[0]
        else:
            update.message.reply_text('Invaild User')
            user_message_map[update.effective_user.id] = []
            res += "You may start over\n"
            res += "Press /help"
            update.message.reply_text(res)
            return ConversationHandler.END

        if update.message.text == str(query_res):
            res = ""
            res += "You are Verified"
            update.message.reply_text(res)
            wks = sh.worksheet('title', sheet)
            df = wks.get_as_df()
            update.message.reply_text("your status is")
            res = df.loc[df['ID'] == int(user_message_map[update.effective_user.id][-1]), :]
            columns = list(res)

            response = ""
            f_str = "{0}: {1}\n"
            for i in columns:
                if i == 'ID':
                    response += f_str.format(header[0], header[1])
                    continue
                response += f_str.format(i, str(res[i].values[0]))

            update.message.reply_text(response)
            user_message_map[update.effective_user.id] = []
            return ConversationHandler.END 
        else:
            res = "You are not Verified"
            update.message.reply_text(res)
            user_message_map[update.effective_user.id] = []
            return ConversationHandler.END

    Command = CommandHandler(command, initiator)
    Message = {}
    Message[states[1]] = [MessageHandler(Filters.text, get_id)]
    Message[states[2]] = [MessageHandler(Filters.text, check_and_get)]
    return (Command, Message)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    res = ""
    res += "You may start over\n"
    res += "Press /help"
    update.message.reply_text(res)
    return ConversationHandler.END

def generate_menu(command_lst):
    idx_start = 0
    idx_end = 3

    CHATBOT_MENU = []

    for command in command_lst:
        key, sheet, heading = command
        CHATBOT_MENU.append((key, sheet, heading, range(idx_start, idx_end)))
        idx_start += 3
        idx_end += 3

    return CHATBOT_MENU

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    entry_points = []
    states = {}

    CHATBOT_MENU = generate_menu(COMMAND_LST)
    for menu in CHATBOT_MENU:    
        out = verify_get_functor(menu[0], menu[1], menu[2], menu[3])
        entry_points.append(out[0])
        for key, value in out[1].items():
            states[key] = value

    conv_handler = ConversationHandler(entry_points=entry_points, 
                                        states=states, 
                                        fallbacks=[CommandHandler('cancel', cancel)])

    dp.add_handler(CommandHandler("help", help))
    #dp.add_handler(CommandHandler("daily", daily))
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()