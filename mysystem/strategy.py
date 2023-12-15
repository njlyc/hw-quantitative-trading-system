# strategy.py
import pandas as pd
import numpy as np


class ReverseStrategy(object):
    def __init__(self, N: int) -> None:
        """
        Initializes the ReverseStrategy object.

        Args:
            N (int): The value of N.
        """
        self.N = N

    def signal(self, data: pd.DataFrame) -> pd.Series:
        """
        Generates a signal based on the given data.

        Args:
            data (pd.DataFrame): The data to generate the signal from.

        Returns:
            pd.Series: A series containing the generated signal.
        """
        price = data['close']
        target = price.rolling(5).mean()
        ret = np.log(target / price)

        return ret.fillna(0.)
    
    
class CrosssectionStrategy(object):
    def __init__(self, baseStrategy: ReverseStrategy) -> None:
        """
        Initializes the CrosssectionStrategy object.

        Args:
            baseStrategy (ReverseStrategy): The base strategy to use.
        """
        self.strategy = baseStrategy

    def signal(self, data: pd.DataFrame) -> pd.Series:
        """
        Generates a signal based on the given data.

        Args:
            data (pd.DataFrame): The data to generate the signal from.

        Returns:
            pd.Series: A series containing the generated signal.
        """
        rets = []
        for (stk_id, data_stk) in data.groupby('stk_id'):
            signal_stk = self.strategy.signal(data_stk).rename(stk_id)
            signal_stk.index = data_stk['date']
            rets.append(signal_stk)
        
        ret = pd.concat(rets, axis=1)

        def normalize(x: pd.DataFrame) -> pd.DataFrame:
            """
            Normalizes the given DataFrame.

            Args:
                x (pd.DataFrame): The DataFrame to normalize.

            Returns:
                pd.DataFrame: The normalized DataFrame.
            """
            return x.subtract(x.mean(axis=1), axis=0).div((x.std(axis=1) + 1e-6), axis=0)

        ret_table = normalize(ret).unstack()

        signal = pd.DataFrame(index=data.set_index(["stk_id", "date"]).index)
        signal["signal"] = ret_table
        return signal.reset_index().set_index(data.index)["signal"]
