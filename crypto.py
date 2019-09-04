################################################################################
###                                                                          ###
###                                CRYPTO.PY                                 ###
###                                                                          ###
###  Contains all the classes and functions needed to make trading desitions ###
###                      in cryptomarkets and exchanges                      ###
###                                                                          ###
###             Created by: MarianoOG (contacto@marianoog.com)               ###
###                         Date: December 31th, 2017                        ###
###                                                                          ###
################################################################################

import matplotlib.pyplot as plt
from datetime import datetime
from indicators import bollinger, bollingernormalized, macd, rsi
from json import load
from matplotlib.dates import date2num, num2date, DateFormatter
from mpl_finance import candlestick_ohlc
from re import findall
from requests import get
from termstyle import red, green, blue
from os.path import dirname, realpath

################################################################################
###                  Auxiliar Functions & Global variables                   ###
################################################################################

dir_path = dirname(realpath(__file__))

def createReport(name, body = ''):
    page = '<!DOCTYPE html>\n'
    page += '<html>\n'
    page += '<head>\n'
    page += '<link rel="stylesheet" type="text/css" href="style.css">'
    page += '</head>\n'
    page += '<body>\n'
    page += body
    page += '</body>\n'
    page += '</html>\n'
    with open(dir_path + '/Report/' + name + '.html', "w") as text_file:
        text_file.write(page)

################################################################################
###                               CLASS MARKET                               ###
################################################################################

# Generic class for Market in any exchange
class Market:

    def __init__(self):
        self.date = []
        self.value = []
        self.volume = []
        self.open = []
        self.low = []
        self.high = []
        self.close = []
        self.fee = 0.0

    def plot(self, n = 50):
        m = len(self.date)
        if m == 0:
            print('Markets.plot: No values saved, not posible to plot!')
            return
        elif m < n:
            n = m
        # Create figure
        fig, ax = plt.subplots()
        # Create subplot up
        ax = plt.subplot(211)
        # Candlestick plot
        quotes = [tuple([self.date[i], self.open[i], self.high[i], self.low[i],
                 self.close[i]]) for i in range(m-n,m)]
        candlestick_ohlc(ax, quotes, width=0.6)
        # Value plot
        plt.plot(self.date[m-n:m+1], self.value[m-n:m+1],'y')
        plt.ylabel('Value')
        plt.title(self.name + ': CandleSticks-Value')
        ax.xaxis.set_major_formatter(DateFormatter(''))
        ax.grid(True)
        # Create subplot down
        ax = plt.subplot(212)
        # Volume plot
        plt.bar(self.date[m-n:m+1], self.volume[m-n:m+1], 0.6)
        plt.ylabel('Volume')
        plt.title(self.name + ': Volume')
        ax.xaxis.set_major_formatter(DateFormatter('%b %d, %y'))
        ax.grid(True)
        # Format date, layout and print
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()

    def calculateIndicators(self, b = 20, r = 14, m = [12,26,9]):
        self.bb, self.s, self.l, self.h = bollinger(self.value, b)
        self.macd, self.signal, self.hist = macd(self.value, m[0], m[1], m[2])
        self.rsi = rsi(self.open, self.close, r)
        self.bbn = bollingernormalized(self.value, self.bb, self.s)

    def plotRSI(self, n = 50):
        m = len(self.date)
        if m == 0:
            print('Markets.plotRSI: No values saved, not posible to plot!')
            return
        elif m < n:
            n = m
        fig, ax = plt.subplots()
        plt.plot(self.date[m-n:m+1], self.rsi[m-n:m+1],'r')
        plt.plot(self.date[m-n:m+1], [0.3 for x in self.rsi[m-n:m+1]],'k--')
        plt.plot(self.date[m-n:m+1], [0.7 for x in self.rsi[m-n:m+1]],'k--')
        plt.title(self.name + ': RSI')
        ax.set_ylim(0,1)
        ax.xaxis.set_major_formatter(DateFormatter('%b %d, %y'))
        ax.grid(True)
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()

    def plotMACD(self, n = 50):
        m = len(self.date)
        if m == 0:
            print('Markets.plotMACD: No values saved, not posible to plot!')
            return
        elif m < n:
            n = m
        fig, ax = plt.subplots()
        plt.plot(self.date[m-n:m+1], self.macd[m-n:m+1], 'b')
        plt.plot(self.date[m-n:m+1], self.signal[m-n:m+1], 'r--')
        plt.bar(self.date[m-n:m+1], self.hist[m-n:m+1], 0.6)
        plt.title(self.name + ': MACD')
        ax.xaxis.set_major_formatter(DateFormatter('%b %d, %y'))
        ax.grid(True)
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()

    def plotBB(self, n = 50):
        m = len(self.date)
        if m == 0:
            print('Markets.plotBB: No values saved, not posible to plot!')
            return
        elif m < n:
            n = m
        fig, ax = plt.subplots()
        plt.plot(self.date[m-n:m+1], self.bb[m-n:m+1],'b')
        plt.plot(self.date[m-n:m+1], self.l[m-n:m+1],'y')
        plt.plot(self.date[m-n:m+1], self.h[m-n:m+1],'y')
        plt.plot(self.date[m-n:m+1], self.value[m-n:m+1],'r--')
        plt.ylabel('Value')
        plt.title(self.name + ': Bollinger Bands')
        ax.xaxis.set_major_formatter(DateFormatter('%b %d, %y'))
        ax.grid(True)
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()

    def plotBBn(self, n = 50):
        m = len(self.date)
        if m == 0:
            print('Markets.plotBBn: No values saved, not posible to plot!')
            return
        elif m < n:
            n = m
        fig, ax = plt.subplots()
        plt.plot(self.date[m-n:m+1], self.bbn[m-n:m+1],'r')
        plt.plot(self.date[m-n:m+1], [0.15 for x in self.bbn[m-n:m+1]],'k--')
        plt.plot(self.date[m-n:m+1], [0.85 for x in self.bbn[m-n:m+1]],'k--')
        plt.title(self.name + ': Bollinger Bands (Normalized)')
        ax.set_ylim(0,1)
        ax.xaxis.set_major_formatter(DateFormatter('%b %d, %y'))
        ax.grid(True)
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()

    def plotSummary(self, n = 50, save = False):
        m = len(self.date)
        if m == 0:
            print('Markets.plotSummary: No values saved, not posible to plot!')
            return
        elif m < n:
            n = m

        # Create figure
        fig, ax = plt.subplots()
        # Candlestick plot
        quotes = [tuple([self.date[i], self.open[i], self.high[i], self.low[i],
                 self.close[i]]) for i in range(m-n,m)]
        candlestick_ohlc(ax, quotes, width=0.6)
        # Value plot
        plt.plot(self.date[m-n:m+1], self.value[m-n:m+1],'g')
        # Bollinger Bands
        plt.plot(self.date[m-n:m+1], self.bb[m-n:m+1],'y--')
        plt.plot(self.date[m-n:m+1], self.l[m-n:m+1],'b--')
        plt.plot(self.date[m-n:m+1], self.h[m-n:m+1],'b--')
        plt.ylabel('Value')
        plt.title(self.name + ': CandleSticks-Value')
        ax.xaxis.set_major_formatter(DateFormatter('%b %d, %y'))
        ax.grid(True)
        # Format date, layout and print
        fig.autofmt_xdate()
        fig.tight_layout()
        if save:
            plt.savefig(dir_path + '/Report/Images/' + self.name + '_candles.png')
            plt.close()
        else:
            plt.show()

        # Create figure
        fig, ax = plt.subplots()
        # Create subplot 1
        ax = plt.subplot(311)
        # Plot MACD
        plt.plot(self.date[m-n:m+1], self.macd[m-n:m+1], 'b')
        plt.plot(self.date[m-n:m+1], self.signal[m-n:m+1], 'r--')
        plt.bar(self.date[m-n:m+1], self.hist[m-n:m+1], 0.6)
        plt.title(self.name + ': MACD')
        ax.xaxis.set_major_formatter(DateFormatter(''))
        ax.grid(True)
        # Create subplot 2
        ax = plt.subplot(312)
        # Plot RSI
        plt.plot(self.date[m-n:m+1], self.rsi[m-n:m+1],'r')
        plt.plot(self.date[m-n:m+1], [0.3 for x in self.rsi[m-n:m+1]],'k--')
        plt.plot(self.date[m-n:m+1], [0.7 for x in self.rsi[m-n:m+1]],'k--')
        plt.title(self.name + ': RSI')
        ax.set_ylim(0,1)
        ax.xaxis.set_major_formatter(DateFormatter(''))
        ax.grid(True)
        # Create subplot 3
        ax = plt.subplot(313)
        # Plot BBn
        plt.plot(self.date[m-n:m+1], self.bbn[m-n:m+1],'r')
        plt.plot(self.date[m-n:m+1], [0.15 for x in self.bbn[m-n:m+1]],'k--')
        plt.plot(self.date[m-n:m+1], [0.85 for x in self.bbn[m-n:m+1]],'k--')
        plt.title(self.name + ': Bollinger Bands (Normalized)')
        ax.set_ylim(0,1)
        ax.xaxis.set_major_formatter(DateFormatter('%b %d, %y'))
        ax.grid(True)
        # Format date, layout and print
        fig.autofmt_xdate()
        fig.tight_layout()
        if save:
            plt.savefig(dir_path + '/Report/Images/' + self.name + '_indicators.png')
            plt.close()
        else:
            plt.show()

    def report(self, n = 50, complete = False):
        self.plotSummary(n, True)
        n = len(self.date) - 1
        div = '<div class="market">\n'
        div += '<h2>Market: ' + self.name + '</h2>\n'
        div += '<table>\n'
        div += '<tr>\n'
        div += '<th>Date</th>\n'
        div += '<td>' + num2date(self.date[n]).strftime('%b %d, %Y') + '</td>\n'
        div += '</tr>\n'
        div += '<tr>\n'
        div += '<th>Value</th>\n'
        div += '<td>' + str(self.value[n]) + '</td>\n'
        div += '</tr>\n'
        div += '<tr>\n'
        div += '<th>RSI:</th>\n'
        div += '<td><font'
        if self.rsi[n] >= 0.7:
            div += ' class="loss">' + str(self.rsi[n])
        elif self.rsi[n] <= 0.3:
            div += ' class="win">' + str(self.rsi[n])
        else:
            div += '>' + str(self.rsi[n])
        div += '</font></td>\n'
        div += '</tr>\n'
        div += '<tr>\n'
        div += '<th>BBn:</th>\n'
        div += '<td><font'
        if self.bbn[n] >= 0.85:
            div += ' class="loss">' + str(self.bbn[n])
        elif self.bbn[n] <= 0.15:
            div += ' class="win">' + str(self.bbn[n])
        else:
            div += '>' + str(self.bbn[n])
        div += '</font></td>\n'
        div += '</tr>\n'
        div += '</table>\n'
        div += '<div class="row">\n'
        div += '<div class="column">\n'
        div += '<img src="Images\\' + self.name + '_candles.png">\n'
        div += '</div>\n'
        div += '<div class="column">\n'
        div += '<img src="Images\\' + self.name + '_indicators.png">\n'
        div += '</div>\n'
        div += '</div>\n'
        div += '</div>\n'
        if complete:
            createReport(self.name + '_report',div)
        else:
            return div

    def buy(self, price, amount, coin = True):
        if coin:
            return amount * price / (self.fee - 1.0)
        else:
            return (1 - self.fee) * amount / (price * 1.0)

    def sell(self, price, amount, coin = True):
        if coin:
            return (1 - self.fee) * amount * price
        else:
            return amount / (price * 1.0 * (self.fee - 1))

################################################################################
###                            CLASS BITSOMARKET                             ###
################################################################################

# Specific Market in Bitso
class BitsoMarket(Market):

    def __init__(self, uri, name, fee):
        self.uri = uri
        self.name = name
        self.fee = fee
        self.update()

    def update(self):
        self.date = []
        self.value = []
        self.volume = []
        self.open = []
        self.low = []
        self.high = []
        self.close = []
        code = get('https://bitso.com/trade/market/' + self.uri).text
        line = findall(r'chartData = \[\{.*\}\]', code)[0]
        data = line.split(' = ')[1]

        with open(dir_path + "/Data/" + self.name + ".json", "w") as text_file:
            text_file.write(data)
        with open(dir_path + "/Data/" + self.name + ".json") as data_file:
            data = load(data_file)

        for x in data:
            self.date.append(date2num(datetime.strptime(x["date"],'%Y-%m-%d')))
            self.value.append(x["vwap"])
            self.volume.append(x["volume"])
            self.open.append(x["open"])
            self.low.append(x["low"])
            self.high.append(x["high"])
            self.close.append(x["close"])

        self.calculateIndicators()

################################################################################
###                               CLASS TRADE                                ###
################################################################################

class Trade:

    def __init__(self, market, base = Market()):
        self.market = market
        self.amount = 0.0  # Of coins
        self.cost = 0.0    # In base
        self.hodings = 0.0 # Estimation in base
        self.gain = 0.0    # Estimation in base

    def buy(self, price, amount, coin = True):
        if coin:
            self.cost += self.market.buy(price, amount)
            self.amount += amount
        else:
            self.cost -= amount
            self.amount += self.market.buy(price, amount, False)
        self.estimate()

    def sell(self, price, quantity, coin = True):
        if coin:
            if quantity > self.amount:
                quantity = self.amount
            self.cost += self.market.sell(price, quantity)
            self.amount -= quantity
            self.estimate()
        else:
            quantity = - self.market.sell(price, quantity, False)
            self.sell(price, quantity)

    def estimate(self):
        self.holdings = self.market.sell(self.market.value[-1], self.amount)
        self.gain = self.holdings + self.cost

    def estimateAlt(self, m):
        c = - self.m.sell(self.m.value[-1], self.cost)
        h = - self.m.sell(self.m.value[-1], self.holdings)
        g = c + h
        return c, h, g

    def update(self):
        self.market.update()
        self.estimate()

    def report(self):
        print('*************************')
        print("Amount:\t%s" % blue(self.amount))
        if self.cost < 0.0:
            print("Cost:\t%s" % red(self.cost))
        elif self.cost > 0.0:
            print("Cost:\t%s" % green(self.cost))
        else:
            print("Cost:\t%s" % blue(self.cost))
        print("Hold:\t%s" % blue(self.holdings))
        if self.gain < 0.0:
            print("Gain: \t%s" % red(self.gain))
        elif self.gain > 0.0:
            print("Gain: \t%s" % green(self.gain))
        else:
            print("Gain: \t%s" % blue(self.gain))

################################################################################
###                              CLASS EXCHANGE                              ###
################################################################################

class Exchange:

    def __init__(self):
        self.name = ''
        self.markets = []

    def update(self):
        for m in self.markets:
            m.update()

    def plot(self, n = 50):
        for m in self.markets:
            m.plot(n)

    def plotSummary(self, n = 50, save = False):
        for m in self.markets:
            m.plotSummary(n, save)

    def report(self, n = 50, ind = False):
        s = ''
        for m in self.markets:
            s += m.report(n, False)
            if ind:
                m.report(n, ind)
        createReport(self.name + '_Exchange_Report', s)

################################################################################
###                           CLASS BITSOEXCHANGE                            ###
################################################################################

class BitsoExchange(Exchange):

    def __init__(self):
        uris =  ['btc/mxn', 'eth/mxn', 'xrp/mxn', 'ltc/mxn', 'bch/mxn', 'tusd/mxn', 'mana/mxn', 'gnt/mxn', 'bat/mxn',
                            'eth/btc', 'xrp/btc', 'ltc/btc', 'bch/btc', 'tusd/btc', 'mana/btc', 'gnt/btc', 'bat/btc']
        names = ['MXN_BTC', 'MXN_ETH', 'MXN_XRP', 'MXN_LTC', 'MXN_BCH', 'MXN_TUSD', 'MXN_MANA', 'MXN_GNT', 'MXN_BAT',
                            'BTC_ETH', 'BTC_XRP', 'BTC_LTC', 'BTC_BCH', 'BTC_TUSD', 'BTC_MANA', 'BTC_GNT', 'BTC_BAT']
        fees =  [0.01,    0.01,    0.008,  0.005,   0.005,
                 0.0015,  0.0015,  0.0015, 0.0025]
        self.name = 'Bitso'
        self.markets = []
        for u, n, f in zip(uris,names,fees):
            self.markets.append(BitsoMarket(u,n,f))

################################################################################
###                                  TESTS                                   ###
################################################################################

bitso = BitsoExchange()
bitso.report(60,True)

#MXN_BTC = bitso.markets[0]
#t = Trade(MXN_BTC)
