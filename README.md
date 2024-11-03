# Coding-Portfolio
This is my coding portfolio. Click on the folders to check the more detailed README descriptions for each one.

## List of projects and summaries:
- **I/O Console Indonesian LOB simulation (Language: C++, Status: Complete till further updates, Created: June 2024):**
  - This was my first C++ project. I used this to learn the syntax of C++ and some of its standard libraries. It is an Indonesian limit order book simulation (Indonesian because of the integer ticks) that displays on the terminal console as an ascii table.

- **Tkinter backtesting application (Language: Python, Status: Ongoing, Created: July/August 2024)**
  - Motivation: After learning how to backtest strategies with Python pandas, I decided to make an application to make it easier to test out new ideas using a pre-downloaded dataset of the price data of all --Indonesian stocks rather than creating a new file for every idea and backtest I want to do.
  - Description: This is a project aimed at making an application for creating custom indicators, backtesting them, and displaying them visually. Libraries used include but are not limited to tkinter (treeviews, comboboxes, notebook, button, canvas), matplotlib, numpy, pykalman, pandas, seaborn, and tkcalendar. The backtesting tab allows the user to select the frequency of price data displayed (1d, 5d, etc.) and the type of chart displayed (regular line chart, kagi, renko, etc.). The indicator tab allows the user to construct indicators using custom syntax to combine technical indicators and data transformations. The price data used is obtained from yfinance and non-price data, such as interest rates, via web scraping using selenium, all stored in a separate folder called "datastore" that was not committed to this repo due to space constraints. 
  - Future updates:
Future features I intend to add are tabs for backtesting against all stocks in various ways (including backtesting against theoretical asian call warrant prices, backtesting against every stock individually displayed on one chart, and backtesting a portfolio allocation strategy based on some alpha), an options tab that shows payoff diagrams of options combos, formulas for the fair price of each kind of option, and a random walk backtesting tab.

- **JaneStreet Puzzles**
  - A folder containing my solutions to Jane Street's monthly puzzles. Solved so far: October 2024 (Conrad Trey Indradjaja)

- **Kaggle Folder**
  - A folder containing my kaggle competition attempts. Kaggle competitions so far: RSNA 2024 MRI Classification



 
