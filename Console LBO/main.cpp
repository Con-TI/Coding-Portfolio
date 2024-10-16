#include <iostream>
#include <cstdlib>
#include <cmath>
#include <string>
#include <set>
#include <vector>
#include <map>
#include <numeric>
#include <algorithm>
#include <iomanip>
#include <iterator>
#include <chrono>
#include <time.h>
#include "include/color.hpp"
#include <random>
#include <thread>
#include <windows.h>

using namespace std;

enum class OrderType { BUY , SELL };
enum class FillType { FILLED , PARTIAL };
enum class TraderStatus { ORDERING , IDLE };

class OrderBook; class Trader; class ExchangeAgent;

multimap<int, int> priceBands = {{0, 50}, {1, 200}, {2, 500}, {3, 2000}, {4, 5000}};
multimap<int, int> priceIncrements = {{0, 1}, {1, 2}, {2, 5}, {3, 10}, {4, 25}};

int checkPriceBand(double price) {
    if (price > 5000) return 4;
    if (price > 2000) return 3;
    if (price > 500) return 2;
    if (price > 200) return 1;
    return 0;
}

struct Order {
    int stockId;
    int traderId;
    double price;
    int quantity;
    OrderType type;

    Order(int sI,int tI, double p, double q, OrderType t) : stockId(sI), traderId(tI), price(p), quantity(q), type(t) {}
};

class OrderBook{
private:
    multimap<double, multimap<int,vector<int>>> buyOrders;
    multimap<double, multimap<int,vector<int>>> sellOrders;

    vector<double> findIntersectingPrices(){
        set<double> buyPrices, sellPrices;
        for (const auto& elem : buyOrders) {
            buyPrices.insert(elem.first);
        }
        for (const auto& elem : sellOrders) {
            sellPrices.insert(elem.first);
        }
        vector<double> overlappingPrices;
        set_intersection(buyPrices.begin(),buyPrices.end(),sellPrices.begin(),sellPrices.end(),back_inserter(overlappingPrices));
        return overlappingPrices;
    };

public:

    void addOrder(const Order& order, const int& time){
        vector<int> vec = {order.quantity, order.traderId};
        if (order.type == OrderType::BUY){
            auto i = buyOrders.find(order.price);
            if (i!=buyOrders.end()){
                multimap<int,vector<int>> timeList = i -> second;
                timeList.insert(make_pair(time, vec));
                i -> second = timeList;
            }
            else{
                multimap<int,vector<int>> timeList;
                timeList.insert(make_pair(time, vec));
                buyOrders.insert(make_pair(order.price,timeList));
            }
        }
        else{
            auto i = sellOrders.find(order.price);
            if (i!=sellOrders.end()){
                multimap<int,vector<int>> timeList = i -> second;
                timeList.insert(make_pair(time, vec));
                i -> second = timeList;
            }
            else{
                multimap<int,vector<int>> timeList;
                timeList.insert(make_pair(time, vec));
                sellOrders.insert(make_pair(order.price,timeList));
            }
        }
    };

    multimap<FillType,pair<double,multimap<OrderType,vector<int>>>> matchOrders(){
        multimap<FillType,pair<double,multimap<OrderType,vector<int>>>> response;
        int buyTime; int buyerID; int sellTime; int sellerID; int quantityBuy; int quantitySell;
        multimap<OrderType,vector<int>> filledOrders; vector<int> filledOrder;
        multimap<OrderType,vector<int>> partialOrders; vector<int> partialOrder;
    
        vector<double> overlappingPrices = findIntersectingPrices();
        for (const double& price: overlappingPrices){
            int q;
            auto i = buyOrders.find(price); 
            auto j = sellOrders.find(price);
            multimap<int,vector<int>> buyTimeList = i -> second; 
            multimap<int,vector<int>> sellTimeList = j -> second;
            
            for (auto k = buyTimeList.begin(); k  != buyTimeList.end();){
                vector<int> bvec = k -> second;
                quantityBuy = bvec[0]; buyerID = bvec[1]; buyTime = k->first;

                for (auto w = sellTimeList.begin(); w != sellTimeList.end();){
                    vector<int> svec = w -> second;
                    quantitySell = svec[0]; sellerID = svec[1]; sellTime = w->first;

                    q = quantitySell - quantityBuy;
                    if (q<0){
                        w = sellTimeList.erase(w);
                        filledOrder = {sellTime, sellerID, quantitySell};
                        filledOrders.insert(make_pair(OrderType::SELL,filledOrder));

                        quantityBuy = abs(q);
                        ;
                    }
                    else if(q>0){
                        k = buyTimeList.erase(k);
                        filledOrder = {buyTime, buyerID, quantityBuy};
                        filledOrders.insert(make_pair(OrderType::BUY,filledOrder));

                        quantitySell = q;
                        svec = {quantitySell,sellerID};
                        w -> second = svec;
                        partialOrder = {sellTime, sellerID, quantitySell};
                        partialOrders.insert(make_pair(OrderType::SELL,partialOrder));
                        break;
                    }
                    else{
                        k = buyTimeList.erase(k);
                        filledOrder = {buyTime, buyerID, quantityBuy};
                        filledOrders.insert(make_pair(OrderType::BUY,filledOrder));

                        w = sellTimeList.erase(w);
                        filledOrder = {sellTime, sellerID, quantitySell};
                        filledOrders.insert(make_pair(OrderType::SELL,filledOrder));
                        break;
                    }
                }
                if (q<0){
                    quantityBuy = abs(q);
                    bvec = {quantityBuy,buyerID};
                    k -> second = bvec;
                    partialOrder = {buyTime, buyerID, quantityBuy};
                    partialOrders.insert(make_pair(OrderType::BUY,partialOrder));
                    break;
                }
                else if(q==0 && sellTimeList.empty()){
                        break;
                }
            }
            if (buyTimeList.empty()){
                i = buyOrders.erase(i);
            }
            else{
                i->second = buyTimeList;
            }
            if (sellTimeList.empty()){
                j = sellOrders.erase(j);
            }
            else{
                j->second = sellTimeList;
            }
            response.insert(make_pair(FillType::FILLED,make_pair(price,filledOrders)));
            response.insert(make_pair(FillType::PARTIAL,make_pair(price,partialOrders)));
        }
        return response;
    };

    multimap<OrderType,pair<double,int>> compressBook(){
        multimap<OrderType,pair<double,int>> neatBook;
        pair<double,int> priceQuantitypair;
        for (auto i = buyOrders.begin(); i!=buyOrders.end();++i){
            double priceBuy = i->first;
            int quantityBuy = 0;
            multimap<int,vector<int>> buyTimeList = i->second;
            for (auto j = buyTimeList.begin(); j!= buyTimeList.end();++j){
                vector<int> bvec = j->second;
                int qB = bvec[0]; 
                quantityBuy += qB;
            }
            priceQuantitypair = {priceBuy,quantityBuy};
            neatBook.insert(make_pair(OrderType::BUY,priceQuantitypair));
        }
        for (auto i = sellOrders.begin(); i!=sellOrders.end();++i){
            double priceSell = i->first;
            int quantitySell = 0;
            multimap<int,vector<int>> sellTimeList = i->second;
            for (auto j = sellTimeList.begin(); j!= sellTimeList.end();++j){
                vector<int> svec = j->second;
                int qS = svec[0]; 
                quantitySell += qS;
            }
            priceQuantitypair = {priceSell,quantitySell};
            neatBook.insert(make_pair(OrderType::SELL,priceQuantitypair));
        }
        return neatBook;
    };

    void resetBook(){
        buyOrders.clear();
        sellOrders.clear();
    };

};

class ExchangeAgent{
private:
    OrderBook Book;
    int stockId;
    multimap<OrderType,pair<double,int>> neatBook;
    int startingPriceBand;
    int minPrice;
    int maxPrice;
    int increment;
    double startingPrice;
    int shares;
    double baseFundamentalValue;
    double midPrice;
    double bidAskSpread;
    double lowestAsk;
    double highestBid;

public:
    ExchangeAgent(int id){
        stockId = id;
        startingPriceBand = rand()%4;
        minPrice = 50 + (priceBands.find(startingPriceBand) -> second);
        maxPrice = priceBands.find(startingPriceBand+1) -> second;
        increment = priceIncrements.find(startingPriceBand) -> second;
        startingPrice = minPrice + (rand() % ((maxPrice-minPrice)/increment))*increment;
        shares = rand()%4990000 + 10000;
        baseFundamentalValue = startingPrice + ((rand()%2)*2-1)*increment*10;
        midPrice = startingPrice;
        bidAskSpread = 0;
        lowestAsk = startingPrice;
        highestBid = startingPrice;
    };

    double bASpread(){
        return bidAskSpread;
    }

    double baseFundamentalVal(){
        return baseFundamentalValue;
    }

    double highBid(){
        return highestBid;
    }

    double lowAsk(){
        return lowestAsk;
    }

    double midP(){
        return midPrice;
    }

    void updatefundamentalValue(){
        int band = checkPriceBand(midPrice);
        increment = priceIncrements.find(band)->second;
        if (baseFundamentalValue > 10){
            double change = ((rand()%2)*2-1)*(rand()%3)*increment;
            baseFundamentalValue += change;
        }
        else{
            double change = rand()%3*increment;
            baseFundamentalValue += change;
        }
    }

    multimap<int,Order> initialDistributionOfStocks(const vector<int>& traderIds){
        multimap<int,Order> toSend;
        int totalNum = 1000;
        for (int i = 0; i!=9; ++i){
            totalNum+=1000*(rand()%2);
        }
        int storeNum = totalNum;
        int relative;
        while (storeNum!=0){
            for (size_t i = 0;i<traderIds.size();++i){
                int traderId = traderIds[i];
                int divisor = rand()%10 + 4;
                relative = storeNum%divisor;
                storeNum -= relative;
                int traderShare= (shares * relative)/totalNum;
                Order order(stockId,-1,startingPrice,traderShare,OrderType::BUY);
                toSend.insert(make_pair(traderId,order));
            }
        }
        return toSend;
    };

    void traderToExchangeLimit(const Order& order, const int& time){
        Book.addOrder(order, time);
    };

    void endDay(){
        Book.resetBook();
        baseFundamentalValue = midPrice;
    }

    multimap<int,Order> compileBook(){
        multimap<FillType,pair<double,multimap<OrderType,vector<int>>>> response = Book.matchOrders();
        neatBook = Book.compressBook();
        multimap<int,Order> responseL;
        for (auto i = response.begin();i!=response.end();++i){
            FillType filltype = i->first;
            double price = (i->second).first;
            multimap<OrderType,vector<int>> orders = (i->second).second;
            for (auto j = orders.begin();j!=orders.end();++j){
                OrderType type = j->first;
                vector<int> vec = j->second;
                int traderId = vec[1];
                int quantity = vec[2];
                Order order(stockId,-1,price,-quantity,type);
                responseL.insert(make_pair(traderId,order));
            }
        }
        return responseL;
    };

    void displayBook(int& counterLength){
        cout<<endl;
        cout<<endl;
        cout<<"Stock ID: "<<stockId<<endl;
        cout<<endl;
        cout<<" |     Quantity     |    "<<dye::red("Bid")<<"    |    "<<dye::green("Ask")<<"    |     Quantity     | "<<endl;
        cout<<" ";
        for (int i=0;i<63;++i){
            cout<<"-";
        }
        cout<<" "<<endl;

        multimap<double,int, greater<double>> Bids;
        multimap<double,int> Asks;
        auto buy_range = neatBook.equal_range(OrderType::BUY);
        auto sell_range = neatBook.equal_range(OrderType::SELL);
        int counterB = 0;
        for (auto i = buy_range.first; ((i!=buy_range.second) && (counterB<counterLength)); ++i){
            Bids.insert(i -> second);
            ++counterB;
        }
        int counterA = 0;
        for (auto i = sell_range.first; ((i!=sell_range.second) && (counterA<counterLength)); ++i){
            Asks.insert(i -> second);
            ++counterA;
        }

        auto bidI = Bids.begin();
        auto askI = Asks.begin();
        int even;
        int space;
        while (bidI != Bids.end() || askI != Asks.end()){
            if (bidI != Bids.end()){
                cout<< " |";
                int qDigits = floor(log10(bidI->second)+1);
                // cout<<float(bidI->second);
                even = qDigits %2 ;
                if (even == 0){
                    space = (19-1-qDigits)/2;
                }
                else{
                    space = (19-qDigits)/2;
                }
                for (int i=0;i<(18-space-qDigits);++i){
                    cout<<" ";
                }
                cout<<(bidI -> second);
                for (int i=0;i<space;++i){
                    cout<<" ";
                }
                cout<<"|";

                int pDigits = floor(log10(bidI->first)+1);
                even = pDigits % 2;
                if (even == 0){
                    space = (12-pDigits)/2;
                }
                else{
                    space = (12-1-pDigits)/2;
                }
                for (int i=0;i<(11-space-pDigits);++i){
                    cout<<" ";
                }
                cout<<dye::red(bidI -> first);
                for (int i=0;i<space;++i){
                    cout<<" ";
                }

                ++bidI;
            }
            else{
                cout<<" |";
                cout<<setw(19)<<"|"<<setw(12);
            }

            cout<<"|";

            if (askI != Asks.end()){
                int pDigits = floor(log10(askI->first)+1);
                even = pDigits % 2;
                if (even == 0){
                    space = (12-pDigits)/2;
                }
                else{
                    space = (12-1-pDigits)/2;
                }
                for (int i=0;i<(11-space-pDigits);++i){
                    cout<<" ";
                }
                cout<<dye::green(askI -> first);
                for (int i=0;i<space;++i){
                    cout<<" ";
                }
                cout<<"|";

                int qDigits = floor(log10(askI->second)+1);
                even = qDigits %2 ;
                if (even == 0){
                    space = (19-1-qDigits)/2;
                }
                else{
                    space = (19-qDigits)/2;
                }
                for (int i=0;i<(18-space-qDigits);++i){
                    cout<<" ";
                }
                cout<<askI -> second;
                for (int i=0;i<space;++i){
                    cout<<" ";
                }
                cout<<"| "<<endl;
                ++askI;
            }
            else{
                cout<<setw(12)<<"|"<<setw(20);
                cout<<"| "<<endl;
            }
        }
        if (counterA<counterLength && counterB<counterLength){
            int emptyRows;
            if ((counterLength-counterA) > (counterLength-counterB)){
                emptyRows = counterLength-counterB;
            }
            else{
                emptyRows = counterLength-counterA;
            }
            for (int i = 0; i<emptyRows;++i){
                cout<<" |"<<setw(19)<<"|"<<setw(12)<<"|"<<setw(12)<<"|"<<setw(20)<<"| "<<endl;
            }
            cout<<endl<<endl;
        }
        else{
            cout<<" |"<<setw(19)<<"|"<<setw(12)<<"|"<<setw(12)<<"|"<<setw(20)<<"| "<<endl;
            cout<<endl<<endl;
        }

        bidI = Bids.begin();
        askI = Asks.begin();
        if (askI!=Asks.end()){
            lowestAsk = askI->first;
        }
        else{
            increment = priceIncrements.find(checkPriceBand(bidI->first))->second;
            lowestAsk = bidI->first + increment*5;
        }
        if (bidI!=Bids.end()){
            highestBid = bidI->first;            
        }
        else{
            increment = priceIncrements.find(checkPriceBand(askI->first))->second;
            highestBid = askI->first - increment*5;
        }
        if (askI==Asks.end() && bidI ==Bids.end()){
            if (midPrice<5000){
                double start = priceBands.find(checkPriceBand(midPrice))->second;
                double end = priceBands.find(checkPriceBand(midPrice)+1)->second;
                increment = priceIncrements.find(checkPriceBand(midPrice))->second;
                int num = (end-start/increment);
                for (int i=0; i<num; ++i){
                    highestBid = start + i*increment;
                    lowestAsk = start + (i+1)*increment;
                    if (highestBid<midPrice<lowestAsk){
                       break; 
                    }
                }
            }
            else{
                double start = 5000;
                double end = 100000;
                increment = priceIncrements.find(checkPriceBand(midPrice))->second;
                int num = (end-start/increment);          
                for (int i=0; i<num; ++i){
                    highestBid = start + i*increment;
                    lowestAsk = start + (i+1)*increment;
                    if (highestBid<midPrice<lowestAsk){
                       break; 
                    }
                }
            }
        }

        double midprice = round((((highestBid) + (lowestAsk)))/2*100)/100;
        double BAspread = round((((lowestAsk)-(highestBid))/(highestBid)*100)*100)/100;
        midPrice = midprice;
        bidAskSpread = BAspread;
        cout<<"Highest Bid: "<<dye::red(highestBid)<<endl;
        cout<<"Lowest Ask: "<<dye::green(lowestAsk)<<endl;
        cout<<"Mid Price: "<<midprice<<endl;
        cout<<"Bid Ask Spread: "<<BAspread<<endl;
    };
};

class Trader{
private:
    int traderId;
    
    int intelligence;
    int trender;
    multimap<int,vector<double>> midPriceMemory;
    int smaLength;
    int hft;
    int meanReversion;
    double tradeFreq;
    int riskTolerance;

    multimap<int,multimap<double,int>> holdings;
    int money;
    multimap<int,multimap<double,int>> pendingBuyOrders;
    multimap<int,multimap<double,int>> pendingSellOrders;

    multimap<int,ExchangeAgent>* stocksPtr;
    multimap<int,double> sentiments;

    TraderStatus status = TraderStatus::ORDERING;
    int timeTillNextTrade = 0;

    void addPendingBuyOrder(const Order& order){
        int stockId = order.stockId;
        double orderPrice = order.price;
        int orderQuantity = order.quantity;
        if (pendingBuyOrders.find(stockId)!=pendingBuyOrders.end()){
            multimap<double,int>& priceQuantityPairs = pendingBuyOrders.find(stockId) -> second;
            if (priceQuantityPairs.find(orderPrice)!=priceQuantityPairs.end()){
                int& existingQuantity = priceQuantityPairs.find(orderPrice)->second;
                existingQuantity += orderQuantity;
            }
            else{
                priceQuantityPairs.insert(make_pair(orderPrice,orderQuantity));
            }
        }
        else{
            multimap<double,int> priceQuantityPairs;
            priceQuantityPairs.insert(make_pair(orderPrice,orderQuantity));
            pendingBuyOrders.insert(make_pair(stockId,priceQuantityPairs));
        }
    };

    void addPendingSellOrder(const Order& order){
        int stockId = order.stockId;
        double orderPrice = order.price;
        int orderQuantity = order.quantity;
        if (pendingSellOrders.find(stockId)!=pendingSellOrders.end()){
            multimap<double,int>& priceQuantityPairs = pendingSellOrders.find(stockId) -> second;
            if (priceQuantityPairs.find(orderPrice)!=priceQuantityPairs.end()){
                int& existingQuantity = priceQuantityPairs.find(orderPrice)->second;
                existingQuantity += orderQuantity;
            }
            else{
                priceQuantityPairs.insert(make_pair(orderPrice,orderQuantity));
            }
        }
        else{
            multimap<double,int> priceQuantityPairs;
            priceQuantityPairs.insert(make_pair(orderPrice,orderQuantity));
            pendingSellOrders.insert(make_pair(stockId,priceQuantityPairs));
        }
    };

    void resetTimer(){
        random_device rd;
        mt19937 gen(rd());
        binomial_distribution<> binomDis(5,tradeFreq);
        timeTillNextTrade = 6 - binomDis(gen);
        status = TraderStatus::IDLE;
    }

    void resetSentiments(multimap<int,ExchangeAgent> & stocks){
        for (auto i=sentiments.begin();i!=sentiments.end();++i){
            double midPrice = (stocks.find((i ->first)) -> second).midP();
            int band = checkPriceBand(midPrice);
            double increment = priceIncrements.find(band) ->second;
            i->second = ((rand()%2)*2-1)*increment;
        }
    }

    void analyzeStock(const int& stockId,const int& time){
        ExchangeAgent& exchange = (*stocksPtr).find(stockId) -> second;
        double evalScore;
        
        double noise = ((rand()%2)*2-1)*((rand()%(100-intelligence)))/2;

        vector<double>& priceMemoryVec = midPriceMemory.find(stockId)->second;
        double mean = accumulate(priceMemoryVec.begin(),priceMemoryVec.end(),0.0)/priceMemoryVec.size();
        double trend;
        if (mean<priceMemoryVec.back()){
            trend = priceMemoryVec.back()/mean;
        } 
        else if (mean>priceMemoryVec.back()){
            trend = -mean/priceMemoryVec.back();
        }
        else{
            trend=0;
        }
        double trendScore = trend*(rand()%trender);

        double spread = exchange.bASpread();
        double hftScore = spread*(rand()%hft);

        double personalSentiment = sentiments.find(stockId)->second;
        double relFundamentalValue = (exchange.baseFundamentalVal() + mean)/2 + personalSentiment;
        double diff = relFundamentalValue-priceMemoryVec.back();
        double sum = relFundamentalValue+priceMemoryVec.back();
        double meanRevScore = ((diff)/(sum))*200*(rand()%meanReversion);

        evalScore = (trendScore + hftScore + meanRevScore) + noise;
        evalScore /= pow(10,ceil(log10(abs(evalScore))));        

        if (evalScore>0){
            int x;
            multimap<int,double> possiblePrices;
            double lowestAsk = exchange.lowAsk() + priceIncrements.find(checkPriceBand(exchange.lowAsk())) -> second;
            if (time!=0){
                possiblePrices.insert(make_pair(8,lowestAsk));
                int band = checkPriceBand(lowestAsk);
                double nextPrice = lowestAsk;
                for (int i=7;i!=-1;--i){
                    int increment = priceIncrements.find(band) -> second;
                    nextPrice -= increment;
                    band = checkPriceBand(nextPrice);
                    possiblePrices.insert(make_pair(i,nextPrice));
                }
                random_device rd;
                mt19937 gen(rd());
                binomial_distribution<> binomDis(8,evalScore);
                x = binomDis(gen);
            }
            else{
                int band = checkPriceBand(lowestAsk);
                int increment = priceIncrements.find(band) -> second;
                double nextPrice = lowestAsk+5*increment;
                possiblePrices.insert(make_pair(15,lowestAsk+5*increment));
                for (int i=14;i!=-1;--i){
                    int increment = priceIncrements.find(band) -> second;
                    nextPrice -= increment;
                    band = checkPriceBand(nextPrice);
                    possiblePrices.insert(make_pair(i,nextPrice));
                }
                random_device rd;
                mt19937 gen(rd());
                binomial_distribution<> binomDis(15,(evalScore+0.5)/2);
                x = binomDis(gen);
            }
            double orderPrice = possiblePrices.find(x) -> second;
            int orderQuantity = rand()%int(floor(money/orderPrice/10));
            Order order(stockId,traderId,orderPrice,orderQuantity,OrderType::BUY);
            int pendingBuySum = 0;
            for (auto j = pendingBuyOrders.begin(); j!= pendingBuyOrders.end(); ++j){
                multimap<double,int> pQBPairs = j->second;
                for (auto i = pQBPairs.begin();i!=pQBPairs.end();++i){
                    pendingBuySum += i->second * i->first;
                }
            }
            if (orderQuantity != 0 && (money-pendingBuySum)>(orderQuantity*orderPrice)){
                exchange.traderToExchangeLimit(order,time);
                addPendingBuyOrder(order);
            }
        } 
        else if (evalScore<0 && holdings.find(stockId)!=holdings.end()){
            int x;
            multimap<int,double> possiblePrices;
            double highestBid = exchange.highBid() - priceIncrements.find(checkPriceBand(exchange.highBid())) -> second;;
            if (time!=0){
                int band = checkPriceBand(highestBid);
                double nextPrice = highestBid;
                possiblePrices.insert(make_pair(7,highestBid));
                for (int i=6;i!=-1;--i){
                    int increment = priceIncrements.find(band) -> second;
                    nextPrice += increment;
                    band = checkPriceBand(nextPrice);
                    possiblePrices.insert(make_pair(i,nextPrice));
                }
                random_device rd;
                mt19937 gen(rd());
                binomial_distribution<> binomDis(7,abs(evalScore));
                x = binomDis(gen);
            }
            else{
                int band = checkPriceBand(highestBid);
                int increment = priceIncrements.find(band) -> second;
                double nextPrice = highestBid - 5*increment;
                possiblePrices.insert(make_pair(15,highestBid-5*increment));
                for (int i=14;i!=-1;--i){
                    increment = priceIncrements.find(band) -> second;
                    nextPrice += increment;
                    band = checkPriceBand(nextPrice);
                    possiblePrices.insert(make_pair(i,nextPrice));
                }
                random_device rd;
                mt19937 gen(rd());
                binomial_distribution<> binomDis(15,(abs(evalScore)+0.5)/2);
                x = binomDis(gen);
            }
            double orderPrice = possiblePrices.find(x) -> second;
            multimap<double,int> priceQuantityPairs = holdings.find(stockId)->second;
            double averagePrice = 0;
            int totalHoldings = 0;
            for (auto i=priceQuantityPairs.begin();i!=priceQuantityPairs.end();++i){
                averagePrice += i->first;
                totalHoldings += i->second;
            }
            double pctDiff = (orderPrice-averagePrice)/averagePrice *100;
            averagePrice /= totalHoldings;
            if (totalHoldings != 0 && (averagePrice<orderPrice || pctDiff<-riskTolerance)){
                int orderQuantity = rand()%totalHoldings;
                Order order(stockId,traderId,orderPrice,orderQuantity,OrderType::SELL);
                int pendingSellq = 0;
                multimap<double,int> pQSPairs;
                if (pendingSellOrders.find(stockId) != pendingSellOrders.end()){
                    pQSPairs = pendingSellOrders.find(stockId)->second;
                    for (auto i = pQSPairs.begin();i!=pQSPairs.end();++i){
                        pendingSellq += i->second;
                    }
                }
                if (orderQuantity != 0 && orderQuantity<(totalHoldings-pendingSellq)){
                    exchange.traderToExchangeLimit(order,time);
                    addPendingSellOrder(order);
                }
            };
        }
    };

public:
    Trader(const int &id, multimap<int,ExchangeAgent>& exchangeAgentList){
        traderId = id;
        stocksPtr = &exchangeAgentList;
        for (auto i=exchangeAgentList.begin();i!=exchangeAgentList.end();++i){
            int stockId = i->first;
            sentiments.insert(make_pair(stockId,0));
        }
        intelligence = rand()%100;
        trender = rand()%100 + 1;
        smaLength = rand()%30+10;
        hft = rand()%100 + 1;
        meanReversion = rand()%100 + 1;
        tradeFreq = (rand()%30+71)*hft*0.0001;
        money = rand()%100000000 + 500000;
        riskTolerance = rand()%11+5;
    }

    void updateTimer(const vector<int> & stockIds,const int & time){
        timeTillNextTrade -= 1;
        if (timeTillNextTrade <= 0){
            status = TraderStatus::ORDERING;
            double numStocks = stockIds.size();
            int divisor = ceil(numStocks/5);
            for (int id:stockIds){
                if(rand()%divisor==0){
                    analyzeStock(id,time);
                }
            }
            resetTimer();
        }
    }

    void updateSentiments(const int & time, multimap<int,ExchangeAgent> & stocks){
        if (time==0){
            resetSentiments(stocks);
        } 
        else{
            for (auto i=sentiments.begin();i!=sentiments.end();++i){
                double midPrice = (stocks.find((i ->first)) -> second).midP();
                int band = checkPriceBand(midPrice);
                double increment = priceIncrements.find(band) ->second;
                i->second += ((rand()%2)*2-1)*(rand()%4)*increment;
            }
        }
    }

    void updatePriceMemory(){
        multimap<int,ExchangeAgent>& exchangeAgentList = *stocksPtr;
        for (auto i=exchangeAgentList.begin();i!=exchangeAgentList.end();++i){
            int stockId = i->first;
            ExchangeAgent& exchange = i->second;
            double midPrice = exchange.midP();
            if (midPriceMemory.find(stockId) == midPriceMemory.end()){
                vector<double> vec = {midPrice};
                midPriceMemory.insert(make_pair(stockId,vec)); 
            }
            else{
                vector<double> vec = midPriceMemory.find(stockId)->second;
                vec.push_back(midPrice);
                if (vec.size() > smaLength){
                    vec.erase(vec.begin());
                }
                midPriceMemory.find(stockId)->second = vec;
            }
        }
    }

    void addHolding(const Order& order){
        if (holdings.find(order.stockId)!=holdings.end()){
            multimap<double,int>& priceQuantityPairs = holdings.find(order.stockId) ->second;
            if (priceQuantityPairs.find(order.price) != priceQuantityPairs.end()){
                int& existingQuantity = priceQuantityPairs.find(order.price)->second;
                existingQuantity += order.quantity;
            }
            else{
                priceQuantityPairs.insert(make_pair(order.price,order.quantity));
            }
        }
        else{
            multimap<double,int> priceQuantityPairs;
            priceQuantityPairs.insert(make_pair(order.price,order.quantity));
            holdings.insert(make_pair(order.stockId,priceQuantityPairs));
        }
    };

    void removeHolding(const Order& order){
        multimap<double,int>& priceQuantityPairs = holdings.find(order.stockId) ->second;
        int orderQuantity = order.quantity;
        int q;
        for (auto i = priceQuantityPairs.begin();i!=priceQuantityPairs.end();){
            q = i->second - orderQuantity;
            if (q<0){
                i = priceQuantityPairs.erase(i);
                orderQuantity = abs(q);
            }
            else if (q>0){
                i->second = q;
                break;
            }
            else{
                i = priceQuantityPairs.erase(i);
                break;
            }
        }
    };

    void receiveResponse(const Order& order){
        if (order.type == OrderType::BUY){
            multimap<double,int>& priceQuantityPairs = pendingBuyOrders.find(order.stockId)->second;
            int qBef = priceQuantityPairs.find(order.price)->second;
            addPendingBuyOrder(order);
            int qAft = priceQuantityPairs.find(order.price)->second;
            int diff = qBef-qAft;
            if (qAft == 0){
                priceQuantityPairs.erase(priceQuantityPairs.find(order.price));
            }
            Order forHoldings(order.stockId,-1,order.price,diff,order.type);
            addHolding(forHoldings);
            money -= abs(order.price*order.quantity);
        }
        else{
            multimap<double,int>& priceQuantityPairs = pendingSellOrders.find(order.stockId)->second;
            int qBef = priceQuantityPairs.find(order.price)->second;
            addPendingSellOrder(order);
            int qAft = priceQuantityPairs.find(order.price)->second;
            if (qAft == 0){
                priceQuantityPairs.erase(priceQuantityPairs.find(order.price));
            }
            Order forHoldings(order.stockId,-1,order.price,qBef-qAft,order.type);
            removeHolding(forHoldings);
            money += abs(order.price*order.quantity);
        }
    }

    void endDay(){
        pendingBuyOrders.clear();
        pendingSellOrders.clear();
    }
};

int main(){
    system("CLS");
    srand((unsigned) time(0));
    int time = 0;
    int day = 0;

    int dayLimit;
    cout << "How many days(>0)? ";
    cin >> dayLimit;
    int dayLength;
    cout << "How long is one day(>0)? ";
    cin>> dayLength;
    int num_stocks;
    cout << "How many stocks? ";
    cin >> num_stocks;
    int num_traders;
    cout<< "How many traders? ";
    cin>> num_traders;
    int counterLength;
    cout<< "Set OrderBook Length (an int) ";
    cin>>counterLength;
    cout<<endl;


    cout<<"starting"<<endl;
    vector<int> stockIds;
    vector<int> traderIds;
    multimap<int,ExchangeAgent> stocks;
    multimap<int,Trader> traders;
    for (int i =0; i!=num_stocks; ++i){
        int stockId = i+1;
        ExchangeAgent exchange(stockId);
        stocks.insert(make_pair(stockId,exchange));
        stockIds.push_back(stockId);
    }
    for(int i=0; i!=num_traders; ++i){
        int traderId = i+1;
        Trader trader(traderId, stocks);
        traders.insert(make_pair(traderId,trader));
        traderIds.push_back(traderId);
    }
    cout<<"created traders and exchange agents"<<endl;

    for (auto i = stocks.begin();i!=stocks.end();++i){
        ExchangeAgent exchange = i->second;
        multimap<int,Order> response = exchange.initialDistributionOfStocks(traderIds);
        cout<<i->first<<endl;
        for (auto k = response.begin();k!=response.end();++k){
            auto j = traders.find(k->first);
            Trader& trader = j->second;
            trader.addHolding(k->second);
        }
    }

    cout<<"initializing complete"<<endl;

    system("CLS");

    do{
        for (auto i = stocks.begin();i!=stocks.end();++i){
            ExchangeAgent& exchange = i->second;
            exchange.updatefundamentalValue();
        }

        for (auto i = traders.begin();i!=traders.end();++i){
            Trader& trader = i->second;
            trader.updateSentiments(time,stocks);
            trader.updatePriceMemory();
            trader.updateTimer(stockIds,time);
        }

        this_thread::sleep_for(150ms);

        system("CLS");

        cout<<"Day: "<<day<<", Time: "<<time<<endl;

        for (auto i = stocks.begin(); i!=stocks.end();++i){
            ExchangeAgent& exchange = i->second;
            multimap<int,Order> response = exchange.compileBook();
            for (auto j = response.begin();j!=response.end();++j){
                auto k = traders.find(j->first);
                Trader& trader = k->second;
                trader.receiveResponse(j->second);
            }
            exchange.displayBook(counterLength);
        }

        time+=1;
        if (time==dayLength){
            time = 0;
            day += 1;
            for (auto i = stocks.begin();i!=stocks.end();++i){
                ExchangeAgent& exchange = i->second;
                exchange.endDay();
            }
            for (auto i = traders.begin();i!=traders.end();++i){
                Trader& trader = i->second;
                trader.updateSentiments(time,stocks);
            }
        }
    } while (day!=dayLimit);

    cout<<endl;
    cout<<"Simulation Complete. Press ENTER to close.";
    cin.sync();
    cin.get();
    cin.ignore();
}