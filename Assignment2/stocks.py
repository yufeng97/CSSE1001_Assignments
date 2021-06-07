"""
    Classes used in the second assignment in CSSE1001.

    StockCollection: All stock market data stored in application.
    Stock: Data for a single stock.
    TradingData: Data for a single day of trading in one stock.
    Loader: Abstract class defining the process of loading stock market data.
    Analyser: Abstract class defining the interface for analysing stock data.
    AverageVolume: Analyse a single stock's data to determine its average volume.
    
    __author__ = "Richard Thomas"
    __email__ = "richard.thomas@uq.edu.au"
"""


class TradingData(object) :
    """Stock market data for a single day of trading for one stock.

        The trading data includes the:
            Date of trading
            Value of opening (first) trade
            Value of highest trade
            Value of lowest trade
            Value of closing (final) trade
            Volume of shares traded
    """
    
    def __init__(self, date, day_open, day_high, day_low, day_close, volume) :
        """
        Parameters:
            date (str): Date in yyyymmdd format.
            day_open (float): Dollar value of the first trade of the day.
            day_high (float): Dollar value of the highest trade of the day.
            day_low  (float): Dollar value of the lowest trade of the day.
            day_close (float): Dollar value of the last trade of the day.
            volume (int): The number of shares traded on this day.
        """
        self._date = date
        self._open = day_open
        self._high = day_high
        self._low = day_low
        self._close = day_close
        self._volume = volume

    def get_date(self) :
        """(str) The date of this day of trading."""
        return self._date

    def set_date(self, date) :
        self._date = date

    def get_open(self) :
        """(float) Value of the opening trade of the day."""
        return self._open

    def set_open(self, day_open) :
        self._open = day_open

    def get_high(self) :
        """(float) Value of highest trade of the day."""
        return self._high

    def set_high(self, day_high) :
        self._high = day_high

    def get_low(self) :
        """(float) Value of lowest trade of the day."""
        return self._low

    def set_low(self, day_low) :
        self._low = day_low

    def get_close(self) :
        """(float) Value of final trade of the day."""
        return self._close

    def set_close(self, day_close) :
        self._close = day_close

    def get_volume(self) :
        """(int) Value of highest trade of the day."""
        return self._volume

    def set_volume(self, volume) :
        self._volume = volume


class Analyser(object) :
    """Abstract class representing any form of stock data analysis."""
    
    def process(self, day) :
        """Abstract method representing collecting and processing DayData.

        Parameters:
            day (TradingData): Trading data for one stock on one day.
        """
        raise NotImplementedError()

    def reset(self) :
        """Reset the analysis process in order to perform a new analysis."""
        raise NotImplementedError()

    def result(self) :
        """Abstract method representing obtaining the result of the analysis.

        Return:
            None: Subclasses will return result of the analysis.
        """
        raise NotImplementedError()


class AverageVolume(Analyser) :
    """Determine the average trading volume for a single stock."""
    
    def __init__(self) :
        self._num_days_analysed = 0
        self._volume = 0
        
    def process(self, day) :
        """Collect the total trading volume over a number of days.

        Parameters:
            day (TradingData): Trading data for one stock on one day.
        """
        self._num_days_analysed += 1
        self._volume += day.get_volume()

    def reset(self) :
        """Reset the analysis process in order to perform a new analysis."""
        self._num_days_analysed = 0
        self._volume = 0

    def result(self) :
        """Return the average trading volume for the processed stock.

        Return:
            int: Average volume of trades across all days processed.
        """
        return self._volume // self._num_days_analysed


class Stock(object) :
    """A single stock listed on the stock market and its trading data."""
    
    def __init__(self, code) :
        """
        Parameters:
            code (str): Stock market code (unique identifier).
        """
        self._code = code
        self._trading_data = {}

    def add_day_data(self, day) :
        """Add one day of trading data to the stock's data.

        Parameters:
            day (TradingData): Trading data for one day.
        """
        # Trading data key is the date stored in the TradingData object
        # and value is the TradingData object.
        self._trading_data[day.get_date()] = day

    def get_day_data(self, date) :
        """Return the trading data for 'date'.

        Parameters:
            date (str): Date in yyyymmdd format of the trading data to retrieve.

        Return:
            TradingData: Trading details for the specified date or None.
        """
        return self._trading_data.get(date)

    def analyse(self, analyser) :
        """Allow any type of analysis to be performed on this stock's
            trading data.

        Data is processed in date order.

        Parameters:
            analyser (Analyser): The object that will perform the analysis.
        """
        sorted_dates = sorted(self._trading_data.keys())
        for date in sorted_dates :
            analyser.process(self._trading_data[date])

    def __str__(self) :
        return self._code


class StockCollection(object) :
    """Provides access to all stock market data."""

    def __init__(self) :
        self._all_stocks = {}

    def get_stock(self, stock_code) :
        """Look up a stock object based on its stock market code.

        Creates a new stock object for 'stock_code' if the object does not
        already exist, otherwise it returns the object mapped to 'stock_code'.

        Parameters:
            stock_code (str): Stock market code used to look up a stock.

        Return:
            Stock: The stock market object represented by this 'stock_code'.
        """
        # '_all_stocks' is a dictionary with 'stock_code' keys,
        # mapped to 'Stock' objects.
        # Either the stock is found in '_all_stocks' or a new 'Stock' object is
        # created if this is the first time this stock code has been loaded.
        self._all_stocks[stock_code] = self._all_stocks.get(stock_code,
                                                            Stock(stock_code))
        return self._all_stocks[stock_code]

    def list_stocks(self) :
        """Simple output of all stocks in the collection."""
        for stock in self._all_stocks.values() :
            print("{0}".format(stock))
        

class Loader(object) :
    """Abstract class defining basic process of loading trading data."""
    
    def __init__(self, filename, stocks) :
        """Data is loaded on object creation.

        Parameters:
            filename (str): Name of the file from which to load data.
            stocks (StockCollection): Collection of existing stock market data
                                      to which the new data will be added.
        """
        # Maintain a reference to the stock colletion into which data is loaded.
        self._stocks = stocks
        with open(filename, "r") as file :
            # Use format specific subclass to parse the data in the file.
            self._process(file)

    def _process(self, file) :
        """Load and parse the stock market data from 'file'."""
        raise NotImplementedError()


if __name__ == "__main__" :
    print("This module provides utility functions for the stock market",
          "analysis program and is not meant to be executed on its own.")
