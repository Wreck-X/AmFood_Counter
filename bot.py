from telebot import TeleBot
import time
import datetime
import threading
import os
import csv

# from dotenv import load_dotenv
# load_dotenv()
bot = TeleBot(os.getenv('amfoodkey'))
os.environ["TZ"] ="Asia/Kolkata"
time.tzset()

blist = []
glist = []
ycount = 0
ncount = 0
boys = 0
botRunning = False
girls = 0

@bot.message_handler(commands=['KEY'])
def sendpoll(message):
    global boys
    global girls
    options = ['YES','NO']
    bot.send_poll(message.chat.id,f"How many of you will have food from staff mess ?",options)
    boys  = 0
    girls = 0


@bot.message_handler(commands=['Poll'])
def sendpoll(message):
    global ycount
    global boys
    global girls
    d = {'Friday':'Satudary','Saturday':'Sunday'}
    today = datetime.datetime.now()
    day_name = today.strftime("%A")
    print(day_name)

    options = ['YES','NO']
    pollid = bot.send_poll(message.chat.id,f"How many of you will have food from staff mess on d[day_name]?\n The poll will close after 4 hours.",options,is_anonymous = False).message_id
    time.sleep(14400)
    bot.send_message(message.chat.id,f"Poll is closed! \n Voted yes = {ycount} \n Boys = {boys}\n Girls = {girls}")
    bot.delete_message(message.chat.id,pollid)
    boys = 0
    girls = 0
    ycount = 0

@bot.poll_answer_handler()
def handle_poll_answer(pollAnswer):
    global boys
    global girls
    global blist
    global glist
    user_id = pollAnswer.user.id
    user_name  = pollAnswer.user.username
    print("Username :",user_name)
    print("User ID:", user_id)
    global ycount,ncount
    if pollAnswer.option_ids == [0]:
        ycount += 1
        with open('members.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if str(user_name) == str(row[0]):
                    if  row[6] == 'M':
                        boys += 1
                        blist.append(str(user_name))

                    elif row[6] == 'F':
                        girls += 1
                        glist.append(str(user_name))

                line_count += 1
        print(glist,blist)
    else:
        if user_name in blist :
            blist.remove(user_name)
            boys -= 1
            ycount -= 1
        elif user_name in glist:
            glist.remove(user_id)
            girls -= 1
            ycount -= 1
        ncount += 1
        print(glist,blist)
    pass


@bot.message_handler(commands=['start'])
def start(message):
    global botRunning
    if botRunning == False:

        chat_id = message.chat.id
        user_id = message.from_user.id
        chat_member = bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        print(chat_member)
        botRunning = True
        bot.reply_to(message,"started")
        thread = threading.Thread(target=timer,args=(message,))
        thread.start()
    else:
        bot.reply_to(message,"Already running")


def timer(message):
    while True:
        today = datetime.datetime.now()
        day_name = today.strftime("%A")
        now = datetime.datetime.now()
        time_now = now.strftime("%H:%M:%S")
        print(time_now)
        if time_now == '16:00:00' and (day_name == 'Friday' or day_name == 'Monday'):
            print(3)
            sendpoll(message)
        time.sleep(1)






bot.infinity_polling()