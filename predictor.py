import sys

theta0 = 0
theta1 = 0
data = []

try:
    f = open('trained.csv', 'r')
except OSError:
    print("Cannot open the file\n")
else:
    s = f.readlines()
    if (len(s) != 6):
        print "Woops ! Looks likethis is not the correct number of lines"
        exit()
    for i in s:
        data.append(float(i))
    f.close()

mileage = input("Hi ! Enter the mileage of your car here : ")
def estimate_price(data, mileage):
    global theta0
    global theta1

    theta0 = data[0]
    theta1 = data[1]
    min_mil = data[2]
    max_mil = data[3]
    min_pri = data[4]
    max_pri = data[5]

    try:
        est = ((theta0 + theta1 * (mileage - min_mil) / (max_mil - min_mil)) * (max_pri - min_pri) + min_pri)
    except OSError:
        print("Cannot open the file\n")
    return est


print "Your car is worth approx. :",  estimate_price(data, mileage), "dollars on estimate\n"