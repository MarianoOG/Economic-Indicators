################################################################################
###                                                                          ###
###                              INDICATORS.PY                               ###
###                                                                          ###
###    This file have functions that calculate diferent trading indicators   ###
###                                                                          ###
###                 Created by: Ona309 (onariam309@gmail.com)                ###
###                         Date: December 31th, 2017                        ###
###                                                                          ###
################################################################################

from numpy import mean, std

################################################################################
###                            INDICATOR FUNCTIONS                           ###
################################################################################

# Exponential Moving Average
def ema(values, n, d = 0):
    if d < 0:
        d = 0
    k = 2/(n+1.0)
    avg = []
    for i in range(len(values)):
        if i < n:
            avg.append(mean(values[0:i+1]))
        elif i < n + d:
            avg.append(mean(values[i-n+1:i+1]))
        else:
            avg.append(k*values[i] + (1-k)*avg[-1])
    return avg

# Simple Moving Average
def sma(values, n):
    avg = []
    for i in range(len(values)):
        if i < n:
            avg.append(mean(values[0:i+1]))
        else:
            avg.append(mean(values[i+1-n:i+1]))
    return avg

# Simple Moving Average
def smd(values, n):
    s = []
    for i in range(len(values)):
        if i < n:
            s.append(std(values[0:i+1]))
        else:
            s.append(std(values[i+1-n:i+1]))
    return s

# Change per period
def change(vopen,vclose):
    delta = [(y - x) for x, y in zip(vopen, vclose)]
    return delta

# Normalized Relative Strenght Index
def rsi(vopen, vclose, n):
    delta = change(vopen,vclose)
    # Absolute gain or loss
    gain = []
    loss = []
    for x in delta:
        if x < 0:
            gain.append(0)
            loss.append(-x)
        else:
            gain.append(x)
            loss.append(0)
    # EMA of gain/loss
    avgGain = ema(gain, n)
    avgLoss = ema(loss, n)
    # Normalized Relative Strengt
    strenght = []
    for g, l in zip(avgGain, avgLoss):
        if l == 0:
            strenght.append(1)
        else:
            strenght.append(1-l/(l+g))
    return strenght

# Moving Average Convergence/Divergence
def macd(values, a, b, c):
    emaa = ema(values, a)
    emab = ema(values, b)
    convdiv = [(x - y) for x, y in zip(emaa, emab)]
    signal = ema(convdiv, c, b - 1)
    hist = [(x - y) for x, y in zip(convdiv, signal)]
    return convdiv, signal, hist

# Boolinger Bands
def bollinger(values, n):
    avg = sma(values, n)
    s = smd(values, n)
    low = [(x - 2*y) for x, y in zip(avg, s)]
    high = [(x + 2*y) for x, y in zip(avg, s)]
    return avg, s, low, high

# Boolinger Bands Normalized
def bollingernormalized(values, avg, st):
    bbn = []
    for v, m, s in zip(values, avg, st):
        d = v - m
        if d >= 2*s:
            bbn.append(1)
        elif d <= -2*s:
            bbn.append(0)
        else:
            bbn.append((d+2*s)/(4*s))
    return bbn
