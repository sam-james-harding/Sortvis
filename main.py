import tkinter as tk

from SortVis import SortVis
from SortingAlgorithms import SORTS

root = tk.Tk()
root.title("Sorting Algorithm Visualizer")

visualiser = SortVis(root, width=500, barDisplayHeight=200, nItems=50, algorithms=SORTS, dataPointsRange=100, endDelay=1000)
visualiser.pack()

root.mainloop()