#sortingAlgorithms.py
import time
import numpy as np
from turtle import color
from tkinter import DISABLED, NORMAL

speed = 0.2
originalColorArray = []

def resetGlobals():
    global speed
    global originalColorArray
    speed = 0.2
    originalColorArray = np.array([])

def colorAlternator(data):
    dataSize = len(data)
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

def bubbleSort(data, draw, fastMode, visualizer):
    dataLength = len(data)-1
    originalColorArray = np.array(colorAlternator(data))
    updatedColor = np.copy(originalColorArray)
    
    for i in range(dataLength):
        for j in range(dataLength):
            if not visualizer.sorting_active:
                return
                
            if data[j] > data[j+1]:
                data[j+1], data[j] = data[j], data[j+1]
                for k in range(len(data)):
                    if (k == j or k == j+1):
                        updatedColor[k] = '#93f1b7'
                    else:
                        updatedColor[k] = originalColorArray[k]
                draw(data, updatedColor)
                
                if not fastMode:
                    visualizer.wait_for_step()
                else:
                    time.sleep(0.0001)
    
    draw(data, originalColorArray)
    visualizer.sorting_active = False
    visualizer.nextStepButton.config(state=DISABLED)
    visualizer.enable_widgets()

def insertionSort(data, draw, fastMode, visualizer):
    originalColorArray = np.array(colorAlternator(data))
    updatedColor = np.copy(originalColorArray)
    dataLength = len(data)
    
    for i in range(1, dataLength):
        if not visualizer.sorting_active:
            return
            
        dataVal = data[i]
        while data[i-1] > dataVal and i > 0:
            if not visualizer.sorting_active:
                return
                
            data[i], data[i-1] = data[i-1], data[i]
            i -= 1
            for j in range(dataLength):
                if (j == i or j == i-1):
                    updatedColor[j] = '#93f1b7'
                else:
                    updatedColor[j] = originalColorArray[j]
            draw(data, updatedColor)
            
            if not fastMode:
                visualizer.wait_for_step()
            else:
                time.sleep(0.0001)
    
    draw(data, originalColorArray)
    visualizer.sorting_active = False
    visualizer.nextStepButton.config(state=DISABLED)
    visualizer.enable_widgets()

def selectionSort(data, draw, fastMode, visualizer):
    originalColorArray = np.array(colorAlternator(data))
    updatedColor = np.copy(originalColorArray)
    dataLength = len(data)
    
    for i in range(dataLength):
        if not visualizer.sorting_active:
            return
            
        minVal = i
        for j in range(i+1, dataLength):
            if not visualizer.sorting_active:
                return
                
            if data[j] < data[minVal]:
                minVal = j
        
        if minVal != i:
            data[minVal], data[i] = data[i], data[minVal]
            for k in range(dataLength):
                if (k == minVal or k == i):
                    updatedColor[k] = '#93f1b7'
                else:
                    updatedColor[k] = originalColorArray[k]
            draw(data, updatedColor)
            
            if not fastMode:
                visualizer.wait_for_step()
            else:
                time.sleep(0.0001)
    
    draw(data, originalColorArray)
    visualizer.sorting_active = False
    visualizer.nextStepButton.config(state=DISABLED)
    visualizer.enable_widgets()

def mergeSort(data, draw, left, right, fastMode, visualizer):
    global originalColorArray
    global speed
    
    if not originalColorArray:
        originalColorArray = colorAlternator(data)
    
    if fastMode:
        speed = 0.0001
    else:
        speed = 0.2

    if left < right and visualizer.sorting_active:
        middle = (left + right) // 2
        mergeSort(data, draw, left, middle, fastMode, visualizer)
        mergeSort(data, draw, middle+1, right, fastMode, visualizer)
        
        if not visualizer.sorting_active:
            return
            
        draw(data, changeColor(len(data), left, middle, right))
        if not fastMode:
            visualizer.wait_for_step()
        else:
            time.sleep(speed)
            
        leftArray = data[left:middle+1]
        rightArray = data[middle+1:right+1]
        i = 0
        j = 0
        k = left
        leftLength = len(leftArray)
        rightLength = len(rightArray)

        while k <= right and visualizer.sorting_active:
            if i < leftLength and j < rightLength:
                if leftArray[i] <= rightArray[j]:
                    data[k] = leftArray[i]
                    i += 1
                else:
                    data[k] = rightArray[j]
                    j += 1
            elif i < leftLength:
                data[k] = leftArray[i]
                i += 1
            else:
                data[k] = rightArray[j]
                j += 1
            k += 1
            
            draw(data, originalColorArray)
            if not fastMode:
                visualizer.wait_for_step()
            else:
                time.sleep(speed)
    
    if right == len(data) - 1:  # If we're at the top level of recursion
        visualizer.sorting_active = False
        visualizer.nextStepButton.config(state=DISABLED)
        visualizer.enable_widgets()

def changeColor(length, left, middle, right):
    colorArray = []
    for i in range(length):
        if i >= left and i <= right:
            if i >= left and i <= middle:
                colorArray.append("#b8f7bb")
            else:
                colorArray.append("#b8f7eb")
        else:
            colorArray.append(originalColorArray[i])
    return colorArray