import tkinter as tk
import random

from BarDisplay import BarDisplay

class SortVis(tk.Frame):
    def __init__(self, root, width, barDisplayHeight, nItems, algorithms: dict, dataPointsRange, endDelay, **kwargs):
        super().__init__(root, **kwargs)

        self.nItems = nItems
        self.algorithms = algorithms
        self.dataPointsRange = dataPointsRange
        self.endDelay = endDelay

        #random list
        self.randomList = [random.randint(1, self.dataPointsRange) for i in range(self.nItems)]
        
        #bar graph display
        self.barDisplay = BarDisplay(self, barDisplayHeight, width)
        self.barDisplay.pack()
        self.barDisplay.display(self.randomList)
        
        # stop and start buttons
        self.startButton = tk.Button(self, text="Play ▶", command=self.start)
        self.startButton.pack(side=tk.LEFT)

        self.stopButton = tk.Button(self, text="Stop ■", state=tk.DISABLED, command=self.stop)
        self.stopButton.pack(side=tk.LEFT)

        #randomize button
        randomizeButton = tk.Button(self, text="Randomize ♻", command=self.randomize)
        randomizeButton.pack(side=tk.LEFT)

        # algorithm selector
        algoNames = list(algorithms.keys())
        self.selectedAlgoVar = tk.StringVar(value=algoNames[0])

        algoSelector = tk.OptionMenu(self, self.selectedAlgoVar, *algoNames)
        algoSelector.pack(side=tk.RIGHT)

    def start(self):
        self.barDisplay.display(self.randomList)

        algoGenerator = self.algorithms[self.selectedAlgoVar.get()][0]
        self.delay = self.algorithms[self.selectedAlgoVar.get()][1]

        self.stopButton.config(state=tk.NORMAL)
        self.startButton.config(state=tk.DISABLED)

        self.afterID = self.after(
            self.delay, 
            lambda: self.iterate(algoGenerator(self.randomList.copy()))
        )

    def stop(self):
        self.stopButton.config(state=tk.DISABLED)
        self.startButton.config(state=tk.NORMAL)

        try:
            self.after_cancel(self.afterID)
        except:
            pass

        self.barDisplay.display(self.randomList)

    def randomize(self):
        self.stop()
        self.randomList = [random.randint(1, self.dataPointsRange) for i in range(self.nItems)]
        self.barDisplay.display(self.randomList)

    def iterate(self, gen):
        try:
            nextSortStage = next(gen)
            self.barDisplay.display(nextSortStage)
            self.afterID = self.after(self.delay, lambda: self.iterate(gen))

        except StopIteration:
            self.after(self.endDelay, self.stop)