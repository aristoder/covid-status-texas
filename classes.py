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
        length = len(self.data)
        for i in range(length):
            if i < int((day_period + 1)/2):         # if index error from beginning portion of the lsit
                data.append(sum(self.data[:i + int((day_period-1)/2)])/(i + int((day_period-1)/2)))
            elif i <= length - int(day_period/2):   # if no index error issue
                data.append(sum(self.data[i - int((day_period + 1)/2) : i + int((day_period-1)/2)])/day_period)
            else:                                   # if index error from end of the lsit
                data.append(sum(self.data[i - int((day_period + 1)/2):])/(length - i + int((day_period+1)/2)))
        return classOfdata(date= self.date, data= data, name= self.name)