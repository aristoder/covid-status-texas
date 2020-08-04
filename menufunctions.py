from misc import clear, plot, returnlastvaliddata, date_relation, takesingleinput
from filemanagment import data_decode
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