from telebot import TeleBot
import os,json,time
bot = TeleBot(os.getenv('amfoodkey'))

blist = []
glist = []
ycount = 0
ncount = 0

@bot.message_handler(commands=['start'])
def start(message):
    global botRunning
    botRunning = True
    bot.reply_to(message,"started")

@bot.message_handler(commands=['sendPoll'])
def sendpoll(message):
    global glist,blist,ycount,ncount
    options = ['YES','NO']
    bot.send_poll(message.chat.id,"Ye or Nay for food?",options, is_anonymous=False ,open_period=10)
    time.sleep(10)
    # bot.send_message(message.chat.id,','.join(votelist)+" has voted")
    glist = []
    blist = []
    ycount = 0
    ncount = 0

@bot.poll_answer_handler()
def handle_poll_answer(pollAnswer):
    global ycount
    global ncount
    if pollAnswer.option_ids == [0]:
        ycount += 1
    else:
        ncount += 1
    pass
    
bot.infinity_polling()