import sys
import heapq
from string import punctuation

def mergesort_externo(N):
    num_arqs = arqs_ordenados(N) # número de arquivos gerados
    k = int(N / (num_arqs+1)); # tamanho dos buffers (1 de saída, k de entrada)
    #apaga(arq) # apaga o arquivo original
    merge(num_arqs, k) # faz o merge dos num_arqs com k elementos

    #for i in range(num_arq):
    # apaga arquivos temporários

def arqs_ordenados(N):
    f_in = open("keatsm.txt", 'r')
    fatia = f_in.read(N)
    ultima_palavra = None
    i = 0

    # Grava N bytes nos arquivos de output, continuando até o fim do arquivo
    # de input
    while len(fatia) > 0:
        with open("outfile_{}.txt".format(i), 'w') as f_out:
            if (i != 0):
                fatia = ultima_palavra + fatia
            stringzinha = fatia.lower().split()
            ultima_palavra = stringzinha.pop()
            string_ordenada = " ".join(sorted(stringzinha))
            f_out.write(tira_pontuacao(string_ordenada))

        i += 1
        fatia = f_in.read(N+N) # lê mais N bytes a partir do anterior

    f_in.close()
    return i+1

# Junta os arquivos de saída ordenados em um único arquivo final utilizando
# fila de prioridade (ou heap queue)
def merge(num_arqs, k):
    # não funciona
    final = heapq.merge(pega_arquivos(num_arqs))
    for elemento in final:
        print(str(elemento))
     # with open("final.txt", 'w', k) as arq_final:
     #   for elemento in final:
     #       arq_final.writelines(elemento)

# Armazena os arquivos de saída abertos em uma lista
def pega_arquivos(num_arqs):
    arquivos = []
    for i in range(num_arqs-1):
        arquivos.append(open("outfile_{}.txt".format(i), 'r'))

    return arquivos

# Tira os sinais de pontuação de uma string
def tira_pontuacao(s) :
    return "".join(c for c in s if c not in punctuation)

N = 200 # memória comporta N registros de dados
#input_arq = open(str(sys.argv[1]), 'r') # leitura do arquivo de input
#input_data = input_arq.read() # conteúdo do arquivo de input

mergesort_externo(N)
#arqs_ordenados(N)
#input_arq.close()
