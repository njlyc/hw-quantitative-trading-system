# trade.py
import pandas as pd
import numpy as np
import pyarrow.feather as feather
from typing import Optional, Dict


class BacktestTradingSystem(object):
    def __init__(self, margin: float = 1e-4, max_position: float = 0.1, cash: float = 1e6) -> None:
        """
        Initializes the BacktestTradingSystem object.

        Args:
            margin (float, optional): The margin to use. Defaults to 1e-4.
            max_position (float, optional): The maximum position to take. Defaults to 0.1.
            cash (float, optional): The amount of cash to start with. Defaults to 1e6.
        """
        self.position = 0
        self.cash = cash
        self.max_position = max_position
        self.margin = margin

    def run(self, data: pd.DataFrame, signal: pd.Series) -> pd.Series:
        """
        Runs the trading system.

        Args:
            data (pd.DataFrame): The data to run the trading system on.
            signal (pd.Series): The signal to use for trading.

        Returns:
            pd.Series: A series containing the results of the trading system.
        """
        res = pd.Series(0, index=data['date'])

        for (idx, info), signal in zip(data.groupby('date'), signal):
            
            price = info['close'].iloc[0]
            asset = self.cash + self.position * price

            if signal > 0:
                delta_position = min(signal, asset * self.max_position / price - self.position)
                self.position += delta_position
                self.cash -= delta_position * price * (1 + self.margin)
                
            elif signal < 0:
                delta_position = min(self.position, -signal)
                self.cash += delta_position * price * (1 + self.margin)
                self.position -= delta_position
            
            res[idx] = self.cash + self.position * price

        return res
    
    def analysis(self, curve: pd.Series, riskless: float = 0.03) -> pd.DataFrame:
        """
        Analyzes the trading system.

        Args:
            curve (pd.Series): The curve to analyze.
            riskless (float, optional): The riskless rate. Defaults to 0.03.

        Returns:
            pd.DataFrame: A DataFrame containing the analysis results.
        """
        ret = (curve.diff() / curve.shift(1)).dropna()
        annual_ret = ret.mean() * 252
        annual_vol = ret.std() * np.sqrt(252)
        
        def max_drawdown(X: pd.Series) -> float:
            """
            Calculates the maximum drawdown.

            Args:
                X (pd.Series): The series to calculate the maximum drawdown for.

            Returns:
                float: The maximum drawdown.
            """
            cummax = np.maximum.accumulate(X)
            drawdown = (cummax - X) / cummax
            return np.max(drawdown)
        
        extra_ret = (annual_ret - riskless)
        sharpe =  extra_ret / annual_vol
        drawdown = max_drawdown(curve)

        return pd.DataFrame({
            "Annual Return": [annual_ret],
            "Extra Return": [extra_ret],
            "Annual Volatility": [annual_vol],
            "Sharpe Ratio": [sharpe],
            "Maximum Drawdown": [drawdown],
        }, index=["Evaluate"],).T
