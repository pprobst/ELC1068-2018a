import sys
import heapq
from quicksort import qcksort
from string import punctuation

def mergesort_externo(N):
    num_arqs = arqs_ordenados(N) # número de arquivos gerados
    #apaga(arq) # apaga o arquivo original
    merge(num_arqs) # faz o merge dos num_arqs utilizando uma heap queue

    #for i in range(num_arqs):
    # apaga arquivos temporários

# Retorna o número de arquivos de saída ordenados gerados pelo arquivo de
# entrada
def arqs_ordenados(N):
    f_in = open("keatsm.txt", 'r')
    fatia = f_in.read(N)
    ultima_palavra = None
    i = 0

    # grava N bytes nos arquivos de saída, continuando até o fim do arquivo
    # de entrada
    while len(fatia) > 0:
        with open("outfile_{}.txt".format(i), 'w') as f_out:
            if (i != 0):
                fatia = ultima_palavra + fatia
            string_lst = fatia.lower().split()
            qcksort(string_lst)
            ultima_palavra = string_lst.pop()
            string_ordenada = " ".join(string_lst)
            f_out.write(tira_pontuacao(string_ordenada))

        i += 1
        fatia = f_in.read(N+N) # lê mais N bytes a partir do anterior

    f_in.close()
    return i+1

# Junta os arquivos de saída ordenados em um único arquivo final utilizando
# fila de prioridade (ou heap queue)
def merge(num_arqs):
    arquivos = pega_arquivos(num_arqs)
    conteudo = [f.readline().split() for f in arquivos]

    final = open("final.txt", 'w')
    #final.writelines('\n'.join(heapq.merge(*conteudo)))
    final.writelines('\n'.join(kmerge_manual(*conteudo)))

    final.close()

# Versão simplificada de heapq.merge, que recebe uma lista de listas ordenadas
# e junta tudo num único iterável ordenado
def kmerge_manual(*conteudo):
    _heappop, _heapreplace, _StopIteration = heapq.heappop, heapq.heapreplace, StopIteration
    _iter = iter

    h = []
    h_append = h.append

    for itnum, it in enumerate(map(iter, conteudo)):
        try:
            next = it.__next__
            h_append([next(), itnum, next])

        except _StopIteration:
            pass

    heapq.heapify(h) # "heapifica" h

    while True:
        try:
            while True:
                v, itnum, next = s = h[0] # IndexError quando h está vazia
                yield v
                s[0] = next() # StopIteration quando exaustada
                _heapreplace(h, s) # restaura a heap

        except _StopIteration:
            _heappop(h) # remove iterador vazio

        except IndexError:
            return

# Armazena os arquivos de saída abertos (não o conteúdo deles) em uma lista
def pega_arquivos(num_arqs):
    arquivos = []
    for i in range(num_arqs-1):
        arquivos.append(open("outfile_{}.txt".format(i), 'r'))

    return arquivos

# Retira os sinais de pontuação de uma string
def tira_pontuacao(s) :
    return "".join(c for c in s if c not in punctuation)

def main():
    N = 200 # memória comporta N bytes para leitura
    #input_arq = open(str(sys.argv[1]), 'r') # leitura do arquivo de input
    #input_data = input_arq.read() # conteúdo do arquivo de input

    mergesort_externo(N)
    #arqs_ordenados(N)
    #input_arq.close()

if __name__ == '__main__':
    main()

# Referências:
# https://en.wikipedia.org/wiki/Merge_algorithm
# https://en.wikipedia.org/wiki/External_sorting
# https://en.wikipedia.org/wiki/K-way_merge_algorithm
# https://stackoverflow.com/questions/36379360/is-there-a-way-to-simplify-this-n-way-merge-in-python
# https://stackoverflow.com/questions/1001569/python-class-to-merge-sorted-files-how-can-this-be-improved
# https://hg.python.org/cpython/file/default/Lib/heapq.py#l314
# https://www.youtube.com/watch?v=sVGbj1zgvWQ (C)
