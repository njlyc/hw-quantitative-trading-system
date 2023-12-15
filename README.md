# Quantitative Trading System

This repository contains three Python files that implement a quantitative trading system:

- `data.py`: Contains the `BacktestDataManager` class, which is responsible for loading and saving data for the trading system.
- `strategy.py`: Contains the `ReverseStrategy` and `CrosssectionStrategy` classes, which implement the trading strategies used by the system.
- `trade.py`: Contains the `BacktestTradingSystem` class, which runs the trading system with given trading signals.

## Usage

To use the trading system, follow these steps:

1. Load your data using the `BacktestDataManager` class.
2. Create an instance of the trading strategy you want to use (`ReverseStrategy` or `CrosssectionStrategy`).
3. Generate trading signals using the `signal` method of the strategy object.
4. Run the trading system using the `BacktestTradingSystem` class with the signals generated in step 3.
5. Analyze the results using the `analysis` method of the `BacktestTradingSystem` object.

## Requirements

The following packages are required to run the trading system:

- pandas
- numpy
- pyarrow

## License

This project is licensed under the MIT License - see the LICENSE file for details.
