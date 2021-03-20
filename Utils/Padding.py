import random
import string


def random_rpad(s, length):
    return s + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length - len(s)))