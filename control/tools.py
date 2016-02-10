# Adapted from http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python

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