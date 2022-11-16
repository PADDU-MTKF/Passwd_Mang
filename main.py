# my modules ************************************************************************************
import otp
from MyDb import *
from mail import *
from dotenv import load_dotenv
import os
import telebot
import time
import random
# https://github.com/eternnoir/pyTelegramBotAPI
load_dotenv()

bot = telebot.TeleBot(os.getenv('API_KEY'))


# bot will only work with a personal group not any other group or chat


def permission(message):
    if str(message.chat.id) == os.getenv('CID'):
        return True
    return False


def clear_message(message_id):
    time.sleep(10)
    i = 0
    while True:
        try:
            bot.delete_message(os.getenv('CID'), message_id+i)
            i -= 1
        except:
            break


def finish(message, add=0, tim=2):
    bot.send_message(message.chat.id, 'Have A Nice Time ....')
    time.sleep(tim)
    clear_message(message.message_id+add)


def save(message, paswd, try_count=0):
    try_count += 1
    if try_count > 3:
        msg = bot.send_message(message.chat.id, "OOPS!!!  Time out....")
        finish(message, 1)

    else:
        try:
            title = message.text.lower()
            Db = str(message.chat.id)

            DATA_LIST = [
                (title, paswd)
            ]

            check = add_data(Db, "Dont_worry", DATA_LIST)
            if check != True:
                try:
                    COL_LIST = [
                        # extra is full command
                        {'col_name': 'Title', 'col_type': 'text',
                            'extra': 'primary key not null'},
                        {'col_name': 'paswd', 'col_type': 'text'}
                    ]
                    check = create_table(Db, "Dont_worry", COL_LIST)
                    check = add_data(Db, "Dont_worry", DATA_LIST)

                    if check != True:
                        raise Exception
                    else:
                        p = "*ENJOY :-* `"+str(paswd)+"`"
                        msg = bot.send_message(
                            message.chat.id, p, parse_mode='MARKDOWN')
                        finish(message, 1)
                except:
                    msg = bot.send_message(
                        message.chat.id, "Try Different name ....")
                    bot.register_next_step_handler(msg, save, paswd, try_count)
            else:
                p = "*ENJOY :-* `"+str(paswd)+"`"
                msg = bot.send_message(
                    message.chat.id, p, parse_mode='MARKDOWN')
                finish(message, 1)

        except Exception as e:
            msg = bot.send_message(message.chat.id, "Try Different name ....")
            bot.register_next_step_handler(msg, save, paswd, try_count)


def check_args(message, args):
    text = message.text.lower()
    text = text.strip()
    if text == 'd':
        paswd = otp.get_passwd()
        p = "*ENJOY :-* `"+str(paswd)+"`"

    else:
        text = text.split(',')
        bol = {'T': True, 'F': False, 't': True, 'f': False}
        size, d, l, sp = 15, True, True, True
        try:
            size = int(text[0])
            d = bol[text[1]]
            l = bol[text[2]]
            sp = bol[text[3]]
        except:
            pass
        paswd = otp.get_passwd(size, d, l, sp)
        p = "*ENJOY :-* `"+str(paswd)+"`"

    if args == 'random':
        bot.send_message(message.chat.id, p, parse_mode='MARKDOWN')
        finish(message, 1)
    elif args == 'create':
        msg = bot.send_message(message.chat.id, "What to Save as ? ")
        bot.register_next_step_handler(msg, save, paswd)


def display(message, try_count=0):
    try_count += 1
    if try_count > 3:
        msg = bot.send_message(message.chat.id, "OOPS!!!  Time out....")
        finish(message, 1)
    else:
        try:
            title = "Title='"+message.text.lower()+"'"
            Db = str(message.chat.id)

            result = get_one(Db, "Dont_worry", title, COL='paswd')

            if result == []:
                msg = bot.send_message(
                    message.chat.id, "No such name ...\n Try Different name ....")
                bot.register_next_step_handler(msg, display, try_count)
            else:
                result = result[0][0]
                p = "*ENJOY :-* `"+str(result)+"`"
                msg = bot.send_message(
                    message.chat.id, p, parse_mode='MARKDOWN')
                finish(message, 1)

        except Exception as e:
            msg = bot.send_message(message.chat.id, "Try again ....")
            bot.register_next_step_handler(msg, display, try_count)


def next(message, args):
    if args in ['create', 'random']:
        para = '''
        Give the following.....

        + Length of password (default 15)
        + Include *Digitise*        (default T)
        + Include *Letter*           (default T)
        + Include *Special*         (default T)

    In the format Eg:-

               *20,T,T,F*
                   Or
            *D (for default)*

        '''
        msg = bot.send_message(message.chat.id, para)
        bot.register_next_step_handler(msg, check_args, args)

    elif args == 'see':
        try:
            Db = str(message.chat.id)

            result = get_all(Db, "Dont_worry", COL='Title')
            print(result)
            if result == []:
                msg = bot.send_message(
                    message.chat.id, "Nothing is Everything :)")

            else:
                reslt = ""
                for each in result:
                    reslt += ("\t"*13+str(each[0])+"\n")
                p = "ENJOY :-\n"+str(reslt)
                msg = bot.send_message(
                    message.chat.id, p)
                finish(message, 1, 6)

        except Exception as e:
            msg = bot.send_message(message.chat.id, "Nothing is Everything :)")

    else:
        # read function
        msg = bot.send_message(
            message.chat.id, "Which password do you want ? ")
        bot.register_next_step_handler(msg, display)


def check_otp(message, args):
    op = str(args[0])
    secret = args[1]
    a = int(op[-2])
    b = int(op[-1])
    if secret == '+':
        result = a+b
    elif secret == '-':
        result = a-b
    elif secret == '*':
        result = a*b

    result = str(op+str(result))

    if str(message.text) == str(result):
        next(message, args[2])
    else:
        bot.send_message(message.chat.id, 'Invalid OTP...\nSTART AGAIN')
        time.sleep(2)
        clear_message(message.message_id)


def send_otp(message, cmd):
    op = otp.get_otp()
    mail_body = f"Your OTP for Logging :- {op}"
    secret = ['*', '+', '-']
    s = random.choice(secret)
    msg = bot.send_message(message.chat.id, f'ENTER OTP ....{s}')
    send_email(mail_body)
    bot.register_next_step_handler(msg, check_otp, (op, s, cmd,))


# ************************************************************************************************************************************

@bot.message_handler(commands=['help', 'start'], func=permission)
def send_help(message):
    text = '''
    These are the commands.....

    /create         :- Create Password
    /read            :- Read Password
    /random      :- Generate Random
    /quick           :- Generate Quick Password
    /seeall       :- See All Password Title
    /reminder    :- Set Reminder and get email
    /help              :- Show this help
    '''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['quick'], func=permission)
def quick_gen(message):
    p = otp.get_passwd()
    p = "*ENJOY :-*  `"+str(p)+"` "
    bot.send_message(message.chat.id, str(p), parse_mode='MARKDOWN')
    finish(message, 1)


@bot.message_handler(commands=['create'], func=permission)
def create_pass(message):
    send_otp(message, 'create')
    #bot.register_next_step_handler(msg, get_rep,p)


@bot.message_handler(commands=['read'], func=permission)
def read_pass(message):
    send_otp(message, 'read')


@bot.message_handler(commands=['random'], func=permission)
def random_pass(message):
    next(message, 'random')


@bot.message_handler(commands=['seeall'], func=permission)
def read_pass(message):
    send_otp(message, 'see')


# ************************************************************************************************************
@bot.message_handler(commands=['reminder'], func=permission)
def reminder(message):
    global get_args
    # get_args=True
    # opt verification
    # p = otp.get_passwd()
    bot.send_message(message.chat.id, "feature for next time :)")
    finish(message, 1)


@bot.message_handler(func=permission)
def echo_all(message):
    bot.send_message(message.chat.id, message.text+" from me")
    finish(message, 1)


bot.infinity_polling()

# ************************************************************************************************
