# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:21:18 2023

@author: thoma
"""

import numpy as np
import pandas as pd
import sys

#Calcule la distance entre le point de test et un point d'entrainement de coordonnées (a,b,c,d,e,f,g)
def distance(dataTest,a,b,c,d,e,f,g):
    pointa= np.array((a,b,c,d,e,f,g))
    return np.linalg.norm(dataTest-pointa)

#Calcule la distance normalisée entre le point de test et un point d'entrainement de coordonnées (a,b,c,d,e,f,g)
def distanceNormalisee(dataTest,a,b,c,d,e,f,g):
    #print("dataTest : ", dataTest)
    #print("a,b,c,d,e,f,g : ", a,b,c,d,e,f,g)
    pointa= np.array((a,b,c,d,e,f,g))
    return (np.linalg.norm(dataTest-pointa)-np.mean(dataTest-pointa))/np.std(dataTest-pointa)


def knn(dataTest,k,fdest,df_train):
    #initialise la liste des distances
    distances=[]

    #Parcourt le dataframe d'entrainement et calcule la distance entre le point de test et chaque point d'entrainement
    for index, row in df_train.iterrows():
        dist = distance(dataTest, row['a'], row['b'],row['c'], row['d'], row['e'], row['f'], row['g'])
        #dist = distanceNormalisee(dataTest, row['a'], row['b'],row['c'], row['d'], row['e'], row['f'], row['g'])
        distances.append((dist,row['label']))
    #Trie la liste des distances
    distances.sort()
    
    #initialise le dictionnaire de résultat en fonction du nombre de labels
    result={i:0 for i in range(len(df_train['label'].unique()))}
    
    #Parcourt les k premiers éléments de la liste distances et incrémente le dictionnaire de résultat
    for i in range(int(k)):
        tupl=distances[i]
        #ajoute 1 au label correspondant dans le dictionnaire de résultat
        result[tupl[1]]+=1
    
    #Calcul du label le plus présent dans le dictionnaire de résultat
    label = max(result, key=lambda k: result[k])
    

    
    #Ecris le label dans le fichier de résultat
    fdest.write(str(label)+'\n')

#Fonction utilisé lorsque un seul fichier de données est fourni. Il sera divisé en deux : 80% pour l'entrainement et 20% pour le test
#Nous pouvons donc calculer la précision des résultats
def main_data_divisied(df,fdest,k):  
        #Mélange les données
        df = df.sample(frac=1).reset_index(drop=True)
        
        #Prend 80% des données pour l'entrainement
        df_train = df.iloc[:int(len(df)*0.8)]
        
        #Prend 20% des données pour le test
        df_try = df.iloc[int(len(df)*0.8):]
        
        for index, row in df_try.iterrows():
            dataTest = np.array((row['a'], row['b'],row['c'], row['d'], row['e'], row['f'], row['g']))
            knn(dataTest,k,fdest, df_train)

        fdest.close()

        #Calcul de la précision des résultats stockés dans SOUFFLETthomas-VARACCAmaxime-TDi.txt en fonction du label donné dans df_try et de la matrice de confusion
        f = open(r"SOUFFLETthomas-VARACCAmaxime-TDi.txt","r")
        lines = f.readlines()
        matrice = np.zeros((len(df_train['label'].unique()),len(df_train['label'].unique())))
        indexLines = 0
        count = 0
        for index, row in df_try.iterrows():
            if indexLines < len(lines):
                if int(lines[indexLines]) == row['label']:
                    count+=1
                matrice[int(lines[indexLines])][int(row['label'])]+=1
                indexLines+=1
        f.close()
        print("Précision : ", count/len(df_try))
        print("Matrice de confusion : ")
        print(matrice)  

def main():
    #Ouvre le fichier dans lequel on va stocker les résultats
    fdest=open(r"SOUFFLETthomas-VARACCAmaxime-TDi.txt","w")
    
    #Récupère le nombre de voisins k voulu
    #Le k le plus optimal est 5
    k = input("Enter the k that you want :")


    df_train=pd.read_csv("KNN/data.txt", names=["a","b","c","d","e","f","g","label"], sep=";")
    df_try=pd.read_csv("KNN/finalTest.txt", names=["a","b","c","d","e","f","g"], sep=";")
    for index, row in df_try.iterrows():
            dataTest = np.array((row['a'], row['b'],row['c'], row['d'], row['e'], row['f'], row['g']))
            knn(dataTest,k,fdest,df_train)
    fdest.close()
    
    """
    Cette partie du code permettait de tester le programme avec des données fournies par l'utilisateur rentrées en argument dans la console
    Par exemple, python3 KNN.py data.txt preTest.txt pour prendre data.txt pour l'entrainement et preTest.txt pour le test
    Elle n'est plus réellement utile pour le code final qui prend data.txt et finalTest.txt
    
    #Si le nombre d'arguments est égal à 3, alors on prend les données de test et les données d'entrainement
    if len(sys.argv) == 3:
        df_train=pd.read_csv(sys.argv[1], names=["a","b","c","d","e","f","g","label"], sep=";")
        df_try=pd.read_csv(sys.argv[2], names=["a","b","c","d","e","f","g","label"], sep=";")
        for index, row in df_try.iterrows():
            dataTest = np.array((row['a'], row['b'],row['c'], row['d'], row['e'], row['f'], row['g']))
            knn(dataTest,k,fdest,df_train)
        fdest.close()
        
    #Si le nombre d'arguments est égal à 2, alors on divise les données fournies en 80% pour l'entrainement et 20% pour le test
    elif len(sys.argv) == 2:
        df=pd.read_csv(sys.argv[1], names=["a","b","c","d","e","f","g","label"], sep=";")
        main_data_divisied(df,fdest,k)
        
    #Si rien n'est donnée en argument, on prend les données data.txt (simplifie les tests du code sans avoir à changer les arguments) 
    else: 
        df=pd.read_csv(r"data.txt", names=["a","b","c","d","e","f","g","label"], sep=";")
        
        #Permet en entrant aucune valeur de k de tester pour k allant de 1 à 9 pour voir lequel donne le meilleur résultat
        if k == "":
            for k in range(1,10):
                df=pd.read_csv(r"data.txt", names=["a","b","c","d","e","f","g","label"], sep=";")
                print("k = ", k)
                main_data_divisied(df,fdest,k)
                fdest=open(r"SOUFFLETthomas-VARACCAmaxime-TDi.txt","w")

        else:
            main_data_divisied(df,fdest,k)
    """

if __name__ == "__main__":
    main()