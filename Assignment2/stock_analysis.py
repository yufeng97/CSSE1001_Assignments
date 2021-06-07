"""
    
    __author__ = Yufeng Liu
    student number = 44443115
    __email__ = yufeng.liu1@uqconnect.edu.au
"""

import stocks

class LoadCSV(stocks.Loader):
    """Loads stock market data from files that are in a comma-separate format """

    def __init__(self, filename, stocks):
        """

        Parameters:
            filename(str): Name of the file from which to load data.
            stocks (StockCollection): Collection of existing stock market data
                                      to which the new data will be added.
        """
        super().__init__(filename, stocks)
            
    def _process(self, file):
        """Iterate through the file, extracting the data from a line"""        
        stocks_list = [] #the list is used to store the processed data
        try:
            for line in file:
                line = line.strip()#remove the space
                stocks_list = line.split(",") #remove the comma and store the data into the list              
                trading_data = stocks.TradingData(stocks_list[1],
                                                  float(stocks_list[2]),
                                                  float(stocks_list[3]),
                                                  float(stocks_list[4]),
                                                  float(stocks_list[5]),
                                                  int(stocks_list[6]))
                single_stock = self._stocks.get_stock(stocks_list[0])
                single_stock.add_day_data(trading_data)                         

        except IndexError:
            raise RuntimeError        

class HighLow(stocks.Analyser):
    """Determines the highest and lowest prices paid for a stock across all
       of the data stored for the stock."""
    
    def __init__(self):
        self._high = None
        self._low = None

    def process(self, day):
        """Collect the total trading the highest and lowest prices over a
           number of days.

        Parameters:
            day (TradingData): Trading data for one stock on one day.
        """
        try:
            high = day.get_high()
            low = day.get_low()
            if self._high == None or self._high < high:#compare the highest prices for all days with every's highest price
                self._high = high
            if self._low == None or self._low > low:#compare the lowest prices for all days with every's lowest price
                self._low = low
        except:
            raise ValueError

    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        self._high = None
        self._low = None    

    def result(self):
        """Return the highest and lowest prices paid for a stock.

        Return:
            tuple: the high value and then the low value.
        """
        return (self._high, self._low) 

class MovingAverage(stocks.Analyser):
    """Calculates the average closing price of a stock over a specified period
       of time """
    
    def __init__(self, num_days):
        """

        Parameter:
            num_days(int): The number of days over which to calculate the
                           average.
        """
        self._num_days = num_days
        self._close = []
        self._sums = 0
        
    def process(self, day):
        """Collect the total trading closing price over a number of days.

        Parameters:
            day (TradingData): Trading data for one stock on one day.
        """
        try:
            if len(self._close) < self._num_days:#make amount of the list's element equal to the number of days
                for i in range(self._num_days):
                    self._close.append(day.get_close())#store the processed closing price into the list
            del(self._close[0])
            self._close.append(day.get_close())        
            self._sums = sum(self._close)
        except:
            raise ValueError
        
    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        self._num_days = None
        self._close = None
        self._sums = 0

    def result(self):
        """Return the average closing price over the last num_days for the
           processed stock.

        Return:
            float: Average closing price of processed stock over the last
                   num_days. """
        return self._sums / self._num_days    

class GapUp(stocks.Analyser):
    """Finds the most recent day in the trading data where the stock’s opening
       price was significantly higher than its previous day’s closing price."""

    def __init__(self, delta):
        """

        Parameter:
            delta(float): A value which is used to determine whether the price
                          difference is significant or not.
        """
        self._delta = delta
        self._open = None
        self._close = None
        self._tradingdata = None 

    def process(self, day):
        """Collect the total trading opening price and previous day's closing
           price over a number of days.

        Parameters:
            day (TradingData): Trading data for one stock on one day.
        """
        try:
            self._open = day.get_open()#today's opening price
            
            if self._close != None:
                price_difference = self._open - self._close
                if price_difference > self._delta:
                    self._tradingdata = day#store the trading data for a specific day

            self._close = day.get_close()#the previous day's closing price
        except:
            raise ValueError

    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        self._open = None
        self._close = None
        self._delta = None

    def result(self):
        """Return the TradingData object which is found by GapUp class.

        Return:
            day(TradingData): the specific day's Trading data.
        """
        return self._tradingdata

class LoadTriplet(stocks.Loader):
    """Loads stock market data from files that are in a triplet key-coded format """

    def __init__(self, filename, stocks):
        """
        Parameters:
            filename(str): Name of the file from which to load data.
            stocks (StockCollection): Collection of existing stock market data
                                      to which the new data will be added.

        """
        super().__init__(filename, stocks)

    def _process(self, file):
        """Iterate through the file, extracting the data from a line"""        

        stocks_list = []
        try:
            for line in file:
                line = line.strip() #remove the space
                stocks_list = line.split(":") #remove colon and store the data as the list
                code = stocks_list[0]
                if stocks_list[1] == "DA":
                    DA = stocks_list[2]
                elif stocks_list[1] == "OP":
                    OP = stocks_list[2]
                elif stocks_list[1] == "HI":
                    HI = stocks_list[2]
                elif stocks_list[1] == "LO":
                    LO = stocks_list[2]
                elif stocks_list[1] == "CL":
                    CL = stocks_list[2]
                elif stocks_list[1] == "VO":
                    VO = stocks_list[2]
                    trading_data = stocks.TradingData(DA, float(OP), float(HI), float(LO), float(CL), int(VO))
                    single_stock = self._stocks.get_stock(code)
                    single_stock.add_day_data(trading_data)
                     
        except IndexError:
            raise RuntimeError
        

def example_usage () :
    all_stocks = stocks.StockCollection()
    LoadCSV("march1.csv", all_stocks)
    LoadCSV("march2.csv", all_stocks)
    LoadCSV("march3.csv", all_stocks)
    LoadCSV("march4.csv", all_stocks)
    LoadCSV("march5.csv", all_stocks)
    LoadTriplet("feb1.trp", all_stocks)
    LoadTriplet("feb2.trp", all_stocks)
    LoadTriplet("feb3.trp", all_stocks)
    LoadTriplet("feb4.trp", all_stocks)
    volume = stocks.AverageVolume()
    stock = all_stocks.get_stock("ADV")
    stock.analyse(volume)
    print("Average Volume of ADV is", volume.result())
    high_low = HighLow()
    stock.analyse(high_low)
    print("Highest & Lowest trading price of ADV is", high_low.result())
    moving_average = MovingAverage(10)
    stock.analyse(moving_average)
    print("Moving average of ADV over last 10 days is {0:.2f}"
          .format(moving_average.result()))
    gap_up = GapUp(0.011)
    stock = all_stocks.get_stock("YOW")
    stock.analyse(gap_up)
    print("Last gap up date of YOW is", gap_up.result().get_date())


if __name__ == "__main__" :
    example_usage()
