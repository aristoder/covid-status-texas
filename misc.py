from classes import data_covid, classOfdata

def clear():
    """Clears the screen independent of OS"""
    import platform
    import os
    if platform.system().lower() == 'windows':
        os.system("cls")
    else:                                           # if linux, unix or anything else
        os.system("clear")

def isitcountyname(text):
    """Tests if the passed string is a countyname. This is checked by the assumption that most county names are one word only.\nNote that Corpus Christi is an exception."""
    try:
        t = len(text.split())
    except:                                         # catch-all exception
        return False
    else:
        if t != 1:                                  # if one word
            return False
        else:                                       # if more than one word
            return True

def neg(number):
    try:
        int(number)
    except:
        return None
    else:
        return -1*number

def c_int(number):
    startingpoint = 0
    for i in range(len(number)):
        if number[i] == "0":
            startingpoint+=1
        elif number[i] == " " or number[i] == "-":
            raise ValueError
        else:
            break
    else:
        return int(number)    
    return int(number[startingpoint:])

def breakintonumber(arg):
    index = 0
    _range = [n for n in range(len(arg))]                        # to substitute "for i in range(len(arg))" and facilitate in jumping iterations
    result=()
    try:                                            # catch-all exception case
        arg = str(arg)
    except:
        raise ValueError
    while index in _range:                                          # starts looking from the end of the list
        extracted=None
        for numberofdigits in range(1,len(arg)):
            possible=None
            tobechecked=None
            if index == 0:
                tobechecked=arg[neg(index+numberofdigits):]
            else:
                tobechecked=arg[neg(index+numberofdigits):neg(index)]
            try:
                possible=c_int(tobechecked)
            except ValueError:
                break
            else:
                extracted=possible
        if extracted == None:
            index+=1
            continue
        else:
            result=extracted,*result
            index += numberofdigits
    return result

def getdate(text, year = 2020):
    """Extracts month and date and return datetime object"""
    from datetime import date
    returndata = {"Date": 0, "Month": 0, "Year": year}
    numbers=breakintonumber(text)
    for i in range(len(numbers)-1):
        if numbers[i] > 0 and numbers[i] < 13 and numbers[i+1] > 0 and numbers[i+1] < 32:
            returndata["Month"]=numbers[i]
            returndata["Date"]=numbers[i+1]
            break
    if returndata["Month"] != 0:                                    # found both month and date
        pass
    else:
        for i in range(len(numbers)):
            if numbers[i] > 0 and numbers[i] < 32:
                returndata["Date"]=numbers[i]
                break
        monthlist = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
        monthabbrlist = ["jan", "feb", "mar", "apr", "may", "june", "july", "aug", "sept", "oct", "nov", "dec"]
        words = text.split()
        for i in range(len(words)):
            try:
                index = monthlist.index(words[i].lower())            # look for month written in full
            except ValueError:
                try:
                    index = monthabbrlist.index(words[i].lower())    # look for month written in abbrevated form
                except ValueError:
                    continue                                        # no hit
                else:
                    returndata["Month"] = index + 1                 # adding month to returndata
                    break
            else:
                returndata["Month"] = index + 1                     # adding month to returndata
                break
        else:
            return - 1                                              # no hit
    return date(year = year, month = returndata["Month"], day = returndata["Date"])

def takesingleinput(outputint = True):
    """Reads input from keyboard without echoing on screen. Returns as integer if outputint = True (Default), else returns as string."""
    from getkey import getkey
    input_ = getkey()
    if outputint == True:
        try:
            input_ = int(input_)                    # changed the output to int
        except ValueError:
            return -1
    return input_

def plot(_data, placeName, depth = 0):
    """Takes in data (assuming in classOfdata class format), and plots the last "depth" number of points."""
    from matplotlib import pyplot
    if _data == None:
        input("There has been an error! No such data found!")
        return
    pyplot.plot(_data.date[depth*-1:], _data.data[depth*-1:])
    if depth == 0:
        pyplot.suptitle(_data.name + " in " + placeName)
    else:
        pyplot.suptitle(_data.name + " in past " + str(depth) + " days" + " in " + placeName)
    pyplot.ylabel(_data.name)
    pyplot.show()

def returnlastvaliddata(arg, daily = False):   
    index=-1 
    if daily:
        if arg[index] == ".":
            return 0, index
    else:
        index = -1
        while True:
            if arg[index] == ".":
                index=index-1
            else:
                break
    return int(arg[index]), index

def date_relation(_input):
    from datetime import date
    today = date.today()
    diff =  str(today - _input).split()[0]
    if diff == "0:00:00":
        return "Today"
    elif diff == '1':
        return "Yesterday"
    else:
        return "on " + str(_input)[-5:-3] + " - " + str(_input)[-2:]

def responseYes(reponse):
    if reponse.lower() in ('y', 'yes', 'ye', 'yep'):
        return True
    else:
        return False

def installThisModule(modulename):
    import os
    os.system("pip3 install " + modulename + " > /dev/null")