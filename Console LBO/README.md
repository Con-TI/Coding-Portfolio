# Summary:
**I/O Console Indonesian LOB simulation (Language: C++, Status: Complete till further updates, Created: June 2024):**
- Motivation: This was my first C++ project. I used this to learn the syntax of C++ and some of its standard libraries.
- Description: This project includes a class for an order book, an exchange agent, and a trading agent. When the compiled exe file is run, it asks for the number of trading agents, the length (time ticks) of each day, and the number of days the simulation runs for. The order book resets at the end of each day, and all pending orders are canceled. The trading agents retain some memory from the previous day in a price vector and start the next day by placing bids or asks based on a distribution and their private "market" signals (n-day SMA based on price vector, bid-ask spread, time ticks between trades, fair value signal from the exchange agent, risk-tolerance (stop loss/take profit), sentiment signal which restarts daily, and noise which increases with decreasing 'intelligence' scores). Multimaps and vectors were heavily used in this project to construct the order book and exchange agent. Other concepts learned and used include C++ classes, enumerations, sets, private and public access specifiers, and control loops in C++ (if, if-else, for, do-while). (Article I read that inspired the various parameters : https://arxiv.org/pdf/2303.00080)
-  *Sidenote:*
*Stocks in the Indonesian stock market have integer ticks that vary depending on the present price.*
*50-200 rupiah stocks have a tick size of 1*
*200-500 rupiah stocks have a tick size of 2*
*500-2000 rupiah stocks have a tick size of 5*
*2000-5000 rupiah stocks have a tick size of 10*
*5000+ rupiah stocks have a tick size of 25*
*I hard-coded these as price bands such that bids and asks sent by trading agents satisfy the above.*

# Instructions:
Run main.exe once compiled
