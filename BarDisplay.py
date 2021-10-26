import tkinter as tk
from typing import List

class BarDisplay(tk.Frame):
    def __init__(self, root, height, width, **kwargs):
        super().__init__(root, **kwargs)

        #variables
        self.height = height
        self.width = width

        #canvas object setup
        canvasLabelFrame = tk.LabelFrame(self, text="Algorithm Display")
        self.canvas = tk.Canvas(canvasLabelFrame, height=height, width=width+1)
        canvasLabelFrame.pack()
        self.canvas.pack()

        #canvas graphics setup
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    def display(self, barGraphData: List[float]):
        self.canvas.delete('all') #clear all old items on canvas

        maxDP = max(barGraphData)
        nItems = len(barGraphData)
        itemWidth = self.width // nItems

        for idx, dataPoint in enumerate(barGraphData):
            displayHeight = int( (dataPoint/maxDP) * self.height )

            startX = idx * itemWidth
            endX = startX + itemWidth

            startY = self.height - displayHeight
            endY = self.height

            self.canvas.create_rectangle(startX, startY, endX, endY)
