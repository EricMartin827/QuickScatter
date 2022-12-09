import openpyxl
import random
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
import functools
from scipy.stats import pearsonr

def compare(x1, x2):
    if x1[0] **2 + x1[1]**2 > x2[0]**2 + x2[1]**2:
        return 1
    elif x1[0] **2 + x1[1]**2 == x2[0]**2 + x2[1]**2:
        return 0
    else:
        return -1

def bootstrapSampling():
    df = pd.read_excel("heightWeightChart.xlsx")
    #print(df)
    corr, _ = pearsonr(df.loc[:, "Height(Inches)"], df.loc[:, "Weight(Pounds)"])
    print("Dataset's correlation coefficient: ")
    print(corr)

    numSamples = 35
    sampSize = 40
    i = 0
    
    myList = []

    print("Starting loop")
    while i < numSamples:

        randSample = df.sample(sampSize)
        j = list(randSample[['Height(Inches)', 'Weight(Pounds)']].itertuples(index=False, name = None))
        j.sort(key = functools.cmp_to_key(compare))
        myList.append(j)

        i += 1

    print("End of loop")
    myArr = np.array(myList)
    avg = myArr.mean(axis = 0)
    plt.scatter(avg[:, 0], avg[:, 1])
    plt.show()

    newCorr, _ = pearsonr(avg[:, 0], avg[:, 1])
    print("Average Bootstrap-Sampled Correlation Coefficient: ")
    print(newCorr)
    


bootstrapSampling()


    
