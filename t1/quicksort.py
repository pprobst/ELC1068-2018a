# Quicksort in-place
# Referência: https://rosettacode.org/wiki/Sorting_algorithms/Quicksort#Python

def qcksort(array):
    quicksort(array, 0, len(array)-1)

def quicksort(array, ini, fim):
    if fim - ini > 0:
        pivo, esq, dir = array[ini], ini, fim
        while esq <= dir:
            while array[esq] < pivo:
                esq += 1
            while array[dir] > pivo:
                dir -= 1
            if esq <= dir:
                array[esq], array[dir] = array[dir], array[esq]
                esq += 1
                dir -= 1
        quicksort(array, ini, dir)
        quicksort(array, esq, fim)
