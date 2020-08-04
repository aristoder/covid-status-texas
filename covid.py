general_data_link = "https://www.dshs.state.tx.us/coronavirus/TexasCOVID19CaseCountData.xlsx"
general_data_filename = "general_data.xlsx"
case_data_county_link = "https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyCaseCountData.xlsx"
case_data_county_filename = "case_data_county.xlsx"
fat_data_county_link = "https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx"
fat_data_county_filename = "fat_data_county.xlsx"
cumulative_tests_data_county_link = "https://dshs.texas.gov/coronavirus/TexasCOVID-19CumulativeTestsOverTimebyCounty.xlsx"
cumulative_tests_data_county_filename = "cumulative_tests_data_county.xlsx"

from filemanagment import update_db, read_db, data_decode
from menufunctions import menu
from misc import clear, responseYes, installThisModule

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