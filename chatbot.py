##this file is based on version 13.7 of python telegram chatbot##and version 1.26.18 of urllib3##chatbot.pyimport telegram
from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters#The messageHandler is used for all message updates
import configparser
from telegram import Update 
import logging
import redis
from chatgpt_hkbu import HKBU_ChatGPT

def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update:"+ str(update))
    logging.info("context:"+ str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

global redis1
def main():
    #Load your token and create an Updater for your Bot
    config =configparser.ConfigParser()
    config.read('config.ini')
    updater =Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']),use_context=True)
    dispatcher =updater.dispatcher
    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']), decode_responses=(config['REDIS']['DECODE_RESPONSE']), username=(config['REDIS']['USER_NAME']))
#You can set this logging module,
#so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s -%(message)s',level=logging.INFO)
#register a dispatcher to handle message:#here we register an echo dispatcher
    #echo_handler =MessageHandler(Filters.text &(~Filters.command),echo)
    #dispatcher.add_handler(echo_handler)
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler('hello', hello_command))
#To start the bot:
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)
    updater.start_polling()
    updater.idle()

def echo(update,context):
    reply_message =update.message.text.upper()
    logging.info("Update:"+str(update))
    logging.info("context:"+str(context))
    context.bot.send_message(chat_id=update.effective_chat.id,text=reply_message)

def help_command(update: Update, context: CallbackContext) -> None:
   """Send a message when the command /help is issued."""
   update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
   """Send a message when the command /add is issued."""
   try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0] # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
   except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def hello_command(update: Update, context:CallbackContext) -> None:
    try:
        name = context.args[0]
        update.message.reply_text(f'Nice to meet you!{name}')
    except(IndexError, ValueError):
        update.message.reply_text('Usage: /hello <name>')

if __name__=='__main__':
    main()