import math 
import datetime as dt
import pandas as pd
from scipy.stats import norm
import os
from django.conf import settings

def fi(x):
      return norm.cdf(x)

def normalInv(x):
    return ((1/math.sqrt(2*math.pi)) * math.exp(-x*x*0.5))

def blackScholesCall(S0, K, r, T, sigma, q=0):
    ret = {}
    if (S0 > 0 and K > 0 and r >= 0 and T > 0 and sigma > 0):        
        d1 = ( math.log(S0/K) + (r -q +sigma*sigma*0.5)*T ) / (sigma * math.sqrt(T))
        ret['d1'] = d1
        d2 = d1 - sigma*math.sqrt(T)
        ret['d2'] = d2
        ret['prime'] = math.exp(-q*T) * S0 * fi(d1)- K*math.exp(-r*T)*fi(d2)
        ret['delta'] = math.exp(-q*T) * fi(d1)
        ret['gamma'] = (normalInv(d1) * math.exp(-q*T)) / (S0 * sigma * math.sqrt(T))
        ret['vega'] = S0 * math.exp(-q*T) * normalInv(d1) * math.sqrt(T)
        ret['theta'] = ( -((S0*sigma*math.exp(-q*T))/(2*math.sqrt(T))) * normalInv(d1) - r*K*(math.exp(-r*T))*fi(d2) + q*S0*(math.exp(-q*T)) * fi(d1) )
    else:
        ret['error']= "Error in parameters"
    return ret

def blackScholesPut(S0, K, r, T, sigma, q=0):
    ret = {}
    if (S0 > 0 and K > 0 and r >= 0 and T > 0 and sigma > 0):        
        d1 = ( math.log(S0/K) + (r -q +sigma*sigma*0.5)*T ) / (sigma * math.sqrt(T))
        ret['d1'] = d1
        d2 = d1 - sigma*math.sqrt(T)
        ret['d2'] = d2
        ret['prime'] = K*math.exp(-r*T)*fi(-d2) - math.exp(-q*T) * S0 * fi(-d1)
        ret['delta'] = - math.exp(-q*T) * fi(-d1)
        ret['gamma'] = math.exp(-q*T) * normalInv(d1) / (S0 * sigma * math.sqrt(T))
        ret['vega'] = S0 * math.exp(-q*T) * normalInv(d1) * math.sqrt(T)
        ret['theta'] = ( -((S0*sigma*math.exp(-q*T))/(2*math.sqrt(T))) * normalInv(d1) + r*K*(math.exp(-r*T))*fi(-d2) - q*S0*(math.exp(-q*T)) * fi(-d1) )
    else:
        ret['error']= "Error in parameters"
    return ret
    
def impliedVolatility(S0, K, r, T, prime, optionType):
    if (S0 > 0 and K > 0 and r >= 0 and T > 0):        
        iterations = 300
        pr_upper = prime
        pr_lower = prime
        iv_lower = iterations
        iv = iterations
        for number in range(1,iterations):
            sigma = (number)/100
            primeCalc = 0
            if optionType == 'call':
                primeCalc = blackScholesCall(S0, K, r, T, sigma)['prime']
            elif optionType == 'put':
                primeCalc = blackScholesPut(S0, K, r, T, sigma)['prime']
            if primeCalc > prime:
                iv_lower = number -1
                pr_upper = primeCalc
                break
            else:
                pr_lower = primeCalc
        
        p_range = (prime - pr_lower) / (pr_upper - pr_lower)
        iv = (iv_lower + p_range) / 100
    else:
        iv = {'error':'Error in parameters'}
    return(iv)    
    
def getFreeRiskInterestRate(date):
    path = os.path.join(settings.STATIC_ROOT,'FEDFUNDS.csv')
    df = pd.read_csv(path)
    date = dt.date(date.year, date.month, 1)
    return df.loc[df['DATE'] == date.strftime("%Y-%m-%d")]['FEDFUNDS'].values[0]/100
        
class BlackScholes():       
    def getOptionGreeks(optionType, spotPrice, strikePrice, optionPrice, currentDate, expirationDate):
        ret = {}
        today = dt.datetime.utcnow()    
        try:
            currentDate = dt.datetime.strptime(currentDate,"%Y-%m-%d")
            expirationDate = dt.datetime.strptime(expirationDate,"%Y-%m-%d")
        except:
            ret['error'] = "Dates should have yyyy-mm-dd format"
            return ret

        if currentDate > today:
            ret['error'] = "Current date should't be in the future"
            return ret
        
        timeInYears = (expirationDate - currentDate).days / 365
        
        if timeInYears < 0:
            ret['error'] = "Expiration date should be equal or greater than current date"
            return ret
        if optionType.lower() not in ['call', 'put']:
            ret['error'] = "Option Type should be ethier CALL or PUT"
            return ret
        try:
            spotPrice = float(spotPrice)
            strikePrice = float(strikePrice)
            optionPrice = float(optionPrice)
        except:
            ret['error'] = "Prices should be decimal numbers"
            return ret
        if spotPrice <= 0 or strikePrice <=0 or optionPrice <= 0:
            ret['error'] = "Prices shoud be greater than 0"
            return ret
        
        freeRiskInterestRate = getFreeRiskInterestRate(currentDate)
        sigma = impliedVolatility(spotPrice, strikePrice, freeRiskInterestRate, timeInYears, optionPrice, optionType.lower())
        if optionType.lower() == 'call':
            result = blackScholesCall(spotPrice, strikePrice, freeRiskInterestRate, timeInYears, sigma)
            return {
             'delta':result['delta'],
             'gamma':result['gamma'], 
             'vega':result['vega'], 
             'theta':result['theta'], 
             'sigma': sigma, 
             'fedFundRate': freeRiskInterestRate,
             'd1': result['d1'],
             'd2': result['d2'] 
             }
        elif optionType.lower() == 'put':
            result = blackScholesPut(spotPrice, strikePrice, freeRiskInterestRate, timeInYears, sigma)
            return {
             'delta':result['delta'],
             'gamma':result['gamma'], 
             'vega':result['vega'], 
             'theta':result['theta'], 
             'sigma': sigma, 
             'fedFundRate': freeRiskInterestRate,
             'd1': result['d1'],
             'd2': result['d2']
             }

    