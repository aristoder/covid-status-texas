general_data_link = "https://www.dshs.state.tx.us/coronavirus/TexasCOVID19CaseCountData.xlsx"
general_data_filename = "general_data.xlsx"
case_data_county_link = "https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyCaseCountData.xlsx"
case_data_county_filename = "case_data_county.xlsx"
fat_data_county_link = "https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx"
fat_data_county_filename = "fat_data_county.xlsx"
cumulative_tests_data_county_link = "https://dshs.texas.gov/coronavirus/TexasCOVID-19CumulativeTestsOverTimebyCounty.xlsx"
cumulative_tests_data_county_filename = "cumulative_tests_data_county.xlsx"

class data_covid:
    """This class has two sets (daily count and cumulative count) for all data: positive cases, fatalities and tests performed. This class also has a name field and all data fields are expected to be of class classOfdata."""
    def __init__(self, cum_cases, cum_fat, daily_new_cases, daily_new_fat, cum_tests = None, new_test = None,name = "Texas"):
        """Initialization function to add all the required data fields."""
        self.name = name
        self.cum_cases = cum_cases
        self.cum_fat = cum_fat
        self.daily_new_cases = daily_new_cases
        self.daily_new_fat = daily_new_fat
        self.cum_test = cum_tests
        self.new_test = new_test

class classOfdata:
    """This class is a pair of list to hold list of data and corresponding data"""
    def __init__(self, date, data, name = None):
        """Initialization function to add all the required data fields."""
        self.date = date
        self.data = data
        if name != None:
            self.name = name

    def average(self, day_period = 1):
        """This function returns moving average of data of class. The period of data is assumed as 1"""
        data = []
        # place the algorithm here
        length = len(self.data)
        for i in range(length):
            if i < int((day_period + 1)/2):         # if index error from beginning portion of the lsit
                data.append(sum(self.data[:i + int((day_period-1)/2)])/(i + int((day_period-1)/2)))
            elif i <= length - int(day_period/2):   # if no index error issue
                data.append(sum(self.data[i - int((day_period + 1)/2) : i + int((day_period-1)/2)])/day_period)
            else:                                   # if index error from end of the lsit
                data.append(sum(self.data[i - int((day_period + 1)/2):])/(length - i + int((day_period+1)/2)))
        return classOfdata(date= self.date, data= data, name= self.name)


def update_db(file_link, file_name):
    """Downloads the data from "file_link" and saves it as "file_name" with .xlsx irrespective of whether it was present in the file name argument."""
    print("Updating", file_name, "...", end = '')
    import urllib.request
    if file_name[-5:] == ".xlsx":                   # adds .xlsx if not present
        pass
    else:
        file_name = file_name + ".xlsx"
    response = urllib.request.urlopen(file_link)
    filedownload = response.read()
    with open(file_name, 'wb') as output:
        output.write(filedownload)
    print("\nFile updated!")

def clear():
    """Clears the screen independent of OS"""
    import platform
    import os
    if platform.system().lower() == 'windows':
        os.system("cls")
    else:                                           # if linux, unix or anything else
        os.system("clear")

def read_db(filename, format=1):
    """Opens the file name "filename" and assuming that the file is in correct format, returns the file with adjusted offsets."""
    import pandas
    import json
    fileinfofilename=filename + ".info"
    fileinfofound = False
    info=0
    try:
        openfile = open(fileinfofilename, "r")
    except FileNotFoundError:
        pass
    else:
        fileinfofound=True
        info=json.load(openfile)
        try:
            if info["filename"]==filename:
                pass
            else:
                fileinfofound=False
        except:
            fileinfofound=True
        openfile.close
    if format == 1:                                 # for file: case_data_county_filename, fat_data_county_filename, cumulative_tests_data_county_filename
        if fileinfofound:
            data = pandas.read_excel(filename, header=info["header"], index_col=info["index_col"], skiprows=info["skiprows"])
            try:
                int(data[data.columns[12]]["Dallas"])
            except:
                try:
                    int(data[data.columns[12]]["DALLAS"])
                except:
                    pass
                else:
                    return data
            else:
                return data
        # no correct info about file found, so searching for correct format
        correct_index_col = 0
        correct_skip_rows=0
        for i in range(2):
            data = pandas.read_excel(filename, header = 0, index_col=i, skiprows=2)
            try:
                data[data.columns[5]]['Dallas']
            except KeyError:
                continue
            else:
                correct_index_col = i
                break
        for i in range(3):
            data = pandas.read_excel(filename, header = 0, index_col=correct_index_col, skiprows=i)
            try:
                int(data[data.columns[0]][data.index[0]])
            except ValueError:
                pass
            else:
                correct_skip_rows=i
                break
        openfile=open(fileinfofilename, "w")
        json.dump({"filename":filename, "header":0, "index_col": correct_index_col, "skiprows": correct_skip_rows}, openfile)
        openfile.close()
        return data
    else:                                           # for file: general_data_filename
        if fileinfofound:
            data = pandas.read_excel(filename, sheet_name=info["sheet_name"], header=info["header"])
            if 'Date' in data.columns:
                return data        
        # no correct info about file found, so searching for correct format
        for i in range(10):
            data = pandas.read_excel(filename, sheet_name = 'Trends', header = i)
            if 'Date' in data.columns:
                openfile=open(fileinfofilename, "w")
                json.dump({"filename": filename, "header": i, "sheet_name": 'Trends'}, openfile)
                openfile.close()
                return data

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

def data_decode(*data, county = False):
    """Reads the decoded excel files and returns the data in class data_covid format.\nThis takes care of both file data representation format types."""
    try:                                            # decides if format1 or format2
        data[0][data[0].columns[0]]['Anderson']
    except:                                         # for file: general_data_filename decoded data
        date = []
        cum_cases = []
        cum_fat = []
        daily_new_cases = []
        daily_new_fat = []
        for i in range(len(data[0]['Date'])):       # for each date
            try:
                temp = str(data[0]["Date"][i].date())      # if not correnlty formatted entry or any other error
                if temp == "NaT":
                    continue
                del(temp)
            except AttributeError:
                pass
            else:                                   # data verified, append to list
                date.append(data[0]["Date"][i].date())
                cum_cases.append(data[0]["Cumulative\nCases"][i])
                cum_fat.append(data[0]["Cumulative\nFatalities"][i])
                daily_new_cases.append(data[0]["Daily\nNew\nCases"][i])
                daily_new_fat.append(data[0]["Fatalities\nby Date\nof Death"][i])
        return data_covid(name="Texas", \
        cum_cases= classOfdata(name = "Cumulative Cases", data= cum_cases, date = date),\
        cum_fat= classOfdata(name= "Cumulative Fatalities", data= cum_fat, date= date),\
        daily_new_cases= classOfdata(name= "Daily new cases", data= daily_new_cases, date= date),\
        daily_new_fat= classOfdata(name= "Daily new fatalities", data= daily_new_fat, date= date),)
    else:                                           # for all other files
        import datetime
        # file #0 = cumulative case
        # file #1 = cumulative fatalities
        # file #2 = cumulative tests
        cum_cases = classOfdata(name = "Cumulative cases", date= [], data= [])
        daily_cases = classOfdata(name= "New cases", date= [], data= [])
        cum_fat = classOfdata(name= "Cumulative fatalities", date= [], data= [])
        daily_fat = classOfdata(name= "New fatalities", date= [], data= [])
        daily_tests = classOfdata(name= "New tests", date= [], data= [])
        cum_tests = classOfdata(name= "Cumulative tests", date= [], data= [])
        for current_file in range(len(data)):                       # per file
            for current_row in data[current_file].index:            # per county
                county_name = current_row
                if isitcountyname(county_name):                         # valid county name
                    pass
                else:
                    continue
                if county:                                            # if for a specific county
                    if county_name.lower() != county.lower():           # proceed only if county name matches to the argument
                        continue
                # creates empty lists
                date_list_fromcurrentfile = []
                data_list_fromcurrentfile = []
                for current_column in data[current_file].columns:   # per date
                    try:
                        current_date = getdate(str(current_column))
                    except ValueError:                              # invalid date
                        continue
                    else:
                        if current_date == -1:                      # invalid date                 
                            continue
                        try:                                        # valid date
                            idata = int(data[current_file][current_column][current_row])
                        except ValueError:                          # invalid data
                            if data[current_file][current_column][current_row] == ".":
                                idata = 0
                            else:
                                continue
                        else:                                       # valid date, add the data to list
                            data_list_fromcurrentfile.append(idata)
                            date_list_fromcurrentfile.append(current_date)
                if current_file == 0:                               # file = cumulative cases
                    cum_cases.data = data_list_fromcurrentfile
                    cum_cases.date = date_list_fromcurrentfile
                    daily_cases.date = date_list_fromcurrentfile
                    for i in range(len(cum_cases.data)):            # produces data for daily cases
                        if i == 0:
                            daily_cases.data.append(cum_cases.data[i])
                        else:
                            daily_cases.data.append(cum_cases.data[i] - cum_cases.data[i-1])
                elif current_file == 1:                             # file = cumilative fatalities
                    cum_fat.data = data_list_fromcurrentfile
                    cum_fat.date = date_list_fromcurrentfile
                    daily_fat.date = date_list_fromcurrentfile
                    for i in range(len(cum_fat.data)):              # produces data for daily fatalities
                        if i == 0:
                            daily_fat.data.append(cum_fat.data[i])
                        else:
                            daily_fat.data.append(cum_fat.data[i] - cum_fat.data[i-1])
                elif current_file == 2:                             # file = cumulative test
                    cum_tests.data = data_list_fromcurrentfile
                    cum_tests.date = date_list_fromcurrentfile
                    daily_tests.date = date_list_fromcurrentfile
                    for i in range(len(cum_tests.data)):            # produce data for daily tests
                        if i == 0:
                            daily_tests.data.append(cum_tests.data[i])
                        else:
                            daily_tests.data.append(cum_tests.data[i] - cum_tests.data[i-1])
        if len(daily_cases.data) == 0:                              # if no data found (if county name does not match or all invalid data)
            return -1
        return data_covid(cum_cases=cum_cases, cum_fat= cum_fat, daily_new_cases= daily_cases, daily_new_fat= daily_fat, cum_tests= cum_tests, new_test= daily_tests, name = county)

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
    pyplot.plot(_data.date, _data.data)
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

def end_menu(data):
    """Menu of options for displaying the data."""
    from datetime import date
    clear()
    inp = menu_function("View total data", "View relative data")    # pre-menu menu
    if inp == 1:            # if depth of data becomes infinite
        depth = 0
    else:                   # reads the depth of data desired
        while True:         # loops to validate depth
            try:
                depth = int(input("\nEnter the depth of data "))
            except ValueError:
                print("Invalid value\nTry again!")
            else:
                break
    while True:
        from getkey import getkey
        clear()
        menu_options = ["View graph of new cases", "View graph of new fatalities", "View graph of cumulative cases", "View graph of cumulative fatalities", "Total cases", "Total fatalities", "New cases in last 24 hours", "New fatalities in last 24 hours", "New cases - 14 days moving average", "New cases - 2x moving average","Custom moving average", "Go back", "Exit"]
        inp = menu_function(*menu_options)
        clear()
        if inp == menu_options.index("View graph of new cases") + 1:
            plot(data.daily_new_cases, depth= depth, placeName= data.name)
        elif inp == menu_options.index("View graph of new fatalities") + 1:
            plot(data.daily_new_fat, depth = depth, placeName= data.name)
        elif inp == menu_options.index("View graph of cumulative cases") + 1:
            plot(data.cum_cases, depth = depth, placeName= data.name)
        elif inp == menu_options.index("View graph of cumulative fatalities") + 1:
            plot(data.cum_fat, depth = depth, placeName= data.name)
        elif inp == menu_options.index("Total cases") + 1:
            todisplay, index = returnlastvaliddata(data.cum_cases.data)
            print("Total cases in ", data.name, ": ", todisplay, sep= "")
            getkey()
        elif inp == menu_options.index("Total fatalities") + 1:
            todisplay, index = returnlastvaliddata(data.cum_fat.data)
            print("Total fatalities in ", data.name, ": ",todisplay, sep= "")
            getkey()
        elif inp == menu_options.index("New cases in last 24 hours") + 1:
            todisplay, index = returnlastvaliddata(data.daily_new_cases.data, daily=True)
            print("New cases in", data.name, date_relation(data.daily_new_cases.date[index]), ":", todisplay)
            getkey()
        elif inp == menu_options.index("New fatalities in last 24 hours") + 1:
            todisplay, index = returnlastvaliddata(data.daily_new_fat.data, daily=True)
            print("New fatalities in", data.name, date_relation(data.daily_new_fat.date[index]), ":", todisplay)
            getkey()
        elif inp == menu_options.index("New cases - 14 days moving average") + 1:
            plot(data.daily_new_cases.average(day_period= 14), depth = depth, placeName= data.name)
        elif inp == menu_options.index("New cases - 2x moving average") + 1:
            plot(data.daily_new_cases.average(day_period= 14).average(day_period=14), depth = depth, placeName= data.name)
        elif inp == menu_options.index("Custom moving average") + 1:
            # custom moving average menu
            print("Choose data:")
            custom_data_choice = menu_function("Daily new cases", "Cumulative cases", "Daily new fatalities", "Cumulative new fatalities", "Daily new tests", "Cumulative tests", _clear= False)
            average_width = 14
            while True:                 # loop to validate average sample width
                try:
                    average_width = int(input("Enter the sample width for moving average: "))
                except ValueError:
                    print("Try another value")
                else:
                    if average_width > 1:
                        break
                    else:
                        "Please enter a value greater than 1"                
            if custom_data_choice == 1:
                plot(data.daily_new_cases.average(average_width), depth= depth, placeName= data.name)
            elif custom_data_choice == 2:
                plot(data.cum_cases.average(average_width), depth= depth, placeName= data.name)
            elif custom_data_choice == 3:
                plot(data.daily_new_fat.average(average_width), depth= depth, placeName= data.name)
            elif custom_data_choice == 4:
                plot(data.cum_fat.average(average_width), depth= depth, placeName= data.name)
            elif custom_data_choice == 5:
                if data.name.lower() == "texas":
                    input("This data is not available right now!")
                    continue
                plot(data.new_test.average(average_width), depth= depth, placeName= data.name)
            elif custom_data_choice == 6:
                if data.name.lower() == "texas":
                    input("This data is not available right now!")
                    continue
                plot(data.cum_test.average(average_width), depth= depth, placeName= data.name)
        elif inp == menu_options.index("Go back") + 1:
            return True
        elif inp == menu_options.index("Exit") + 1:
            return False
        else:
            clear()
            quit()
        clear()

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

def menu_county(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county, county = None):
    """Menu to select a county."""
    if county == None:                    # if no county name provided
        while True:                     # loop to validate county name
            clear()
            county_name = input("Enter the name of the county: ")
            data_county = data_decode(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county, county= county_name)
            if data_county == -1:       # invalid county name or no such data found
                print("county name not found.")
                print("Press \"Enter\" to exit, any other key to try again")
                t = takesingleinput(False)
                if t == "\n":
                    return
            else:
                break
    else:                               # county name provided in the argument
        data_county = data_decode(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county, county= county)
    repeat = end_menu(data_county)      # calling end_menu with the correctly loaded data
    return repeat

def menu(data_texas, xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county):
    """Menu to select state or county."""
    clear()
    repeat = 0
    while True:
        t = menu_function("Texas", "Dallas", "Any other county", "Exit")
        if t == 1:
            repeat = end_menu(data_texas)
        elif t == 2:
            repeat = menu_county(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county, county= "Dallas")
        elif t == 3:
            repeat = menu_county(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county)
        elif t == 4:                                # exits
            return
        if repeat != True:                          # exits (triggered if passed by other menus)
            return repeat

def menu_function(*args, takeanyinput = False, _clear = True):
    """Simple menu function to display the passed strings as menu options and return the correct choosen answer."""
    if _clear:
        clear()
    t = 0
    numberofoptions = len(args)
    if numberofoptions > 9:                 # not triggered in recursive calls
        start = 0
        end = 8
        count = 0
        while True:
            if end < numberofoptions - 1:   # need to display "More" as an menu option
                response = menu_function(*args[start:end], "More", takeanyinput= takeanyinput)
                if response == 9:           # if "More" pressed
                    start = start + 8
                    end = end + 8
                    count = count + 1
                else:                       # base case
                    return response + (count*8)
            elif (end + 1) == numberofoptions:# 9th option is the last option
                response = menu_function(*args[start:numberofoptions], takeanyinput= takeanyinput)
                return response + (count*8)
            else:                           # no 9th option needed
                response = menu_function(*args[start:end], takeanyinput= takeanyinput)
                return response + (count*8)
    else:                                   # basic call for no need to display "More"
        for i in range(numberofoptions):    # displaying options
            print(i + 1, '. ', args[i], sep='')
        if takeanyinput:
            t = takesingleinput(outputint=False)
        else:
            while True:
                t = takesingleinput()
                if (t > 0) and (t <= len(args)):# checking for valid response
                    break
        return t

def responseYes(reponse):
    if reponse.lower() in ('y', 'yes', 'ye', 'yep'):
        return True
    else:
        return False

def installThisModule(modulename):
    import os
    os.system("pip3 install " + modulename + " > /dev/null")

if __name__ == "__main__":
    try:
        clear()
        # accessing internet to update the local files
        t = input("Do you want to update the database from the server? ")
        if responseYes(t):
            update_db(general_data_link, general_data_filename)
            update_db(case_data_county_link, case_data_county_filename)
            update_db(fat_data_county_link, fat_data_county_filename)
            update_db(cumulative_tests_data_county_link, cumulative_tests_data_county_filename)
        # reading files into memory
        clear()
        print("Reading files....")
        xceldata_texas = read_db(general_data_filename, format=0)
        xceldata_cumulative_case_county = read_db(case_data_county_filename, format=1)
        xceldata_cumulative_fat_county = read_db(fat_data_county_filename, format=1)
        xceldata_cumulative_tests_county = read_db(cumulative_tests_data_county_filename, format=1)
        # decoding and menu calling
        data_texas = data_decode(xceldata_texas)
        del(xceldata_texas)
        menu(data_texas, xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county)
        clear()
        pass
    except ModuleNotFoundError:
        # check installation of getkey
        try:
            import getkey
        except ModuleNotFoundError:
            response=input("Module getkey not found.\nDo you want to install getkey? (Internet connection required).")
            if responseYes(response):
                installThisModule("getkey")
                try:
                    import getkey
                except ModuleNotFoundError:
                    print("Module installation failed. Please run this command \"pip3 (or pip) install getkey\" and try fixing manually.")
                    input()
                    quit()
                else:
                    print("Installation successful.")
            else:
                quit()
        # check installation of xlrd
        try:
            import xlrd
        except ModuleNotFoundError:
            response=input("Module xlrd not found.\nDo you want to install xlrd? (Internet connection required).")
            if responseYes(response):
                installThisModule("xlrd")
                try:
                    import xlrd
                except ModuleNotFoundError:
                    print("Module installation failed. Please run this command \"pip3 (or pip) install xlrd\" and try fixing manually.")
                    input()
                    quit()
                else:
                    print("Installation successful.")
            else:
                quit()
        # check installation of pandas
        try:
            import pandas
        except ModuleNotFoundError:
            response=input("Module pandas not found.\nDo you want to install pandas? (Internet connection required).")
            if responseYes(response):
                installThisModule("pandas")
                try:
                    import pandas
                except ModuleNotFoundError:
                    print("Module installation failed. Please run this command \"pip3 (or pip) install pandas\" and try fixing manually.")
                    input()
                    quit()
                else:
                    print("Installation successful.")
            else:
                quit()
        # check installation of matplotlib
        try:
            import matplotlib
        except ModuleNotFoundError:
            response=input("Module matplotlib not found.\nDo you want to install matplotlib? (Internet connection required).")
            if responseYes(response):
                installThisModule("matplotlib")
                try:
                    import matplotlib
                except ModuleNotFoundError:
                    print("Module installation failed. Please run this command \"pip3 (or pip) install matplotlib\" and try fixing manually.")
                    input()
                    quit()
                else:
                    print("Installation successful.")
            else:
                quit()