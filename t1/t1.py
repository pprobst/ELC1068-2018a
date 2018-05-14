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
    deleta_arquivos("out") # remove os arquivos de saída temporários
    print("Fim!")

# Retorna o número de arquivos de saída ordenados gerados pelo arquivo de entrada
def arqs_ordenados(N, nome_arq):
    i = 0
    # grava N bytes nos arquivos de saída, continuando até o fim do arquivo
    # de entrada
    with open(nome_arq, 'r') as f_in:
        for fatia in ler_em_fatias(f_in, N):
            with open("outfile_{}.txt".format(i), 'w') as f_out:
                fatia = tira_pontuacao(fatia)
                fatia = fatia.lower().split()
                qcksort(fatia)  # quicksort é um tanto lento!
                #fatia.sort() # timsort; mais rápido!
                fatia = '\n'.join(fatia)
                f_out.write(fatia)
            i += 1

    return i+1

# Lê o arquivo f N a N bytes ("fatia")
def ler_em_fatias(f, N):
    while True:
        fatia = f.read(N)
        if not fatia:
            break
        yield fatia

# Junta os arquivos de saída ordenados em um único arquivo final utilizando
# heap queue
def merge(num_arqs):
    arquivos = pega_filenames(num_arqs)

    with ExitStack() as stack, open('final.txt', 'w') as final:
        arquivos = [stack.enter_context(open(arq)) for arq in arquivos]
        final.writelines(hmerge_manual(*arquivos))

# Versão simplificada de heapq.merge(), que recebe iteráveis ordenados e junta tudo
# num único iterador sobre os valores ordenados
def hmerge_manual(*arquivos):
    h = []

    for itnum, it in enumerate(map(iter, arquivos)):
        # itnum -> número da iteração
        # it -> arquivo
        # next -> próximo arquivo
        # next() -> primeiro elemento de cada arquivo
        try:
            next = it.__next__
            h.append([next(), itnum, next])

        except StopIteration:
            pass

    heapq.heapify(h) # "heapifica" hi

    while True:
        try:
            while True:
                v, itnum, next = s = h[0] # h[0] -> menor valor da heap
                if v[-1] != '\n':
                    yield v + '\n'
                else:
                    yield v # cada yield retorna o menor valor
                s[0] = next() # StopIteration quando exaustada
                heapq.heapreplace(h, s) # restaura a heap com o próximo elem

        except StopIteration:
            heapq.heappop(h) # remove iterador vazio

        except IndexError:
            return

# Armazena os nomes dos arquivos temporários numa lista
def pega_filenames(num_arqs):
    arquivos = []
    for i in range(num_arqs-1):
        arquivos.append("outfile_{}.txt".format(i))

    return arquivos

# Deleta os arquivos temporários
def deleta_arquivos(prefixo):
    for item in os.listdir():
        if item.startswith(prefixo):
            os.remove(item)

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
# http://code.activestate.com/recipes/491285/
# https://stackoverflow.com/questions/36379360/is-there-a-way-to-simplify-this-n-way-merge-in-python
# https://stackoverflow.com/questions/1001569/python-class-to-merge-sorted-files-how-can-this-be-improved
# https://hg.python.org/cpython/file/default/Lib/heapq.py#l314
# https://www.youtube.com/watch?v=sVGbj1zgvWQ (C)
