from classes import data_covid, classOfdata
from misc import isitcountyname, getdate

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
            except:
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