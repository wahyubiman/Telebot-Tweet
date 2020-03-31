'''from app.database import *
from .helper import wordlist, twitter
from .scraper import start_scrape
'''
import logging
from configobj import ConfigObj
from telegram.ext import (Updater, CommandHandler, Filters, CallbackContext)
from .helper import twitter, wordlist
from .scraper import start_scrape
from functools import wraps

logger = logging.getLogger()
config = ConfigObj("setting.ini")
LIST_OF_ADMINS = ['wahyubiman']

def restricted(func):
    '''wrapper for restrict user action'''
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        username = update.message.from_user.username
        if username not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(username))
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def start(update, context):
    update.message.reply_text("""### Welcome ###
    
    this bot can scrape tweet that contain specific keyword,
    
    please use /help to see all available command""")
    
text_help = """### HELP ###

if command has argument, add command + argument separated by space

# Supported command :
- /user_add username : add twitter user for scrape tweet
- /user_del (username) : delete twitter user from scraping list
- /user_list : show list twitter username
- /keyword_add keyword : add keyword
- /keyword_del keyword : delete keyword
- /keyword_list : show keyword list

"""
def help(update, context):
    update.message.reply_text(text_help)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(f'caused error {context.error}')

@restricted
def user_add(update, context):
    text = update.message.text.split(" ")[1]
    twitter.user_add(text)
    update.message.reply_text(f"Add twitter username {text} SUCCESS")

@restricted
def user_del(update, context):
    text = update.message.text.split(" ")[1]
    twitter.user_delete(text)
    update.message.reply_text(f"Delete twitter username {text} SUCCESS")

def user_list(update, context):
    user_list = twitter.user_read()
    update.message.reply_text(user_list)

@restricted
def keyword_add(update, context):
    text = update.message.text.split(" ")[1]
    wordlist.add(text)
    update.message.reply_text(f"Add keyword : {text} SUCCESS")

@restricted
def keyword_del(update, context):
    text = update.message.text.split(" ")[1]
    wordlist.delete(text)
    update.message.reply_text(f"Delete keyword {text} SUCCESS")

def keyword_list(update, context):
    word = wordlist.read()
    update.message.reply_text(word)

msg = """### New Tweet @{} ###
Time : {}
---------------------------------

{}

Hashtag : {}
---------------------------------
Reply {} | Retweet {} | Like {}

More detail https://twitter.com/{}/status/{}
---------------------------------
"""
def send_msg(context: CallbackContext):
    '''for send message to channel'''
    tweets = start_scrape()
    for i in tweets:
        for tweet in i['data']:
            context.bot.send_message(chat_id=config['main']['channel'], 
                text=msg.format(i['username'], tweet['time'], tweet['text'], tweet['entries']['hashtags'],
                tweet['replies'], tweet['retweets'], tweet['likes'], i['username'], tweet['tweetId']))
    
# ======== start here ======== #
def start_telebot(token, mode="polling"):
    '''Start telegram bot
    
    Args:
        mode (str): telegram mode polling or webhook, default is polling
    '''
    print(f'start telegram bot mode {mode}')
    # Get the dispatcher to register handlers
    updater = Updater(token, use_context=True)
    bg_task = updater.job_queue
    duration = config['main']['duration']
    #job_thread = threading.Thread(target=start_scrape)
    if "m" in duration:
        m = int(duration.replace("m", ""))
        bg_task.run_repeating(send_msg, interval=m*60, first=0)
    elif "h" in duration:
        h = int(duration.replace("h", ""))
        bg_task.run_repeating(send_msg, interval=(h*60)*60, first=0)
    else:
        print("Please specify duration for scrape tweet in setting.ini")
        logger.warning("Please specify duration for scrape tweet in setting.ini")
        exit()
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('user_add', user_add, pass_args=True))
    dp.add_handler(CommandHandler('user_del', user_del, pass_args=True))
    dp.add_handler(CommandHandler('user_list', user_list))
    dp.add_handler(CommandHandler('keyword_add', keyword_add, pass_args=True))
    dp.add_handler(CommandHandler('keyword_del', keyword_del, pass_args=True))
    dp.add_handler(CommandHandler('keyword_list', keyword_list))
    dp.add_error_handler(error)
    
    if mode == "polling":
        # telegram mode polling
        updater.start_polling()
        updater.idle()
    elif mode == "webhook":
        # telegram mode webhook
        port = config['webhook']['port']
        domain = config['webhook']['domain']
        cert_location = config['webhook']['cert']
        updater.start_webhook(listen='127.0.0.1', port=port, url_path=token),
        updater.bot.set_webhook(url='https://{domain}/{token}',
            certificate=open(cert_location, 'rb')
            )





