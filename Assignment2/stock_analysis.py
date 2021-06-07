"""
    __author__ = Yufeng Liu
    student number = 44443115
    __email__ = yufeng.liu1@uqconnect.edu.au
"""
from stocks import Loader, Analyser, StockCollection, TradingData, AverageVolume


class LoadCSV(Loader):
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
        try:
            for line in file:
                line = line.strip()
                stock_code, date, day_open, day_high, day_low, day_close, volume = line.split(",")
                trading_data = TradingData(date,
                                           float(day_open),
                                           float(day_high),
                                           float(day_low),
                                           float(day_close),
                                           int(volume))
                stock = self._stocks.get_stock(stock_code)
                stock.add_day_data(trading_data)
        except ValueError:
            raise RuntimeError


class LoadTriplet(Loader):
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

        try:
            all_data = file.readlines()
            for i in range(0, len(all_data), 6):
                stock_data = all_data[i: i+6]
                code = stock_data[0].split(":")[0]
                key_dict = {}
                for line in stock_data:
                    _, key, data = line.strip().split(":")
                    key_dict[key] = data

                trading_data = TradingData(key_dict['DA'],
                                           float(key_dict['OP']),
                                           float(key_dict['HI']),
                                           float(key_dict['LO']),
                                           float(key_dict['CL']),
                                           int(key_dict['VO']))
                stock = self._stocks.get_stock(code)
                stock.add_day_data(trading_data)
        except ValueError:
            raise RuntimeError


class HighLow(Analyser):
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
        high = day.get_high()
        low = day.get_low()
        # compare the highest prices for all days with each highest price
        if self._high is None or self._high < high:
            self._high = high
        # compare the lowest prices for all days with each lowest price
        if self._low is None or self._low > low:
            self._low = low

    def reset(self):
        """Reset the analysis process in order to perform a new analysis."""
        self._high = None
        self._low = None

    def result(self):
        """Return the highest and lowest prices paid for a stock.

        Return:
            tuple: the high value and then the low value.
        """
        return self._high, self._low


class MovingAverage(Analyser):
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
        if len(self._close) < self._num_days:  # make amount of the list's element equal to the number of days
            for i in range(self._num_days):
                self._close.append(day.get_close())  # store the processed closing price into the list
        del (self._close[0])
        self._close.append(day.get_close())
        self._sums = sum(self._close)

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


class GapUp(Analyser):
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
        self._trading_data = None

    def process(self, day):
        """Collect the total trading opening price and previous day's closing
           price over a number of days.

        Parameters:
            day (TradingData): Trading data for one stock on one day.
        """
        # today's opening price
        self._open = day.get_open()

        if self._close is not None:
            price_difference = self._open - self._close
            if price_difference > self._delta:
                self._trading_data = day

        # the previous day's closing price
        self._close = day.get_close()

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
        return self._trading_data


def example_usage():
    all_stocks = StockCollection()
    LoadCSV("data_files/march1.csv", all_stocks)
    LoadCSV("data_files/march2.csv", all_stocks)
    LoadCSV("data_files/march3.csv", all_stocks)
    LoadCSV("data_files/march4.csv", all_stocks)
    LoadCSV("data_files/march5.csv", all_stocks)
    LoadTriplet("data_files/feb1.trp", all_stocks)
    LoadTriplet("data_files/feb2.trp", all_stocks)
    LoadTriplet("data_files/feb3.trp", all_stocks)
    LoadTriplet("data_files/feb4.trp", all_stocks)
    volume = AverageVolume()
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


if __name__ == "__main__":
    example_usage()
