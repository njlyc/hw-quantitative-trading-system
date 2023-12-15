# data.py
import pyarrow.feather as feather
import pandas as pd


class BacktestDataManager(object):
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """
        Initializes the BacktestDataManager object.

        Args:
            *args (tuple): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        pass
    
    def save(self, filename: str) -> None:
        """
        Saves the data to a Feather file.

        Args:
            filename (str): The name of the file to save the data to.
        """
        feather.write_feather(self.data, filename)

    def load(self, filename: str) -> None:
        """
        Loads the data from a Feather file.

        Args:
            filename (str): The name of the file to load the data from.
        """
        self.data = feather.read_feather(filename)

    def request(self, stk_id: list, date_start: str, date_end: str, columns: list = None) -> pd.DataFrame:
        """
        Requests data for a given stock ID and date range.

        Args:
            stk_id (list): A list of stock IDs to filter the data by.
            date_start (str): The start date of the date range to filter the data by.
            date_end (str): The end date of the date range to filter the data by.
            columns (list, optional): A list of columns to include in the returned DataFrame. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the filtered data.
        """
        if columns is None:
            # If no columns are specified, use all columns
            columns = self.data.columns
        
        # Filter the data by stock ID and date range
        df = self.data.loc[
            (self.data['stk_id'].isin(stk_id)) & 
            (self.data['date'] >= date_start) &
            (self.data['date'] <= date_end),
            columns
        ]

        return df
