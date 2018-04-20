import sys

def mergesort_externo(arq, N):
    num_arqs = arqs_ordenados(arq) # número de arquivos gerados
    k = N / (num_arqs+1); # tamanho dos buffers (1 de saída, k de entrada)
    #apaga(arq) # apaga o arquivo original
    merge(arq, num_arqs, k) # faz o merge dos num_arqs com k elementos

    #for i in range(num_arq):
    # apaga arquivos temporários

def arqs_ordenados(N):
    inpt = None
    with open("keatsm.txt" , 'r') as f:
        inpt = f.read()

    i = 0
    in_slice = inpt[:N]
    # Grava N bytes nos arquivos de output, continuando até o fim do arquivo
    # de input
    while len(in_slice) > 0:
        with open("outfile_{}.txt".format(i), 'w') as f:
            f.write(''.join(sorted(in_slice)))

        i += 1
        in_slice = inpt[i*N:i*N + N]

N = 100 # RAM comporta N registros de dados
#input_arq = open(str(sys.argv[1]), 'r') # leitura do arquivo de input
#input_data = input_arq.read() # conteúdo do arquivo de input

#mergesort_externo(input_file, 4)
arqs_ordenados(N)
#input_arq.close()

# Referência para o algoritmo: https://www.youtube.com/watch?v=sVGbj1zgvWQ
