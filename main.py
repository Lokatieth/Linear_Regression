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

    try:
        prices = [(x[1] - min_pri) / (max_pri - min_pri) for x in points]
    except ZeroDivisionError:
        print ("All prices are the same, every prediction will be ", min_pri)
        exit()
    try:
        mileages = [(x[0] - min_mil) / (max_mil - min_mil) for x in points]
    except ZeroDivisionError:
        print ("All mileages are the same, every prediction will be unstable")
        exit()
    return zip(mileages, prices)
    
    
def gradient_descent(mileages, prices, delta = 0.01, epochs = 200):

    global theta0
    global theta1
    for i in range(0, epochs):
        yp = [(theta0 + theta1 * x) for x in mileages]
        SSE = [1/2 * ((y - (theta0 + theta1 * x)) * (y - (theta0 + theta1 * x))) for x, y in zip(mileages, prices)]
        dSSEa = [-(y - (theta0 + theta1 * x)) for x,y in zip(mileages, prices)]
        dSSEb = [-(y - (theta0 + theta1 * x)) * x for x,y in zip(mileages, prices)]
        newtheta0 = theta0 - delta * sum(dSSEa)
        newtheta1 = theta1 - delta * sum(dSSEb)
        
        theta0 = newtheta0
        theta1 = newtheta1

def parse_columns(lines):

    if lines[0] != "km,price" or not lines:
        print ("You need to have two columns : \"km\" and \"price\" at the top of the file.")
        exit()
    for line in lines[1:]:
        detailed = line.split(',');
        if len(detailed) == 2 and detailed[0].isdigit() and detailed[1].isdigit():
            points.append((int(detailed[0]), int(detailed[1])))

    mileages = [x[0] for x in points]
    prices = [y[1] for y in points]
    
                

with open('data.csv') as data:
    lines = data.readlines()
    lines = [line.rstrip('\n') for line in lines]

ret = parse_columns(lines)

points = normalize_data(points)
mileages, prices =  zip(*points)
gradient_descent(mileages, prices)
fh = open("trained.csv", "w") 
 
fh.write(str(theta0) + "\n" +  
str(theta1) + "\n" +
str(min_mil) + "\n" +
str(max_mil) + "\n" +
str(min_pri) + "\n" +
str(max_pri) + "\n")
fh.close() 
 

plt.plot([x[0] * (max_mil - min_mil) + min_mil for x in points], [y[1] * (max_pri - min_pri) + min_pri for y in points], 'bo')
plt.plot([x[0] * (max_mil - min_mil) + min_mil for x in points], [(theta0 + x[0] * theta1) * (max_pri - min_pri) + min_pri for x in points])
plt.xlabel("Mileage")
plt.ylabel("Price")
plt.show()