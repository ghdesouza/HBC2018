#include <stdio.h>
#include <stdlib.h>

typedef struct{
	int tam_entrada;
	int quant_amostra;
	
	double **dataset;
}
DATASET;

void DATASET_Carrega(char nome_arquivo[], DATASET* data, int tam_entrada, int quant_amostra){
	int i, j;
		
	data->tam_entrada = tam_entrada;
	data->quant_amostra = ((int)(quant_amostra));
	
	data->dataset = (double**) malloc(data->quant_amostra*sizeof(double*));
	for(i = 0; i < data->quant_amostra; i++) data->dataset[i] = (double*) malloc((data->tam_entrada+1)*sizeof(double));
	
	FILE* arq;
	arq = fopen(nome_arquivo, "r");
	double lixo;
	if(arq != NULL){
		for(i = 0; i < quant_amostra; i++){
			for(j = 0; j <= data->tam_entrada; j++) fscanf(arq, "%lf", &data->dataset[i][j]);
		}
		fclose(arq);
		
	}
}

void DATASET_Destrutor(DATASET *data){
	int i;
	
	for(i = 0; i < data->quant_amostra; i++){
		free(data->dataset[i]);
	}	free(data->dataset);
	
}

int main(){
	
	srand(1);

	char nome_dataset[];
	char nome_file[];
	int quant_amostras;
	
	int train = 1;

	if(train){
		char nome_dataset[] = "train_corte_pond_100_chegada.txt";
		char nome_file[] = "dist_11x8_train_cheg.txt";
		quant_amostras = 1071952;
	}else{
		char nome_dataset[] = "test_pond_100.txt";
		char nome_file[] = "dist_11x8_test.txt";
		quant_amostras = 234;
	}

	float locais[9][2] = {{35.156181, 136.923974},
						  {35.156463, 136.926576},
						  {35.156785, 136.925529},
						  {35.156993, 136.924575},
						  {35.157258, 136.926753},
						  {35.157480, 136.925406},
						  {35.157598, 136.926138},
						  {35.157641, 136.926592},
						  {35.157974, 136.924739}};
	
	int tam_entrada = 22;
	
	DATASET *data = (DATASET*) malloc(sizeof(DATASET));
	
	printf("creating the dataset\n");
	
	DATASET_Carrega(nome_dataset, data, tam_entrada, quant_amostras);
	
	int i, j, k;
	double **data_nova = (double**) malloc((quant_amostras)*sizeof(double*));
	for(i = 0; i < (quant_amostras); i++) data_nova[i] = (double*) malloc(89*sizeof(double));
	
	double xl, yl;
	for(i = 0; i < quant_amostras; i++){
		for(j = 0; j < 11; j++){
			for(k = 0; k < 8; k++){
				xl = (data->dataset[i][2*j]) - (locais[k][0]-35.0);
				yl = (data->dataset[i][2*j+1]) - (locais[k][1]-136.0); 
				data_nova[i][j*8+k] = sqrt(((xl*xl)+(yl*yl)));
				
			}
		}
		data_nova[i][89] = data->dataset[i][data->tam_entrada];
	}
	
	FILE *arq = fopen(nome_file, "w");
	for(i = 0; i < (quant_amostras); i++){
		for(j = 0; j < 89; j++){
			fprintf(arq, "%lf\t", data_nova[i][j]);
		}
		fprintf(arq, "%lf\n", data_nova[i][89]);
	}
	fclose(arq);
	
	for(i = 0; i < (quant_amostras); i++){
		free(data_nova[i]);
	}	free(data_nova);
	
	DATASET_Destrutor(data);
	free(data);
	
	return 0;
	
}

