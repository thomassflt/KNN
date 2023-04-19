#Full path
f1 = open(r"/Users/thomas/Library/CloudStorage/OneDrive-DeVinci/ESILV/A3/S6/Data et IA/SOUFFLETthomas-VARACCAmaxime-TDi.txt","r")
#Relative path
f2 = open(r"/Users/thomas/Downloads/PlaideauAnna-BenfetitaIlyana-TDQ.txt","r")

linesf1 = f1.readlines()
linesf2 = f2.readlines()

#print(len(linesf1))
#print(len(linesf2))

sameLength = True if len(linesf1) == len(linesf2) else False

if sameLength:
    similaire = 0
    for i in range(len(linesf1)):
        if linesf1[i] == linesf2[i]:
            similaire +=1
    
    print("Le taux de similitude est de : ", similaire/len(linesf1)*100, "%" )
    print(4000-similaire, "erreurs")
else:
    print("Les fichiers ne sont pas de la même taille")