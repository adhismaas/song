from sklearn import svm
from scipy import spatial
from os import listdir
import os
import pandas as pd
import numpy as np



lagu = listdir('data_train/')
# lagu = [for x in lagu]
# lagu = [x.split(".") for x in lagu]
# for i in range(len(lagu)):
# 	lagu[i][0] = int(lagu[i][0])
# for x in lagu :
# 	x = x.split('.')
lagu = sorted(lagu, key=lambda x: float(x.split()[0]))
# print(lagu)
ekspresi = [10.0, 10.0, 2.0, 10.0, 10.0, 10.0, 10.0]
# ekspresi = [10-x for x in ekspresi]
print(ekspresi)
recommend = []
data = pd.read_csv("musicData.csv")
data = data.fillna(0)
# print(data)

dataCentro = data.groupby(['Id']).mean()
dataDeviation = data.groupby(['Id']).std().mul(0.1)

# dataDeviation = dataDeviation.loc[:,'Id'] *= 0.1

# print(dataCentro)
dataDeviation = dataDeviation.std(axis=1)
# dataDeviation['Senang', 'Sedih'] *= 0.1
# print(dataDeviation)

dataCentro = dataCentro.values.tolist()
dataDeviation = dataDeviation.values.tolist()

print(dataDeviation)
# print(dataCentro[15])

for i in range(len(dataCentro)):
	temp = spatial.distance.cosine(ekspresi, dataCentro[i])
	# print(temp)
	# temp = temp*10
	if temp < dataDeviation[i] :
		# print(temp)
		print(str(i) + ' ' + str(temp))
		recommend.append([i+1,temp,lagu[i]])
		# print(recommend[i])

recommend = sorted(recommend, key=lambda x: x[1])
for x in recommend:
	print(*x)
# print(recommend)