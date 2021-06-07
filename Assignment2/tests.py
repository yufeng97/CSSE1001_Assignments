#!/usr/bin/env python3

"""
Supporting tests for the second assignment

Passing these test is NOT a guaruntee the code works. It is up to you to
test and verify that your code works correctly. We will use more tests than
this to mark your assignment and verify functionality. Many cases have been
excluded. 

Usage:
python test.py
OR 
Run through IDLE

Put test.py in the same folder as your assignment solution which must be
called 'stock_analysis.py'.
Ensure there is a folder called 'data_files' which contains the data files
listed below in the TEST_FILES variable.

In the interest of getting this testing code to you ASAP we have skipped some
good coding practices, e.g. detailed comments, magic numbers and accessing 
private variables.
Don't take this as a perfect example of code for this course. 

__author__ = "Roy Portas"
"""
import unittest
import stocks

# The script to test
import stock_analysis as sa

TEST_FILES = {
    'march1.csv': 'data_files/march1.csv',
    'march2.csv': 'data_files/march2.csv',
    'march3.csv': 'data_files/march3.csv',
    'march4.csv': 'data_files/march4.csv',
    'march5.csv': 'data_files/march5.csv',
    'feb1.trp': 'data_files/feb1.trp',
    'feb2.trp': 'data_files/feb2.trp',
    'feb3.trp': 'data_files/feb3.trp',
    'feb4.trp': 'data_files/feb4.trp',
    'march1_small.csv': 'data_files/march1_small.csv',
    'feb1_small.trp': 'data_files/feb1_small.trp'
}
VERSION = 1.0

class LoadTripletSmallTest(unittest.TestCase):
    """ A smaller test example for LoadTriplet where results can be printed
        and analysed manually.
    """
    def setUp(self):
        """ Setup work before each test
        """
        self.all_stocks = stocks.StockCollection()
        sa.LoadTriplet(TEST_FILES['feb1_small.trp'], self.all_stocks)

    def test_LoadCSV(self):
        """ Test only expected stock codes are loaded and that the right number
            of TradingData exist in each stock.
        """
        EXPECTED_STOCKS = ['1AG', 'BNR', 'XNJ']
        loaded_stocks = self.all_stocks._all_stocks

        # Ensure only 3 stocks are loaded
        self.assertEqual(len(loaded_stocks.keys()), 3, 
            "StockCollection does not have 3 stocks in it.")

        for stock_code in loaded_stocks.keys():
            self.assertIn(stock_code, EXPECTED_STOCKS, 
                "Loaded stock codes not correct. Got: " + stock_code)

            # For each stock check it has 3 TradingData
            stock_obj = self.all_stocks.get_stock(stock_code)
            num_td = len(stock_obj._trading_data.keys())
            exp_num = 3
            self.assertEqual(num_td, exp_num, 
                "Stock: {} has {} TadingData, should have {}.".format(
                    stock_code, num_td, exp_num))


class LoadCSVSmallTest(unittest.TestCase):
    """ A smaller test example for LoadCSV where results can be printed
        and analysed manually.
    """
    def setUp(self):
        """ Setup work before each test
        """
        self.all_stocks = stocks.StockCollection()
        sa.LoadCSV(TEST_FILES["march1_small.csv"], self.all_stocks)

    def test_LoadCSV(self):
        """ Test only expected stock codes are loaded and that the right number
            of TradingData exist in each stock.
        """
        EXPECTED_STOCKS = ['1AD', 'BNR', 'MIL']
        loaded_stocks = self.all_stocks._all_stocks

        # Ensure only 3 stocks are loaded
        self.assertEqual(len(loaded_stocks.keys()), 3, 
            "StockCollection does not have 3 stocks in it.")

        for stock_code in loaded_stocks.keys():
            self.assertIn(stock_code, EXPECTED_STOCKS, 
                "Loaded stock codes not correct. Got: " + stock_code)

            # For each stock check it has 5 TradingData
            stock_obj = self.all_stocks.get_stock(stock_code)
            num_td = len(stock_obj._trading_data.keys())
            exp_num = 5
            self.assertEqual(num_td, exp_num, 
                "Stock: {} has {} TadingData, should have {}.".format(
                    stock_code, num_td, exp_num))

    def test_avg_volume(self):
        """ Ensure each 1AD stock has been loaded correctly by calculating 
            volumes
        """
        # This is a given class so should work 'out of the box' once 
        # loading works
        expected_volume = 12665
        volume = stocks.AverageVolume()
        stock = self.all_stocks.get_stock("1AD")
        stock.analyse(volume)
        result = volume.result()
        self.assertEqual(result, expected_volume, 
            "Volume not correct. Got:" + str(result))

class AssignmentSheetExampleTest(unittest.TestCase):
    """ A set of test cases checking the functionality described in the
        assignment task sheet
    """
    def setUp(self):
        """ Setup work before each test
        """
        self.all_stocks = stocks.StockCollection()
        sa.LoadCSV(TEST_FILES["march1.csv"], self.all_stocks)
        sa.LoadCSV(TEST_FILES["march2.csv"], self.all_stocks)
        sa.LoadCSV(TEST_FILES["march3.csv"], self.all_stocks)
        sa.LoadCSV(TEST_FILES["march4.csv"], self.all_stocks)
        sa.LoadCSV(TEST_FILES["march5.csv"], self.all_stocks)
        sa.LoadTriplet(TEST_FILES["feb1.trp"], self.all_stocks)
        sa.LoadTriplet(TEST_FILES["feb2.trp"], self.all_stocks)
        sa.LoadTriplet(TEST_FILES["feb3.trp"], self.all_stocks)
        sa.LoadTriplet(TEST_FILES["feb4.trp"], self.all_stocks)

    def test_avg_volume(self):
        """ Test "Average Volume of ADV is 3629160"
        """
        volume = stocks.AverageVolume()
        stock = self.all_stocks.get_stock("ADV")
        stock.analyse(volume)
        self.assertEqual(volume.result(), 3629160, 
            "Did not get correct value for Average Volume test.")

    def test_high_low(self):
        """ Test "Highest & Lowest trading price of ADV is (0.031, 0.018)"
        """
        high_low = sa.HighLow()
        stock = self.all_stocks.get_stock("ADV")
        stock.analyse(high_low)
        self.assertEqual(high_low.result(), (0.031, 0.018), 
            "Did not get correct value for Highest and Lowest trading price")

    def test_moving_average(self):
        """ Test "Moving average of ADV over last 10 days is 0.02"
        """
        moving_average = sa.MovingAverage(10)
        stock = self.all_stocks.get_stock("ADV")
        stock.analyse(moving_average)
        self.assertEqual("{0:.2f}".format(moving_average.result()), "0.02",
            "Did not get correct value for moving average.")

    def test_gap_up(self):
        """ Test "Last gap up date of YOW is 20170330"
        """
        gap_up = sa.GapUp(0.011)
        stock = self.all_stocks.get_stock("YOW")
        stock.analyse(gap_up)
        self.assertEqual(gap_up.result().get_date(), '20170330')



class LoadCSVTest(unittest.TestCase):
    """ A large scale test suite for the LoadCSV class
    """
    def setUp(self):
        """ Setup work before each test
        """
        self.all_stocks = stocks.StockCollection()

    def test_inheritance(self):
        """ [OOC 3] Demonstrated correct understanding of inheritance
        """
        loadCsv = sa.LoadCSV(TEST_FILES['march1.csv'], self.all_stocks)
        self.assertEqual(loadCsv.__class__.__bases__[0].__name__, 'Loader', 
            'LoadCSV should correctly inherit from Loader')

    def test_process_overriden(self):
        """ [OOC 4] Demonstrated correct understanding of overriding methods
        """
        loadCsv = sa.LoadCSV(TEST_FILES['march1.csv'], self.all_stocks)
        with open(TEST_FILES['march1.csv'], 'r') as f:
            loadCsv._process(f)
        # If it gets here, it hasn't thrown the not implemented exception

    def test_simple_case(self):
        """ Large file test of LoadCSV to ensure the correct number of 
            stocks are loaded
        """
        loadCsv = sa.LoadCSV(TEST_FILES['march1.csv'], self.all_stocks)

        stocks_loaded = self.all_stocks._all_stocks.keys()
        self.assertEqual(len(stocks_loaded), 1910, 
            'LoadCSV should load correct number of stocks')

    def test_invalid_file(self):
        """ Test program raises appropriate exceptions
        """
        with self.assertRaises(RuntimeError):
            # This is an invalid Triplet file and should not work
            sa.LoadCSV('stocks.py', self.all_stocks)



class LoadTripletTest(unittest.TestCase):
    """ Larger file test suite for LoadTriplet class
    """
    def setUp(self):
        """ Setup work before each test
        """
        self.all_stocks = stocks.StockCollection()
        sa.LoadTriplet(TEST_FILES['feb1.trp'], self.all_stocks)

    def test_inheritance(self):
        """ [OOC 3] Demonstrated correct understanding of inheritance
        """
        loadTriplet = sa.LoadTriplet(TEST_FILES['feb1.trp'], self.all_stocks)
        self.assertEqual(loadTriplet.__class__.__bases__[0].__name__, 'Loader', 
            'LoadTriplet should correctly inherit from Loader')

    def test_process_overriden(self):
        """ [OOC 4] Demonstrated correct understanding of overriding methods
        """
        loadTriplet = sa.LoadTriplet(TEST_FILES['feb1.trp'], self.all_stocks)
        with open(TEST_FILES['feb1.trp'], 'r') as f:
            loadTriplet._process(f)
        # If it gets here, it hasn't thrown the not implemented exception

    def test_simple_case(self):
        """ Large file test that LoadTriplet is correct
        """
        loadTriplet = sa.LoadTriplet(TEST_FILES['feb1.trp'], self.all_stocks)
        stocks_loaded = self.all_stocks._all_stocks.keys()

        self.assertEqual(len(stocks_loaded), 1878, 
            'LoadTriplet should load correct number of stocks')

    def test_invalid_file(self):
        """ Test program raises appropriate exceptions
        """
        with self.assertRaises(RuntimeError):
            # This is an invalid Triplet file and should not work
            sa.LoadTriplet('stocks.py', self.all_stocks)

class HighLowTest(unittest.TestCase):
    """ A large file test suite for the HighLow analyser
    """
    def setUp(self):
        """ Setup work before each test
        """
        self.all_stocks = stocks.StockCollection()

    def test_inheritance(self):
        """ [OOC 3] Demonstrated correct understanding of inheritance
        """
        hl = sa.HighLow()
        self.assertEqual(hl.__class__.__bases__[0].__name__, 'Analyser', 
            'HighLow should correctly inherit from Analyser')
    
    def testSimpleResult(self):
        """ Large file test of the HighLow analyser
        """
        # Load a simple training set    
        sa.LoadCSV(TEST_FILES['march1.csv'], self.all_stocks)
        hl = sa.HighLow()

        stock = self.all_stocks.get_stock("ADV")
        stock.analyse(hl)
        
        res = hl.result()
        self.assertEqual(res, (0.025, 0.023),
            'Did not get correct value for the Highest and Lowest price')


class MovingAverageTest(unittest.TestCase):
    """ A large file test suite for the MovingAverage analyser
    """
    def setUp(self):
        """ Setup work before each test
        """
        self.all_stocks = stocks.StockCollection()

    def test_inheritance(self):
        """ [OOC 3] Demonstrated correct understanding of inheritance
        """
        ma = sa.MovingAverage(1)
        self.assertEqual(ma.__class__.__bases__[0].__name__, 'Analyser', 
            'MovingAverage should correctly inherit from Analyser')
    
    def testSimpleResult(self):
        """ Large file test of the MovingAverage analyser
        """
        num_days = 4

        # Load a simple training set    
        sa.LoadCSV(TEST_FILES['march1.csv'], self.all_stocks)
        ma = sa.MovingAverage(num_days)

        stock = self.all_stocks.get_stock("ADV")
        stock.analyse(ma)
        
        res = ma.result()
        self.assertEqual(res, 0.02375, 
            'MovingAverage not correct for stock "ADV" in "march1.csv"')

class GapUpTest(unittest.TestCase):
    """ A large file test suite of the GapUp analyser
    """
    def setUp(self):
        """ Setup work before each test
        """
        self.all_stocks = stocks.StockCollection()

    def test_inheritance(self):
        """ [OOC 3] Demonstrated correct understanding of inheritance
        """
        gu = sa.GapUp(1)
        self.assertEqual(gu.__class__.__bases__[0].__name__, 'Analyser', 
            'GapUp should correctly inherit from Analyser')

    def testSimpleResult(self):
        """ A large file test of the GapUp analysers
        """
        delta = 0.0009

        # Load a simple training set    
        sa.LoadCSV(TEST_FILES['march1.csv'], self.all_stocks)
        gu = sa.GapUp(delta)

        stock = self.all_stocks.get_stock("ADV")
        stock.analyse(gu)
        
        res = gu.result()
        self.assertIsNotNone(res, 'GapUp should return a valid TradingData for stock "ADV" in "march1.csv"')
        self.assertEqual(res.get_date(), '20170228', 'GapUp should return correct result for stock "ADV" in "march1.csv"')

if __name__ == '__main__':
    print("Tests version:", VERSION)
    unittest.main()
