# Coding-Portfolio
This is my coding portfolio, with projects detailed in my resume and more.

## List of projects and summaries:
- **I/O Console Indonesian LOB simulation in C++ (Language: C++, Status: Complete till further updates, Created: June 2024):**
  - Motivation: This was my first C++ project. I used this to learn the syntax of C++ and some of its standard libraries.
  - Description: This project includes a class for an order book, an exchange agent, and a trading agent. When the compiled exe file is run, it asks the number of trading agents, the length (time ticks) of each day, and the number of days the simulation runs for. The order book resets at the end of each day, and all pending orders are canceled. The trading agents retain some memory from the previous day in a price vector and start the next day by placing bids or asks based on a distribution and their private "market" signals (n-day SMA based on price vector, bid-ask spread, time ticks between trades, fair value signal from the exchange agent, risk-tolerance (stop loss/take profit), sentiment signal which restarts daily, and noise which increases with decreasing 'intelligence' scores). Multimaps and vectors were heavily used in this project to construct the order book and exchange agent. Other concepts learned and used include C++ classes, enumerations, sets, private and public access specifiers, and control loops in C++ (if, if-else, for, do-while).
  - *Sidenote:*
*Stocks in the Indonesian stock market have integer ticks that vary depending on the present price.*
*50-200 rupiah stocks have a tick size of 1*
*200-500 rupiah stocks have a tick size of 2*
*500-2000 rupiah stocks have a tick size of 5*
*2000-5000 rupiah stocks have a tick size of 10*
*5000+ rupiah stocks have a tick size of 25*
*I hard-coded these as price bands such that bids and asks sent by trading agents satisfy the above.*

- **Tkinter backtesting application (Language: Python, Status: Ongoing, Created: July/August 2024)**
  - Motivation: After learning how to backtest strategies with Python pandas, I decided to make an application to make it easier to test out new ideas using a pre-downloaded dataset of the price data of all --Indonesian stocks rather than creating a new file for every idea and backtest I want to do.
  - Description: This is a project aimed at making an application for creating custom indicators, backtesting them, and displaying them visually. Libraries used include but are not limited to tkinter, matplotlib, numpy, pykalman, pandas, seaborn, and tkcalendar. The backtesting tab allows the user to select the frequency of price data displayed (1d, 5d, etc.) and the type of chart displayed (regular line chart, kagi, renko, etc.). The indicator tab allows the user to construct indicators using custom syntax to combine technical indicators and data transformations. The price data used is obtained from yfinance and non-price data, such as interest rates, via web scraping using selenium, all stored in a separate folder called "datastore" that was not committed to this repo due to space constraints.
  - *Sidenote:*
*Future features I intend to add are tabs for backtesting against all stocks in various ways (including backtesting against theoretical asian call warrant prices, backtesting against every stock individually displayed on one chart, and backtesting a portfolio allocation strategy based on some alpha), an options tab that shows payoff diagrams of options combos, formulas for the fair price of each kind of option, and a random walk backtesting tab.* 
