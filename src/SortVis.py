import tkinter as tk
import random

from .BarDisplay import BarDisplay

class SortVis(tk.Frame):
    def __init__(self, root, width, barDisplayHeight, nItems, algorithms: dict, dataPointsRange, endDelay, **kwargs):
        super().__init__(root, **kwargs)

        #instance variables
        self.nItems = nItems
        self.algorithms = algorithms
        self.dataPointsRange = dataPointsRange
        self.endDelay = endDelay

        #fetching algo names and current algo
        algoNames = list(self.algorithms.keys())
        self.currentAlgoName = algoNames[0]
        self.nItems = self.algorithms[self.currentAlgoName][2]

        #tkinter variables
        self.selectedAlgoVar = tk.StringVar(value=self.currentAlgoName)
        self.selectedAlgoVar.trace("w", self.onAlgoChange)

        self.delayVar = tk.IntVar(value=self.algorithms[self.currentAlgoName][1])

        self.lengthVar = tk.IntVar(value=self.algorithms[self.currentAlgoName][2])
        self.lengthVar.trace("w", lambda *_: self.randomize())

        #random list
        self.randomList = [random.randint(1, self.dataPointsRange) for i in range(self.lengthVar.get())]
        
        #bar graph display
        self.barDisplay = BarDisplay(self, barDisplayHeight, width)
        self.barDisplay.pack()
        self.barDisplay.display(self.randomList)

        #frame for line of buttons below graph display
        buttonsFrame = tk.Frame(self)
        buttonsFrame.pack(fill=tk.X)
        
        # stop and start buttons
        self.startButton = tk.Button(buttonsFrame, text="Play ▶", command=self.start)
        self.startButton.pack(side=tk.LEFT)

        self.stopButton = tk.Button(buttonsFrame, text="Stop ■", state=tk.DISABLED, command=self.stop)
        self.stopButton.pack(side=tk.LEFT)

        #randomize button
        randomizeButton = tk.Button(buttonsFrame, text="Randomize ♻", command=self.randomize)
        randomizeButton.pack(side=tk.LEFT)

        # algorithm selector
        algoSelector = tk.OptionMenu(buttonsFrame, self.selectedAlgoVar, *algoNames)
        algoSelector.pack(side=tk.RIGHT)

        # list length and delay sliders
        lengthSlider = tk.Scale(self, from_=5, to=125, label="Length of List", 
            orient=tk.HORIZONTAL, variable=self.lengthVar
        )
        delaySlider = tk.Scale(self, from_=1, to_=200, label="Delay (ms)", 
            orient=tk.HORIZONTAL, variable=self.delayVar
        )

        lengthSlider.pack(fill=tk.X)
        delaySlider.pack(fill=tk.X)

    def start(self):
        self.barDisplay.display(self.randomList)

        algoGenerator = self.algorithms[self.selectedAlgoVar.get()][0]

        self.stopButton.config(state=tk.NORMAL)
        self.startButton.config(state=tk.DISABLED)

        self.afterID = self.after(
            self.delayVar.get(), 
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
        self.randomList = [random.randint(1, self.dataPointsRange) for i in range(self.lengthVar.get())]
        self.barDisplay.display(self.randomList)

    def onAlgoChange(self, *_):
        self.currentAlgoName = self.selectedAlgoVar.get()
        self.nItems = self.algorithms[self.currentAlgoName][2]

        self.delayVar.set( self.algorithms[self.currentAlgoName][1] )
        self.lengthVar.set( self.algorithms[self.currentAlgoName][2] )

        self.randomize()

    def iterate(self, gen):
        try:
            nextSortStage = next(gen)
            self.barDisplay.display(nextSortStage)
            self.afterID = self.after(self.delayVar.get(), lambda: self.iterate(gen))

        except StopIteration:
            self.after(self.endDelay, self.stop)