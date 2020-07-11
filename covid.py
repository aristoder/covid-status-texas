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
    def __init__(self, date, data, name = None):
        self.date = date
        self.data = data
        if name != None:
            self.name = name

    def average(self, day_period = 1):
        data = []
        # place the algorithm here
        length = len(self.data)
        for i in range(length):
            if i < int((day_period + 1)/2):
                data.append(sum(self.data[:i + int((day_period-1)/2)])/(i + int((day_period-1)/2)))
            elif i <= length - int(day_period/2):
                data.append(sum(self.data[i - int((day_period + 1)/2) : i + int((day_period-1)/2)])/day_period)
            else:
                data.append(sum(self.data[i - int((day_period + 1)/2):])/(length - i + int((day_period+1)/2)))
        return classOfdata(date= self.date, data= data, name= self.name)


def update_db(file_link, file_name):
    print("Updating", file_name, "...", end = '')
    import urllib.request
    if file_name[-5:] == ".xlsx":
        pass
    else:
        file_name = file_name + ".xlsx"
    response = urllib.request.urlopen(file_link)
    filedownload = response.read()
    with open(file_name, 'wb') as output:
        output.write(filedownload)
    print("\nFile updated!")

def clear():
    import platform
    import os
    if platform.system().lower() == 'windows':
        os.system("cls")
    else:
        os.system("clear")

def read_db(filename):
    import pandas
    pos = 0
    try:
        data = pandas.read_excel(filename, sheet_name = 'Trends')
    except:
        for i in range(2):
            data = pandas.read_excel(filename, header = 0, index_col=i, skiprows=2)
            try:
                data[data.columns[5]]['Dallas']
            except KeyError:
                continue
            else:
                pos = i
                # print(i)
                break
        for i in range(3):
            data = pandas.read_excel(filename, header = 0, index_col=pos, skiprows=i)
            try:
                int(data[data.columns[0]][data.index[0]])
            except ValueError:
                pass
            else:
                break
        return data
    else:
        for i in range(10):
            data = pandas.read_excel(filename, sheet_name = 'Trends', header = i)
            if 'Date' in data.columns:
                return data

def isitcityname(text):
    try:
        t = len(text.split())
    except:
        return False
    else:
        if t != 1:
            return False
        else:
            return True

def data_decode(*data, city = False):
    # print("Decoding data.....")
    try:
        data[0][data[0].columns[0]]['Anderson']
    except:
        date = []
        cum_cases = []
        cum_fat = []
        daily_new_cases = []
        daily_new_fat = []
        for i in range(len(data[0]['Date'])):
            try:
                str(data[0]["Date"][i].date())
            except AttributeError:
                pass
            else:
                date.append(data[0]["Date"][i])
                cum_cases.append(data[0]["Cumulative\nCases"][i])
                cum_fat.append(data[0]["Cumulative\nFatalities"][i])
                daily_new_cases.append(data[0]["Daily\nNew\nCases"][i])
                daily_new_fat.append(data[0]["Daily\nNew\nFatalities"][i])
        # return data_covid(date, cum_cases, cum_fat, daily_new_cases, daily_new_fat)
        return data_covid(name="Texas", \
        cum_cases= classOfdata(name = "Cumulative Cases", data= cum_cases, date = date),\
        cum_fat= classOfdata(name= "Cumulative Fatalities", data= cum_fat, date= date),\
        daily_new_cases= classOfdata(name= "Daily new cases", data= daily_new_cases, date= date),\
        daily_new_fat= classOfdata(name= "Daily new fatalities", data= daily_new_fat, date= date),)
    else:  
        import datetime
        # returndata = []

        # file #0 = cumulative case
        # file #1 = cumulative fatalities
        # file #2 = cumulative tests
        cum_cases = classOfdata(name = "Cumulative cases", date= [], data= [])
        daily_cases = classOfdata(name= "New cases", date= [], data= [])
        cum_fat = classOfdata(name= "Cumulative fatalities", date= [], data= [])
        daily_fat = classOfdata(name= "New fatalities", date= [], data= [])
        daily_tests = classOfdata(name= "New tests", date= [], data= [])
        cum_tests = classOfdata(name= "Cumulative tests", date= [], data= [])
        for current_file in range(len(data)):                                  # per file
            # columns_size = len(data[0].columns)
            for current_row in data[current_file].index:                  # per city
                city_name = current_row
                if isitcityname(city_name):                                    # valid city name
                    pass
                else:
                    continue
                if city:
                    if city_name.lower() != city.lower():
                        continue
                date_list_fromcurrentfile = []
                data_list_fromcurrentfile = []
                for current_column in data[current_file].columns:              # per date
                    try:
                        current_date = getdate(current_column)                 # valid date
                    except ValueError:
                        continue
                    else:
                        if current_date == -1:
                            continue
                        try:
                            idata = int(data[current_file][current_column][current_row])
                        except ValueError:
                            continue
                        else:
                            data_list_fromcurrentfile.append(idata)
                            date_list_fromcurrentfile.append(current_date)
                if current_file == 0:
                    cum_cases.data = data_list_fromcurrentfile
                    cum_cases.date = date_list_fromcurrentfile
                    daily_cases.date = date_list_fromcurrentfile
                    for i in range(len(cum_cases.data)):
                        if i == 0:
                            daily_cases.data.append(cum_cases.data[i])
                        else:
                            daily_cases.data.append(cum_cases.data[i] - cum_cases.data[i-1])
                elif current_file == 1:
                    cum_fat.data = data_list_fromcurrentfile
                    cum_fat.date = date_list_fromcurrentfile
                    daily_fat.date = date_list_fromcurrentfile
                    for i in range(len(cum_fat.data)):
                        if i == 0:
                            daily_fat.data.append(cum_fat.data[i])
                        else:
                            daily_fat.data.append(cum_fat.data[i] - cum_fat.data[i-1])
                elif current_file == 2:
                    cum_tests.data = data_list_fromcurrentfile
                    cum_tests.date = date_list_fromcurrentfile
                    daily_tests.date = date_list_fromcurrentfile
                    for i in range(len(cum_tests.data)):
                        if i == 0:
                            daily_tests.data.append(cum_tests.data[i])
                        else:
                            daily_tests.data.append(cum_tests.data[i] - cum_tests.data[i-1])
        if len(daily_cases.data) == 0:
            return -1
        return data_covid(cum_cases=cum_cases, cum_fat= cum_fat, daily_new_cases= daily_cases, daily_new_fat= daily_fat, cum_tests= cum_tests, new_test= daily_tests, name = city)

def getdate(_input, year = 2020):
    returndata = ()
    i = 0
    try:                                            # catch-all exception case
        _input = str(_input)
    except:
        return returndata
    _range = [n for n in range(len(_input))]
    while i in _range:
        if True:
            try:
                if i == 0:
                    t = int(_input[-2:])
                else:
                    t = int(_input[-2 + (-1*i):-1*i])
            except ValueError:
                try:
                    if i == 0:
                        t = int(_input[-1:])
                    else:
                        t = int(_input[-1 + (-1*i):-1*i])
                except ValueError:
                    i = i + 1
                else:
                    if t > 0:
                        returndata = (t,) + returndata
                        i = i + 1
                    else:
                        i = i + 1
                continue
            else:
                if t > 0:
                    returndata = (t,) + returndata
                    i = i + 2
                    # print(i)
                else:
                    i = i + 1
    if len(returndata) == 2:
        pass
    elif len(returndata) == 1:
        monthlist = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
        monthabbrlist = ["jan", "feb", "mar", "apr", "may", "june", "july", "aug", "sept", "oct", "nov", "dec"]
        word = _input.split()
        for i in range(len(word)):
            try:
                index = monthlist.index(word[i].lower())
            except ValueError:
                try:
                    index = monthabbrlist.index(word[i].lower())
                except ValueError:
                    continue
                else:
                    returndata = (index + 1,) + returndata
                    break
            else:
                returndata = (index + 1,) + returndata
                break
        else:
            return - 1
    else:
        return -1
    from datetime import date
    return date(year = year, month = returndata[0], day = returndata[1])

def takesingleinput(outputint = True):
    from getkey import getkey
    input_ = getkey()
    if outputint == True:
        try:
            input_ = int(input_)
        except ValueError:
            return -1
    return input_

def plot(_data, depth = 0):
    if _data == None:
        input("There has been an error! No such data found!")
        return
    from matplotlib import pyplot
    pyplot.plot(_data.date, _data.data)
    if depth == 0:
        pyplot.suptitle(_data.name)
    else:
        pyplot.suptitle(_data.name + " in past " + str(depth) + " days")
    pyplot.ylabel(_data.name)
    pyplot.show()

def end_menu(data):
    clear()    # import os
    from datetime import date
    inp = menu_function("View total data", "View relative data")
    if inp == 1:            # fixes so that depth of data becomes infinite
        depth = 0
    else:                   # reads the depth of data desired
        while True:
            try:
                depth = int(input("\nEnter the depth of data "))
            except ValueError:
                print("Invalid value\nTry again!")
            else:
                break
    while True:
        clear()
        menu_options = ["View graph of new cases", "View graph of new fatalities", "View graph of cumulative cases", "View graph of cumulative fatalities", "Total cases", "Total fatalities", "New cases in last 24 hours", "New fatalities in last 24 hours", "New cases - 14 days moving average", "Custom moving average", "Go back", "Exit"]
        inp = menu_function(*menu_options)
        from getkey import getkey
        if inp == menu_options.index("View graph of new cases") + 1:
            plot(data.daily_new_cases, depth= depth)
        elif inp == menu_options.index("View graph of new fatalities") + 1:
            plot(data.daily_new_fat, depth = depth)
        elif inp == menu_options.index("View graph of cumulative cases") + 1:
            plot(data.cum_cases, depth = depth)
        elif inp == menu_options.index("View graph of cumulative fatalities") + 1:
            plot(data.cum_fat, depth = depth)
        elif inp == menu_options.index("Total cases") + 1:
            print("Total cases in ", data.name, ": ", data.cum_cases.data[-1], sep= "")
            getkey()
        elif inp == menu_options.index("Total fatalities") + 1:
            print("Total fatalities in ", data.name, ": ",data.cum_fat.data[-1], sep= "")
            getkey()
        elif inp == menu_options.index("New cases in last 24 hours") + 1:
            print("New cases in", data.name, "on", data.daily_new_cases.date[-1].day, ":", int(data.daily_new_cases.data[-1]))
            getkey()
        elif inp == menu_options.index("New fatalities in last 24 hours") + 1:
            print("New fatalities in", data.name, "on", data.daily_new_fat.date[-1].day, ":", int(data.daily_new_fat.data[-1]))
            getkey()
        elif inp == menu_options.index("New cases - 14 days moving average") + 1:
            plot(data.daily_new_cases.average(day_period= 14), depth = depth)
        elif inp == menu_options.index("Custom moving average") + 1:
            clear()
            print("Choose data:")
            custom_data_choice = menu_function("Daily new cases", "Cumulative cases", "Daily new fatalities", "Cumulative new fatalities", "Daily new tests", "Cumulative tests", _clear= False)
            average_width = 14
            while True:
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
                plot(data.daily_new_cases.average(average_width), depth= depth)
            elif custom_data_choice == 2:
                plot(data.cum_cases.average(average_width), depth= depth)
            elif custom_data_choice == 3:
                plot(data.daily_new_fat.average(average_width), depth= depth)
            elif custom_data_choice == 4:
                plot(data.cum_fat.average(average_width), depth= depth)
            elif custom_data_choice == 5:
                if data.name.lower() == "texas":
                    input("This data is not available right now!")
                    continue
                plot(data.new_test.average(average_width), depth= depth)
            elif custom_data_choice == 6:
                if data.name.lower() == "texas":
                    input("This data is not available right now!")
                    continue
                plot(data.cum_test.average(average_width), depth= depth)
        elif inp == menu_options.index("Go back") + 1:
            return True
        elif inp == menu_options.index("Exit") + 1:
            return False
        else:
            clear()
            quit()
        clear()

def menu_city(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county, city = None):
    if city == None:
        while True:
            clear()
            city_name = input("Enter the name of the city: ")
            data_county = data_decode(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county, city= city_name)
            if data_county == -1:
                print("City name not found.")
                print("Press \"Enter\" to exit, any other key to try again")
                t = takesingleinput(False)
                if t == "\n":
                    return
            else:
                break
    else:
        data_county = data_decode(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county, city= city)
    repeat = end_menu(data_county)
    return repeat

def menu(data_texas, xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county):
    clear()
    repeat = 0
    while True:
        t = menu_function("Texas", "Dallas", "Any other city", "Exit")
        if t == 1:
            repeat = end_menu(data_texas)
        elif t == 2:
            repeat = menu_city(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county, city= "Dallas")
        elif t == 3:
            repeat = menu_city(xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county)
        elif t == 4:
            return
        if repeat != True:
            return repeat

def menu_function(*args, takeanyinput = False, _clear = True):
    if _clear:
        clear()
    t = 0
    numberofoptions = len(args)
    if numberofoptions > 9:
        start = 0
        end = 8
        count = 0
        while True:
            if end < numberofoptions - 1:
                response = menu_function(*args[start:end], "More", takeanyinput= takeanyinput)
                if response == 9:
                    start = start + 8
                    end = end + 8
                    count = count + 1
                else:
                    return response + (count*8)
            elif (end + 1) == numberofoptions:
                response = menu_function(*args[start:end + 1], takeanyinput= takeanyinput)
                return response + (count*8)
            else: 
                response = menu_function(*args[start:end], takeanyinput= takeanyinput)
                return response + (count*8)
    else:
        for i in range(numberofoptions):
            print(i + 1, '. ', args[i], sep='')
        if takeanyinput:
            t = takesingleinput(outputint=False)
        else:
            while True:
                t = takesingleinput()
                if (t > 0) and (t <= len(args)):
                    break
        return t

if __name__ == "__main__":
    clear()
    # accessing internet to update the local files
    t = input("Do you want to update the database from the server? ")
    if t in ('y', 'Y', 'Yes', 'yes', 'YES'):
        update_db(general_data_link, general_data_filename)
        update_db(case_data_county_link, case_data_county_filename)
        update_db(fat_data_county_link, fat_data_county_filename)
        update_db(cumulative_tests_data_county_link, cumulative_tests_data_county_filename)
    # reading files into memory
    clear()
    print("Reading files....")
    xceldata_texas = read_db(general_data_filename)
    xceldata_cumulative_case_county = read_db(case_data_county_filename)
    xceldata_cumulative_fat_county = read_db(fat_data_county_filename)
    xceldata_cumulative_tests_county = read_db(cumulative_tests_data_county_filename)
    # decoding and menu calling
    data_texas = data_decode(xceldata_texas)
    del(xceldata_texas)
    menu(data_texas, xceldata_cumulative_case_county, xceldata_cumulative_fat_county, xceldata_cumulative_tests_county)
    clear()
    pass