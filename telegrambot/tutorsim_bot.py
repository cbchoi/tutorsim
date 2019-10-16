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

DAILY, VERIFY_DAILY_ID, VERIFY_DAILY_PW = range(0, 3)
MID01, VERIFY_MID01_ID, VERIFY_MID01_PW = range(3, 6)

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

def daily(update, context):
    user_status_map[update.effective_user] = DAILY
    res = ""
    res += "Please Reply Your ID."
    update.message.reply_text(res)
    return VERIFY_DAILY_ID

def verify_daily_id(update, context):
    user_status_map[update.effective_user.id] = VERIFY_DAILY_ID
    if update.effective_user.id not in user_message_map:
        user_message_map[update.effective_user.id] = [update.message.text]
    else:
        user_message_map[update.effective_user.id].append(update.message.text)

    res = ""
    res += "Please Reply Your Password."
    update.message.reply_text(res)
    return VERIFY_DAILY_PW

def verify_daily_pw(update, context):
    user_status_map[update.effective_user.id] = VERIFY_DAILY_PW
    print("id_check")
    if not user_message_map[update.effective_user.id][-1].isdecimal():
        update.message.reply_text('Invaild User')
        user_message_map[update.effective_user.id] = []
        response = ""
        response += "You may start over\n"
        response += "Press /help"
        update.message.reply_text(res)
        return ConversationHandler.END

    print("pw_check")
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
        wks = sh.worksheet('title','Daily')
        df = wks.get_as_df()
        update.message.reply_text("your status is")
        res = df.loc[df['ID'] == int(user_message_map[update.effective_user.id][-1]), :]
        columns = list(res)

        response = ""
        f_str = "{0}: {1}\n"
        for i in columns:
            if i == 'ID':
                response += f_str.format("Date","Result")
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

def mid01(update, context):
    user_status_map[update.effective_user] = MID01
    res = ""
    res += "Please Reply Your ID."
    update.message.reply_text(res)
    return VERIFY_MID01_ID

def verify_mid01_id(update, context):
    user_status_map[update.effective_user.id] = VERIFY_MID01_ID
    if update.effective_user.id not in user_message_map:
        user_message_map[update.effective_user.id] = [update.message.text]
    else:
        user_message_map[update.effective_user.id].append(update.message.text)

    res = ""
    res += "Please Reply Your Password."
    update.message.reply_text(res)
    return VERIFY_MID01_PW

def verify_mid01_pw(update, context):
    user_status_map[update.effective_user.id] = VERIFY_MID01_PW
    print("id_check")
    if not user_message_map[update.effective_user.id][-1].isdecimal():
        update.message.reply_text('Invaild User')
        user_message_map[update.effective_user.id] = []
        response = ""
        response += "You may start over\n"
        response += "Press /help"
        update.message.reply_text(res)
        return ConversationHandler.END

    print("pw_check")
    res = stu_list_df.loc[ stu_list_df['ID'] == int(user_message_map[update.effective_user.id][-1]), "PW"]
    print(int(user_message_map[update.effective_user.id][-1]))
    
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
        wks = sh.worksheet('title','midterm01')
        df = wks.get_as_df()
        update.message.reply_text("your status is")
        res = df.loc[df['ID'] == int(user_message_map[update.effective_user.id][-1]), :]
        columns = list(res)

        response = ""
        f_str = "{0}: {1}\n"
        for i in columns:
            if i == 'ID':
                response += f_str.format("Problem","Result")
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

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    res = ""
    res += "You may start over\n"
    res += "Press /help"
    update.message.reply_text(res)
    return ConversationHandler.END

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('daily', daily), CommandHandler('mid01', mid01)],

        states={
            VERIFY_DAILY_ID: [MessageHandler(Filters.text, verify_daily_id)],
            VERIFY_DAILY_PW: [MessageHandler(Filters.text, verify_daily_pw)],

            VERIFY_MID01_ID: [MessageHandler(Filters.text, verify_mid01_id)],
            VERIFY_MID01_PW: [MessageHandler(Filters.text, verify_mid01_pw)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    # on different commands - answer in Telegram
    #dp.add_handler(CommandHandler("start", start))
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