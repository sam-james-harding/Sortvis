import random

#each algorithm should be a generator, taking in a list and yielding each stage of its sorting
def bubbleSort(l: list):
    while True:
        nSwaps = 0
        for i in range( len(l) - 1 ):
            if l[i] > l[i+1]:
                l[i], l[i+1] = l[i+1], l[i]
                nSwaps += 1
                yield l
        
        if nSwaps == 0: break

def bogoSort(l: list):
    def isSorted(lst):
        for i in range(len(lst)-1):
            if lst[i] > lst[i+1]:
                return False
        return True

    while not isSorted(l):
        random.shuffle(l)
        yield l

def selectionSort(l: list):
    sorted = []

    for i in range(len(l)):
        minimum = min(l)
        sorted.append(minimum)
        l.remove(minimum)
        yield (sorted + l)

def insertionSort(l: list):
    sorted = []

    while len(l) > 0:
        firstItem = l.pop(0)
        
        if len(sorted) == 0:
            sorted.append(firstItem)
        else:
            i = len(sorted) - 1
            while i >= 0 and sorted[i] > firstItem: i -= 1
            sorted.insert(i+1, firstItem)
        
        yield (sorted + l)

#dictionary of {name: (generator, delay)}
SORTS = {
    "Bubble Sort": (bubbleSort, 10),
    "Bogo Sort": (bogoSort, 1),
    "Selection Sort": (selectionSort, 100),
    "Insertion Sort": (insertionSort, 100)
}