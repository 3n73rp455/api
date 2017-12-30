import random
import string


def generate_key():
    char_set = string.ascii_letters + string.digits
    key = ''.join([char_set[random.randint(0, len(char_set) - 1)] for i in range(48)])
    return key

def generate_password(pw_len):
    pw = []
    for i in range(pw_len//3):
        pw.append(string.ascii_letters[random.randrange(len(string.ascii_letters))])
        pw.append(string.digits[random.randrange(len(string.digits))])
        pw.append(string.punctuation[random.randrange(len(string.punctuation))])
    for i in range(pw_len-len(pw)):
        pw.append(string.ascii_letters[random.randrange(len(string.ascii_letters))])
    random.shuffle(pw)
    pw = ''.join(pw)
    return pw