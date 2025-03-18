from cmath import e
from tkinter import *
from tkinter import ttk
import tkinter.font as font
import random
import numpy as np
from threading import Thread
import time
from sortingAlgorithms import bubbleSort, insertionSort, selectionSort, mergeSort, resetGlobals

class SortingVisualizer:
    def __init__(self):
        self.root = Tk()
        self.root.title('Visualized Sorting Algorithms')
        self.root.maxsize(1600, 1600)
        self.root.config(bg='#272643')
        
        self.waiting_for_step = False
        self.sorting_paused = False
        self.sorting_active = False
        
        self.setup_ui()
        
    def setup_ui(self):
        self.myFont = font.Font(family="Open Sans", size=10)
        self.myFontBold = font.Font(family="Open Sans", size=10, weight="bold")
        self.titleFont = font.Font(family="Fira Code", size=15, weight="bold")
        
        self.algType = StringVar()
        self.data = []
        self.dataHolder = np.array([])
        self.fastMode = IntVar()
        
        # Frame and Canvas Setup
        self.myFrame = Frame(self.root, width=300, height=650, bg='#272643', bd=0)
        self.myFrame.grid(row=0, column=0, padx=0, pady=0)
        self.myCanvas = Canvas(self.root, width=1000, height=600, bg='#e2fbfa', relief=GROOVE, bd=4)
        self.myCanvas.grid(row=0, column=2, padx=20, pady=20)
        
        # Title Section
        titlebox = Canvas(self.myFrame, width=270, height=150, bg='#272643', relief=GROOVE, 
                         bd=4, highlightbackground='#7674b6')
        titlebox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=E)
        
        Label(self.myFrame, text="Sorting\nVisualizer", bg='#272643', fg='white', 
              font=self.titleFont, width=19).grid(row=0, column=0, columnspan=2, padx=5, pady=70, sticky=N)
        
        # Algorithm Selection
        Label(self.myFrame, text="Selected Algorithm: ", bg='#272643', fg='white', 
              font=self.myFont).grid(row=2, column=0, padx=5, pady=0, sticky=W)
        self.algMenu = ttk.Combobox(self.myFrame, textvariable=self.algType, font=self.myFont,
                                   values=['Bubble Sort', 'Merge Sort', 'Selection Sort', 'Insertion Sort'])
        self.algMenu.grid(row=2, column=1, padx=0, pady=0)
        self.algMenu.current(0)
        
        # Data Size Entry
        Label(self.myFrame, text="Data Size: ", bg='#272643', fg='white', font=self.myFont,
              width=10).grid(row=4, column=0, padx=5, pady=10, sticky=E)
        self.sizeEntry = Entry(self.myFrame)
        self.sizeEntry.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=E)
        
        # Min/Max Entries
        Label(self.myFrame, text="Minimum: ", bg='#272643', fg='white', font=self.myFont,
              width=10).grid(row=5, column=0, padx=5, pady=10, sticky=E)
        self.minEntry = Entry(self.myFrame)
        self.minEntry.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky=E)
        
        Label(self.myFrame, text="Maximum: ", bg='#272643', fg='white', font=self.myFont,
              width=10).grid(row=6, column=0, padx=5, pady=10, sticky=E)
        self.maxEntry = Entry(self.myFrame)
        self.maxEntry.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=E)
        
        # Buttons
        self.genButton = Button(self.myFrame, text="Generate Data", command=self.generate,
                              bg='#bae8e8', font=self.myFont, bd=0)
        self.genButton.grid(row=7, column=0, columnspan=2, padx=20, pady=10)
        
        self.sortButton = Button(self.myFrame, text="Sort", command=self.begin_sort,
                               bg='#93f1b7', font=self.myFontBold, bd=0)
        self.sortButton.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
        
        self.nextStepButton = Button(self.myFrame, text="Next Step", command=self.next_step,
                                   bg='#93f1b7', font=self.myFontBold, bd=0, state=DISABLED)
        self.nextStepButton.grid(row=10, column=0, columnspan=2, padx=5, pady=5)
        
        self.resetButton = Button(self.myFrame, text="Reset", command=self.reset_data,
                                bg='#adbcfb', font=self.myFont, bd=0)
        self.resetButton.grid(row=11, column=1, padx=5, pady=10, sticky=E)
        
        # Fast Mode Checkbox
        Checkbutton(self.myFrame, text="Fast Mode", variable=self.fastMode, font=self.myFont,
                   bg='#adbcfb', onvalue=1, offvalue=0, bd=0).grid(row=11, column=0, padx=10, pady=10, sticky=W)
    
    def draw(self, data, currentColor):
        self.myCanvas.delete("all")
        canvasHeight = 600
        canvasWidth = 1000
        dataSize = len(data)
        barHeight = canvasHeight / (dataSize + 1)
        offset = 11
        barSpacing = round(1/dataSize)
        scaledData = 1/(max(data)) * np.array(data)
        fontSize = round((1/dataSize)*150) + 5
        barFont = font.Font(family="Fira Code", size=fontSize)
        showFont = dataSize-1 <= 50
        
        for i, dataVal in enumerate(scaledData):
            topx = 0
            topy = (i*barHeight) + offset + barSpacing
            botx = canvasWidth - (canvasWidth-dataVal*900)
            boty = (i+1)*barHeight + offset
            self.myCanvas.create_rectangle(topx, topy, botx, boty, fill=currentColor[i], outline="")
            if showFont:
                self.myCanvas.create_text(botx-2, boty-(barHeight/2), anchor=E,
                                        text=str(data[i]), font=barFont, fill='white')
        self.root.update_idletasks()
    
    def entry_verification(self):
        try:
            maximum = int(self.maxEntry.get())
        except:
            maximum = 10
            self.maxEntry.delete(0, "end")
            self.maxEntry.insert(0, "10")
            
        try:
            minimum = int(self.minEntry.get())
        except:
            minimum = 0
            self.minEntry.delete(0, "end")
            self.minEntry.insert(0, "0")
            
        try:
            size = int(self.sizeEntry.get())
        except:
            size = 5
            self.sizeEntry.delete(0, "end")
            self.sizeEntry.insert(0, "5")
            
        if minimum < 0 or minimum >= maximum:
            minimum = 0
            self.minEntry.delete(0, "end")
            self.minEntry.insert(0, "0")
            
        if maximum <= 0 or maximum <= minimum:
            maximum = 10
            self.maxEntry.delete(0, "end")
            self.maxEntry.insert(0, "10")
            
        if size < 0 or size > 100:
            self.sizeEntry.delete(0, "end")
            self.sizeEntry.insert(0, "5")
            size = 5
            
        return minimum, maximum, size
    
    def generate(self):
        minimum, maximum, size = self.entry_verification()
        self.data = []
        for i in range(size):
            self.data.append(random.randint(minimum, maximum))
        self.dataHolder = np.copy(self.data)
        self.draw(self.data, self.color_alternator())
    
    def color_alternator(self):
        dataSize = len(self.data)
        lightenBar = True
        colorArray = []
        for i in range(dataSize):
            if lightenBar:
                colorArray.append('#6967a1')
                lightenBar = False
            else:
                colorArray.append('#545283')
                lightenBar = True
        return colorArray
    
    def next_step(self):
        if self.waiting_for_step:
            self.sorting_paused = False
            self.waiting_for_step = False
    
    def wait_for_step(self):
        self.waiting_for_step = True
        self.sorting_paused = True
        while self.sorting_paused and self.sorting_active:
            self.root.update()
            time.sleep(0.1)
    
    def begin_sort(self):
        if not(not self.sizeEntry.get() or not self.minEntry.get() or not self.maxEntry.get()):
            self.disable_widgets()
            self.nextStepButton.config(state=NORMAL)
            self.sorting_active = True
            
            if self.algType.get() == "Merge Sort":
                self.sort_thread = Thread(target=lambda: mergeSort(self.data, self.draw,
                                                                 0, len(self.data)-1, self.fastMode.get(), self))
            else:
                alg_dict = {
                    "Bubble Sort": bubbleSort,
                    "Insertion Sort": insertionSort,
                    "Selection Sort": selectionSort
                }
                self.sort_thread = Thread(target=lambda: alg_dict[self.algType.get()](
                    self.data, self.draw, self.fastMode.get(), self))
            
            self.sort_thread.start()
    
    def reset_data(self):
        if len(self.dataHolder) > 0:
            self.sorting_active = False
            resetGlobals()
            self.data = np.copy(self.dataHolder)
            self.draw(self.data, self.color_alternator())
            self.enable_widgets()
            self.nextStepButton.config(state=DISABLED)
    
    def disable_widgets(self):
        self.algMenu.config(state=DISABLED)
        self.sizeEntry.config(state=DISABLED)
        self.minEntry.config(state=DISABLED)
        self.maxEntry.config(state=DISABLED)
        self.genButton.config(state=DISABLED)
        self.sortButton.config(state=DISABLED)
    
    def enable_widgets(self):
        self.algMenu.config(state=NORMAL)
        self.sizeEntry.config(state=NORMAL)
        self.minEntry.config(state=NORMAL)
        self.maxEntry.config(state=NORMAL)
        self.genButton.config(state=NORMAL)
        self.sortButton.config(state=NORMAL)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SortingVisualizer()
    app.run()