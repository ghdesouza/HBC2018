import csv
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

arq = open('train_corte_peso_100.txt', 'a')

for amostra in range(263):
	dados_arquivo = pd.read_table('../train/%03.d.csv'%amostra, header = -1, sep = ',')
	dados_arquivo = (np.array(dados_arquivo[1:])).T
	tempo = dados_arquivo[3].astype(np.float)

	classes_arquivo = pd.read_table('../train_trip_info.csv', header = -1, sep = ',')
	classes_partida = np.array(classes_arquivo[2][1:]).astype(np.float)
	classes_chegada = np.array(classes_arquivo[3][1:]).astype(np.float)

	for corte_inicio in range(len(tempo)):
		for corte_fim in range(1, len(tempo)):
			if tempo[corte_inicio] < 45 and tempo[-1]-tempo[-corte_fim] < 45:

				posicao = dados_arquivo[0:2, corte_inicio:-corte_fim].T.astype(np.float)
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

				for c1 in range(corte_inicio+corte_fim):
					temp = pos_interpol[0][0]-35
					arq.write('%lf'%temp)
					temp = pos_interpol[0][1]-136
					arq.write('\t%lf'%temp)
					for i in range(1, len(pos_interpol)):
						temp = pos_interpol[i][0]-35
						arq.write('\t%lf'%temp)
						temp = pos_interpol[i][1]-136
						arq.write('\t%lf'%temp)
					temp = classes_partida[amostra]+1
					arq.write('\t%lf\n'%temp)

arq.close





