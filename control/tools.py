import logging

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Adapted from http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
import control


def getRed(prt): return u"\033[91m{}\033[00m".format(prt)
def prRed(prt): print(getRed(prt))


def getGreen(prt): return u"\033[92m{}\033[00m".format(prt)
def prGreen(prt): print(getGreen(prt))


def getYellow(prt): return u"\033[93m{}\033[00m".format(prt)
def prYellow(prt): print(getYellow(prt))


def getLightPurple(prt): return u"\033[94m{}\033[00m".format(prt)
def prLightPurple(prt): print(getLightPurple(prt))


def getPurple(prt): return u"\033[95m{}\033[00m".format(prt)
def prPurple(prt): print(getPurple(prt))


def getCyan(prt): return u"\033[96m{}\033[00m".format(prt)
def prCyan(prt): print(getCyan(prt))


def getLightGray(prt): return u"\033[97m{}\033[00m".format(prt)
def prLightGray(prt): print(getLightGray(prt))


def getBlack(prt): return u"\033[98m{}\033[00m".format(prt)
def prBlack(prt): print(getBlack(prt))

# Code 4 - underline
# Code 7 - white background
# Code 30 - 37, dull colours, white, red, yellow, blue, purple, green, grey
# Code 40 - 47, background analog to 30 - 37
# Code 90 - 97 bright text colour, dark grey, red, green, yellow, light blue, purple, cyan, black
# Code 100-107 background colour
def getCustom(prt, code=98, code2=00): return u"\033[{}m{}\033[{}m".format(code, prt, code2)

# A decorator function that takes care of starting a coroutine
# automatically on call.


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr

    return start


def copy_drive(gauth):
    '''Create a deep copy of the GoogleAuth object,
    and the GoogleDrive object for use by another thread.
    :param drive: the GoogleAuth object to copy
    :returns: a tuple with the copies of the GoogleAuth and a GoogelDrive object'''
    old_gauth = gauth
    gauth = GoogleAuth()
    gauth.credentials = old_gauth.credentials
    gauth.Authorize()
    drive = GoogleDrive(gauth)
    return (gauth, drive)

def setup_logger(name, log_level=logging.DEBUG, use_cl_logger=True):
    # Set up FUSE logging.
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if use_cl_logger:  # use command line logger.
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    fh = logging.FileHandler(control.constants.LOGS_FOLDER + name + '.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger
