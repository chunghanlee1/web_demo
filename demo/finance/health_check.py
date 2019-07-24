import numpy as np
import scipy.stats as stats
import random
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool
import time
import sys

def investmentResult(investmentRisk, userCurrentAge, userDeathAge):
    """
    Identifies user portfolio risk-return characteristics for simulation
    Input: 
        investmentRisk (Int): User selected investment riskiness ranking
        userCurrentAge (Int): User current age
        userDeathAge (Int): User expected mortality age, used to calculate life expectancy
    Output: List of simulated yearly investment return until death
    """
    #Set risk and return
    yearlyInvestmentResult = []
    if investmentRisk < 2: 
        assetReturn = 0.01
        assetRisk = 0.01
    elif investmentRisk < 4:
        assetReturn = 0.03
        assetRisk = 0.08
    elif investmentRisk < 6:
        assetReturn = 0.05
        assetRisk = 0.1
    elif investmentRisk < 8:
        assetReturn = 0.07
        assetRisk = 0.15
    else:
        assetReturn = 0.1
        assetRisk = 0.2
    #Specify investment result using Monte Carlo simulation
    for i in range(userCurrentAge, userDeathAge):
        yearlyInvestmentResult.append(random.gauss(assetReturn, assetRisk))
    return yearlyInvestmentResult


def yearlyTotalIncome(userIncome, incomeGrowth, userCurrentAge, userDeathAge, userRetirementAge):
    """
    Exrapolate user income to future years until retirement. Income after retirement is assumed to be 0.
    Input: 
        userIncome (Int): Current income level
        incomeGrowth (Float): Decimal figure that indicates the income growth rate every year
        userCurrentAge (Int): User current age
        userDeathAge (Int): User expected mortality age, used to calculate life expectancy
        userRetirementAge (Int): User retirement age
    Output: List of extrapolated yearly income until death age. 
    """
    lifetimeIncome = []
    for i in range(userCurrentAge, userDeathAge):
        if i <= userRetirementAge:
            lifetimeIncome.append(userIncome*((1+incomeGrowth)**(i-userCurrentAge)))
        else:
            lifetimeIncome.append(0)
    return lifetimeIncome


def yearlyTotalSpending(userSpending, inflation, userCurrentAge, userDeathAge):
    """
    Exrapolate user spending to future years until death
    Input: 
        userSpending (Int): Current spending level
        inflation (Float): Decimal figure that indicates the spending growth rate every year
        userCurrentAge (Int): User current age
        userDeathAge (Int): User expected mortality age, used to calculate life expectancy
    Output: List of extrapolated yearly spending until death age
    """
    lifetimeSpending = []
    for i in range(userCurrentAge, userDeathAge):
        lifetimeSpending.append(userSpending*((1+inflation)**(i-userCurrentAge)))
    return lifetimeSpending

def simGraph(yearlyResult):
    """
    Visualize yearly result to show average and worst case scenarios
    Input: 
        yearlyResult (List): A nested list of simulations over multiple years
    Output: A graph of results that plots the different possible scenarios
    """
    worstCase = []
    poorCase = []
    averageCase = []
    for i in yearlyResult:
        worstCase.append(np.percentile(i, 5))
        poorCase.append(np.percentile(i, 25))
        averageCase.append(np.percentile(i, 50))
    
    x=[str(i) for i in range(len(poorCase))]
    p=figure(x_range=x, 
            plot_height=500, 
            plot_width=500,
            title='Simulated Wealth Over Time',
            toolbar_location='right', 
            tools='wheel_zoom,hover,pan',
            x_axis_label="Years from now",
            y_axis_label='Net Worth')
    p.line(x=x, y=worstCase, legend='worst case', line_width=3, line_color=(225,0,0))
    p.line(x=x, y=poorCase, legend='poor case', line_width=3, line_color=(150,30,30))
    p.line(x=x, y=averageCase, legend='average case', line_width=3, line_color=(100,50,50))
    p.legend.location='bottom_right'
    script,div = components(p)
    return (script,div)

def simOutputClassification(netWealth):
    """
    Classification of simulation data to present diagnosis result
    Input:
        netWealth (List): List of possible wealth outcome for the simulation trials
    Output: String of diagnostic content
    """
    p = np.percentile(netWealth, 5)
    probRuin = stats.percentileofscore(netWealth, 0)
    if probRuin < 1 :
        return ("Congratulations, your financial situation is excellent! In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%")
    elif probRuin <= 5:
        return ("Your condition is safe! In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%")
    elif probRuin <= 10:
        return ("You have a pretty decent financial condition! In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%")
    elif probRuin <= 20:
        return ("Your financial condition is not bad. In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%")
    elif probRuin <= 30:
        return ("Your financial condition is a bit shaky... In the worst case you will have " + str(p) + " dollars left. And the chance for you to get into financial trouble is: " + str(probRuin) + "%")
    elif probRuin <= 40:
        return ("Hmm...It seems like your current financial situation is not robust enough...There is a "+ str(probRuin) + "% chance you will not have enough money by the end of your life. In the worst case, you will have " + str(p) + " dollars...")
    elif probRuin > 40:
        return ("Oh no...It seems like your current financial situation is pretty lousy...There is a "+ str(probRuin) + "% chance you will not have enough money by the end of your life. In the worst case, you will have " + str(p) + " dollars...")
    

def reqReturnOutputClassification(reqReturn):
    """
    Classification of required return data to present diagnosis result
    Input:
        netWealth (Float): Target required return to satisfy the needs throughout planning horizon
    Output: String of diagnostic content
    """
    if reqReturn <= 0.001 :
        return ("Congratulations, your financial condition is awesome, you don't need any investment to achieve your financial goals! Your required return is: " + str(reqReturn*100) + "%")
    elif reqReturn < .02:
        return ("Congratulations, your financial condition is very secure, just need a little bit investment to achieve your financial goals! Your required return is: " + str(reqReturn*100) + "%")
    elif reqReturn < .04:
        return ("Your financial condition is pretty good. Your required return is: " + str(reqReturn*100) + "%")
    elif reqReturn < .06:
        return ("Your financial condition is ok. Your required return is: " + str(reqReturn*100) + "%")
    elif reqReturn < .08:
        return ("Your financial condition requires some attention... Your required return is: " + str(reqReturn*100) + "%")
    elif reqReturn < .09:
        return ("Your financial condition is a bit dangerous... Your required return is: " + str(reqReturn*100) + "%")
    elif reqReturn >= .09:
        return ("You are in a very dangerous financial condition.... Your required return is: " + str(reqReturn*100) + "% or above")

def simHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, investmentRisk, userCurrentAge, userDeathAge, userRetirementAge):
    """
    Monte Carlo based financial health check function: Using simulation to test the expected financial situation of user
    Input: User financial information
    Output: Diagnosis result
    """
    yearlyDetails = [[] for _ in range(userDeathAge-userCurrentAge)]#create a nested list to hold yearly savings
    lifetimeIncome = yearlyTotalIncome(userIncome, incomeGrowth, userCurrentAge, userDeathAge, userRetirementAge)
    lifetimeSpending = yearlyTotalSpending(userSpending, inflation, userCurrentAge, userDeathAge)
    userCurrentSavings = userSavings
    for i in range(5000):#Repeat Lifetime 5000 times    
        userSavings = userCurrentSavings
        yearlyInvestmentResult = investmentResult(investmentRisk, userCurrentAge, userDeathAge)
        for j in range(userCurrentAge-userCurrentAge, userDeathAge-userCurrentAge):
            #Calculate net savings every period
            if userSavings < 0:
                userSavings = userSavings + lifetimeIncome[j] - lifetimeSpending[j]
            else:
                userSavings = (userSavings*(1+yearlyInvestmentResult[j]) + lifetimeIncome[j] - lifetimeSpending[j])
            yearlyDetails[j].append(userSavings)
    script,div = simGraph(yearlyDetails)
    result_description= simOutputClassification(yearlyDetails[userDeathAge-userCurrentAge-1])
    return (result_description, script, div)

def reqReturnHealthCheck(userIncome, incomeGrowth, userSpending, inflation, userSavings, userCurrentAge, userDeathAge, userRetirementAge):
    """
    Required return based financial health check function: Using bisection search to find the needed return level to sustain spending throughout planning horizon
    Input: User financial information
    Output: User required return to achieve financial goal. 
    """
    lifetimeIncome = yearlyTotalIncome(userIncome, incomeGrowth, userCurrentAge, userDeathAge, userRetirementAge)
    lifetimeSpending = yearlyTotalSpending(userSpending, inflation, userCurrentAge, userDeathAge)
    minReqReturn = 0
    maxReqReturn = 0.2#20% is a very high return requirement
    userCurrentSavings = userSavings
    for i in range(200):#Don't want to enter a loop forever in case there's no solution
        reqReturn = (minReqReturn + maxReqReturn)/2
        userSavings = userCurrentSavings#Reset financial condition
        for i in range(userCurrentAge-userCurrentAge, userDeathAge-userCurrentAge):
            if userSavings < 0:
                userSavings = userSavings + lifetimeIncome[i] - lifetimeSpending[i]
            else:
                userSavings = (userSavings*(1+reqReturn) + lifetimeIncome[i] - lifetimeSpending[i])
        if abs(userSavings) <= 1:#Solution found
            break
        elif userSavings >1:
            maxReqReturn = reqReturn
        elif userSavings <1:
            minReqReturn = reqReturn
    return reqReturnOutputClassification(reqReturn)

if __name__=='__main__':
    result_description, result_plot = simHealthCheck(userIncome=100, 
                    incomeGrowth=0.05, 
                    userSpending=90, 
                    inflation=0.03, 
                    userSavings=2000, 
                    investmentRisk=5, 
                    userCurrentAge=50, 
                    userDeathAge=100, 
                    userRetirementAge=70)
    print(result_description)
