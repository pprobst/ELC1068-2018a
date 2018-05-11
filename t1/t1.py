import sys
import os
import heapq
from contextlib import ExitStack
from quicksort import qcksort
from string import punctuation

# Reúne todos os passos para realizar o mergesort externo
def mergesort_externo(N, nome_arq):
    num_arqs = arqs_ordenados(N, nome_arq) # número de arquivos gerados
    merge(num_arqs) # faz o merge dos num_arqs utilizando uma heap queue

    # remove arquivos de saída temporários
    for item in os.listdir():
        if item.startswith("out"):
            os.remove(item)

    print("Fim!")

# Retorna o número de arquivos de saída ordenados gerados pelo arquivo de entrada
def arqs_ordenados(N, nome_arq):
    f_in = open(nome_arq, 'r')
    fatia = f_in.read(N)
    ultima_palavra = None
    i = 0

    # grava N bytes nos arquivos de saída, continuando até o fim do arquivo
    # de entrada
    while len(fatia) > 0:
        with open("outfile_{}.txt".format(i), 'w') as f_out:
            #if (i != 0):
            #    fatia = ultima_palavra + fatia
            fatia = tira_pontuacao(fatia)
            string_lst = fatia.lower().split()
            qcksort(string_lst)
            #ultima_palavra = string_lst.pop()
            string_ordenada = '\n'.join(string_lst)
            #f_out.write(tira_pontuacao(string_ordenada))
            f_out.write(string_ordenada)

        i += 1
        fatia = f_in.read(N+N) # lê mais N bytes a partir do anterior

    f_in.close()
    return i+1

# Junta os arquivos de saída ordenados em um único arquivo final utilizando
# fila de prioridade (heap queue)
def merge(num_arqs):
    arquivos = pega_filenames(num_arqs)

    with ExitStack() as stack, open('final.txt', 'w') as final:
        arquivos = [stack.enter_context(open(arq)) for arq in arquivos]
        final.writelines(kmerge_manual(*arquivos))
        #for line in heapq.merge(*arquivos):
        #    final.write(line)

# Versão simplificada de heapq.merge, que recebe iteráveis ordenados e junta tudo
# num único iterador sobre os valores ordenados
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

# Armazena os nomes dos arquivos temporários numa lista
def pega_filenames(num_arqs):
    arquivos = []
    for i in range(num_arqs-1):
        arquivos.append("outfile_{}.txt".format(i))

    return arquivos

# Retira os sinais de pontuação de uma string
def tira_pontuacao(s) :
    return "".join(c for c in s if c not in punctuation)

def main():
    try:
        nome_arq = sys.argv[1]
    except IndexError:
        print("Insira o nome do arquivo de entrada como argumento!\n" +
              "ex.: python t1.py nome_do_arquivo.txt")
        sys.exit()

    N = int(input("Insira os N bytes de leitura suportados em memória: "))

    mergesort_externo(N, nome_arq)

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
