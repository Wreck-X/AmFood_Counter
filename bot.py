from telebot import TeleBot
import os

bot = TeleBot(os.getenv('amfood'))



@bot.message_handler(commands=['start'])
def start(message):
    global botRunning
    botRunning = True
    bot.reply_to(message,"started")


@bot.message_handler(commands=['sendPoll'])
def sendpoll(message):
    options = ['YES','NO']
    bot.send_poll(message.chat_id,"Ye or Nay for food?",options)