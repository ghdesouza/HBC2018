import csv
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dataset = []

for amostra in range(234):
	dados_arquivo = pd.read_table('../test/%03.d.csv'%amostra, header = -1, sep = ',')
	dados_arquivo = (np.array(dados_arquivo[1:])).T
	tempo = dados_arquivo[3].astype(np.float)

	classes_arquivo = pd.read_table('../train_trip_info.csv', header = -1, sep = ',')
	classes_partida = np.array(classes_arquivo[2][1:]).astype(np.float)
	classes_chegada = np.array(classes_arquivo[3][1:]).astype(np.float)

	posicao = dados_arquivo[0:2].T.astype(np.float)
	deslocamento = []
	deslocamento.append(0)

	for i in range(1, len(posicao)):
		d_x = posicao[i][0]-posicao[i-1][0]
		d_y = posicao[i][1]-posicao[i-1][1]
		d_d = (d_x**2+d_y**2)**0.5
		deslocamento.append(deslocamento[-1]+d_d)
	for i in range(len(deslocamento)):
		deslocamento[i] = deslocamento[i] / deslocamento[-1]
	deslocamento = np.array(deslocamento)

	pos_interpol = []

	quant_interval = 100
	for i in range(quant_interval+1):
		j = 0
		while j < len(deslocamento)-1 and deslocamento[j+1] < i/quant_interval:
			j = j+1
		t_0 = deslocamento[j]
		t_1 = deslocamento[j+1]
		t_p = i/quant_interval
		if t_1 == t_0:
			x_barra = posicao[j][0]
			y_barra = posicao[j][1]
		else:
			x_barra = posicao[j][0]*(1-((t_p-t_0)/(t_1-t_0)))+posicao[j+1][0]*(1-((t_1-t_p)/(t_1-t_0)))
			y_barra = posicao[j][1]*(1-((t_p-t_0)/(t_1-t_0)))+posicao[j+1][1]*(1-((t_1-t_p)/(t_1-t_0)))
		pos_interpol.append([x_barra, y_barra])
	pos_interpol = np.array(pos_interpol)

	dataset.append([])
	for i in range(len(pos_interpol)):
		dataset[-1].append(pos_interpol[i][0]-35)
		dataset[-1].append(pos_interpol[i][1]-136)
	dataset[-1].append(classes_chegada[amostra]+1)

dataset = np.array(dataset)
print(len(dataset))
arq = open('interpolacao_100_test.txt', 'a')
for i in range(len(dataset)):
	arq.write('%lf'%dataset[i][0])
	for j in range(1,len(dataset[i])):
		arq.write('\t%lf'%dataset[i][j])
	arq.write('\n')
arq.close


