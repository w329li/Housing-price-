#!/usr/bin/python
# encoding:utf-8
import json
import os.path
from pathlib import *
from pprint import pprint
import numpy as np
import statsmodels.api as sm



## convert money(a string) into integer since all data related to expense
##   has the expression like: $xxx,xxx, so we need to remove the dollar sign
##   and comm
def strToint(string):
    if ("$" in string): string = string.replace("$","")
    while(","in string): string = string.replace(",","")
    return string




#####read given data from the attr file and build list of list to record all potentially useful data#######

def readjson():
    path = './scraped_data/'
    data_list = []
    acc = 1
    for i in range(0,44):
        file_path = Path(path+str(i)+".attrs")
        if file_path.exists():
            data = json.load(open(path+'0.attrs'))
            ######rename = "new"+str(i)+".json"
            for entry in data:

                ############basic properties of houses#########################
                soldPrice = data[entry]["Sold Price"]
                listPrice = data[entry]["List Price"]
                listPrice = float(strToint(listPrice))
                soldPrice = float(strToint(soldPrice))
                bedrms = float(data[entry]["Bedrms"])
                bathfull = float(data[entry]["Baths Full"])
                size = float(data[entry]["Tot Flr Area AG Metres"])
                age = float(data[entry]["day_sold"][-4:]) - float(data[entry]["Yr Built"])

                ##########Previous: follow the order: index, name, listPrice, soldPrice,size,#bedrooms, #bathsrooms,age
                ##########Present: follow the order: soldPrice, listPrice,size, #bedrooms,#bathsrooms,age
                #######################################################################################
                data_list.append( [soldPrice,listPrice ,size,bedrms, bathfull,age])
                acc = acc+1
    return data_list

#####################################################end_for_this_function############################


## toatlly there are 21912 houses ###
dataFile = readjson()

print("total data we have: "+ str(len(dataFile)))

#### only get first element in each sublist of dataFile since we need reponse variates
def response(dataFile):
    new = []
    length = len(dataFile)
    for i in range(0,length):
        new = new + [dataFile[i][0]]
    return new



#### delete (n-1)th element in each sublist of dataFile since we only need explanatory variates
def update(dataFile,n):
    length = len(dataFile)
    for i in range(0,length):
        ##dataFile[i] = dataFile[i]
        dataFile[i] = dataFile[i][:n]+ dataFile[i][n+1:]
    return dataFile

##################################################3



ResponseVar = response(dataFile)

## remove the response variate from dataFile
dataFile = update(dataFile,0)


print(len(dataFile[0]))


### need to get transpose of dataFile(in each sublist,all elements mean a particular explanatory variate
### like listPrice, age.....)

temp = dataFile #### make a copy for current dataFile
###print(temp)
dataFile = [list(x) for x in zip(*dataFile)]

##print(ResponseVar)


#####################################################


### y is a list(response variate),x is a list of list(explanatory variates)
###  this funciton can builf the linear regerssion model and show all data
###   we need
def regress(y,x):
    ones = np.ones(len(x[0]))
    var = sm.add_constant(np.column_stack((x[0],ones)))
    for i in x[1:]:
        var = sm.add_constant(np.column_stack((i,var)))
    result  = sm.OLS(y,var).fit()
    return result



print("Know we have the a Linear Regression model with 5 explanatory variates")
print (regress(ResponseVar,dataFile).summary())
######################################################3


## Based on summary,x5 is list price ,x4 is size of house,x3 is # of bedrooms ,x2 is
##  number of bathrooms,x1 is age of house.
## 1. Since adjusted R-squared is 0.995 > 0.9, so this is a strong multilinearity for some
##    explanatory variates
## 2. p value of x3(numnber of bedrooms) is  0.617 >> 0.05, so there is no strong linear relationship
##    between sold price and #of bedrooms, we remove it in the second model



temp = update(temp,2) ### temp is consider as the new data file without element "#of bedrooms"
dataFile = [list(x) for x in zip(*temp)]
print("Know we have the updated Linear Regression model with 4 explanatory variates")
print (regress(ResponseVar,dataFile).summary())




#### with given data of house,make the prediction for sold price of given house
def prediction(x1,x2,x3,x4):
    return -8204.316 + 0.9619*x1 + 70.9554*x2 + 2098.7268*x3 + 82.4239*x4
############################################################################################

def main():
    print("Based on our model,the linear relationship between soldPrice and listPrice,size,#of bathroom,age of house is: ")
    print("y = -8204.316 + 0.9619*x1 + 70.9554*x2 + 2098.7268*x3 + 82.4239*x4")
    houseName = raw_input("house name: ")
    listPrice = input("list price: ")
    size = input("size of house: ")
    bathrm = input("number of bathrooms: ")
    age = input("age of house:")
    print("house name:"+ str(houseName)+",list price: "+str(listPrice)+",number of bathrooms: "
          +str(bathrm)+",age of house: "+str(age))
    predictPrice = prediction(float(listPrice),float(size),float(bathrm),float(age))
    print("Based on our model, the predicted sold price is: "+ str(predictPrice))


if __name__== "__main__":
    main()


