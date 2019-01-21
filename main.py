from __future__ import division
import numpy as np;
import matplotlib.pyplot as plt;
import re;

mileages = []
prices = []
points = []
theta0 = 0.0
theta1 = 0.0
min_mil = 0
max_mil = 0
min_pri = 0
max_pri = 0


def normalize_data(points):
    global min_mil
    global max_mil
    global min_pri
    global max_pri

    mileages = [x[0] for x in points]
    prices = [x[1] for x in points]

    mileage_sum = sum(mileages)
    price_sum = sum(prices)
    min_mil = min(mileages)
    max_mil = max(mileages)
    min_pri = min(prices)
    max_pri = max(prices)

    mileages = [(x[0] - min_mil) / (max_mil - min_mil) for x in points]
    prices = [(x[1] - min_pri) / (max_pri - min_pri) for x in points]
    return zip(mileages, prices)
    
    
def gradient_descent(mileages, prices, delta = 0.01, epochs = 1000):

    # for mileage, price in zip(mileages, prices):
    #     print mileage,'\t', price#, '\t', theta0 + theta1 * mileage
    global theta0
    global theta1
    for i in range(0, epochs):
    #     pred_price = theta0 + theta1 *
        yp = [(theta0 + theta1 * x) for x in mileages]
        SSE = [1/2 * ((y - (theta0 + theta1 * x)) * (y - (theta0 + theta1 * x))) for x, y in zip(mileages, prices)]
        dSSEa = [-(y - (theta0 + theta1 * x)) for x,y in zip(mileages, prices)]
        dSSEb = [-(y - (theta0 + theta1 * x)) * x for x,y in zip(mileages, prices)]
        newtheta0 = theta0 - delta * sum(dSSEa)
        newtheta1 = theta1 - delta * sum(dSSEb)
        
        theta0 = newtheta0
        theta1 = newtheta1
        # print theta0,'\t',theta1, sum(SSE)
        # for mileage, price, yp, SSE, dSSEa, dSSEb in zip(mileages, prices, yp, SSE, dSSEa, dSSEb):
        #     print mileage,'\t', price, '\t', yp, '\t', SSE , '\t', dSSEa, '\t', dSSEb
        # print sum(SSE)

    



def linear_regression(mileages, prices):

    size = len(mileages)
    mileage_sum = sum([x for x in mileages])
    price_sum = sum([x for x in prices])
    mileage_mean = mileage_sum / size
    price_mean = price_sum / size
    
    squared_mileage_sum = sum([x*x for x in mileages])
    squared_price_sum = sum([x*x for x in prices])

    product_sum = sum([x * y for x,y in zip(prices, mileages)])

    interrupt = (price_sum * squared_mileage_sum - mileage_sum * product_sum) / (size * squared_mileage_sum - (mileage_sum * mileage_sum))
    slope = (size * product_sum - mileage_sum * price_sum) / (size * squared_mileage_sum - (mileage_sum * mileage_sum))


    
    return(interrupt, slope)




def parse_columns(lines):
    if lines[0] != "km,price":
        print "You need to have two columns : \"km\" and \"price\" at the top of the file."
        exit()
    for line in lines[1:]:
        detailed = line.split(',');
        if len(detailed) == 2 and detailed[0].isdigit() and detailed[1].isdigit():
            points.append((int(detailed[0]), int(detailed[1])))

    mileages = [x[0] for x in points]
    prices = [y[1] for y in points]
    
                

with open('data.csv') as data:
# with open('test.csv') as data:
    lines = data.readlines()
    lines = [line.rstrip('\n') for line in lines]

ret = parse_columns(lines)

points = normalize_data(points)
mileages, prices =  zip(*points)

axb = linear_regression([x[0] for x in points], [y[1] for y in points])

gradient_descent(mileages, prices)
# 250 000, 3600
estim = (60000 - min_mil) / (max_mil - min_mil)
estimlol = theta0 + theta1 * estim
prixestime = (estimlol * (max_pri - min_pri) + min_pri)
print theta0, theta1, estimlol, prixestime

# print min_mil

# plt.plot([x[0] for x in points], [y[1] for y in points], 'bo')
# plt.plot([x[0] for x in points], [(var[0] + var[1] * float(y[0])) for y in points])
plt.plot([x[0] for x in points], [axb[0] + x[0] * axb[1] for x in points])
plt.xlabel("Mileage")
plt.ylabel("Price")
plt.show()