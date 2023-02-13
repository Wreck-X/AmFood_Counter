from telebot import TeleBot
import os,json,time
bot = TeleBot(os.getenv('amfoodkey'))

blist = []
glist = []
@bot.message_handler(commands=['start'])
def start(message):
    global botRunning
    botRunning = True
    bot.reply_to(message,"started")

@bot.message_handler(commands=['sendPoll'])
def sendpoll(message):
    global glist
    global blist
    options = ['YES','NO']
    bot.send_poll(message.chat.id,"Ye or Nay for food?",options, is_anonymous=False ,open_period=10)
    time.sleep(10)
    bot.send_message(message.chat.id,','.join(votelist)+" has voted")
    glist = []
    blist = []
@bot.poll_answer_handler()
def handle_poll_answer(pollAnswer):
    votelist.append(pollAnswer.user.first_name)

    
bot.infinity_polling()