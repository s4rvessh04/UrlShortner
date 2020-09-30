import random
import string
from database import DataBase


def slinkGen():
    chars = string.ascii_letters + string.digits
    slink = ""
    
    charLength = 0
    while charLength < 8: 
        slink += random.choice(chars)
        charLength+=1
    finishedLink = slink
    
    return finishedLink

def shortenUrls():
    chars = string.ascii_letters + string.digits
    slink = ""
    
    charLength = 0
    while charLength < 16:
        slink += random.choice(chars)
        charLength+=1

    return slink