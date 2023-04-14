# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:21:18 2023

@author: thoma
"""

import numpy as np
import pandas as pd

def distance(xtest,sl,sw,pl,pw):
    pointa= np.array((sl,sw,pl,pw))
    return np.linalg.norm(xtest-pointa)


def knn(xtest,k):
    distances=[]
    df=pd.read_csv(r"IA3-ml_data_iris.txt", names=["sl","sw","pl","pw","label"])
    for index, row in df.iterrows():
        dist = distance(xtest, row['sl'], row['sw'],row['pl'], row['pw'])
        distances.append((dist,row['label']))
    distances.sort()
    
    result={0:0, 1:0, 2:0}
    for i in range(k):
        tupl=distances[i]
        if(tupl[1] == "Iris-setosa"):
            result[0] = result[0]+1
        elif(tupl[1] == "Iris-versicolor"):
            result[1] = result[1]+1
        else:
            result[2] = result[2]+1
    
    plante,valeur = max(result.items(), key=lambda x: x[1])
    
    if(plante==0):
        print("La plante associée à vos données est une Iris-setosa")
    elif(plante==1):
        print("La plante associée à vos données est une Iris-versicolor")
    else:
        print("La plante associée à vos données est une Iris-virginica")

    
    
    
def main():
    xtest = np.array(((5.1,3.5,1.4,0.2)))
    k = int(input("Entrez une valeur de k : "))
    knn(xtest,k)
    
    
if __name__ == "__main__":
    main()