import random as r

def gen_otp_passwd(otp_length=10,get_digits=True,get_letters=True,get_special=True):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits  = "0123456789"
    special = "@#&_-"
    otp=str()
    choice_list=list()

    if get_digits==True:
        choice_list.append(digits)
    if get_letters==True:
        choice_list.append(letters)
        otp +=r.choice(letters)
        otp_length-=1
    if get_special==True:
        choice_list.append(special)
    if choice_list==[]:
        choice_list.append(digits)
        choice_list.append(letters)

    for i in range(otp_length):
        otp +=r.choice(r.choice(choice_list))
    return otp

def get_otp(otp_length=6,get_digits=True,get_letters=False,get_special=False):
    
    return(gen_otp_passwd(otp_length,get_digits,get_letters,get_special))

def get_passwd(otp_length=15,get_digits=True,get_letters=True,get_special=True):
    return(gen_otp_passwd(otp_length,get_digits,get_letters,get_special))
