# app.py
from flask import Flask, render_template, jsonify, request
import random
import numpy as np

app = Flask(__name__)

# Sorting algorithms
def bubble_sort(data):
    steps = []
    n = len(data)
    arr = data.copy()
    
    for i in range(n-1):
        for j in range(n-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append({
                    'array': arr.copy(),
                    'comparing': [j, j+1]
                })
    return steps

def selection_sort(data):
    steps = []
    n = len(data)
    arr = data.copy()
    
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append({
            'array': arr.copy(),
            'comparing': [i, min_idx]
        })
    return steps

def insertion_sort(data):
    steps = []
    n = len(data)
    arr = data.copy()
    
    for i in range(1, n):
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
            steps.append({
                'array': arr.copy(),
                'comparing': [j+1, j+2]
            })
        arr[j+1] = key
    return steps

def merge_sort(data):
    steps = []
    arr = data.copy()
    
    def merge(arr, l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        i = j = 0
        k = l
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
            steps.append({
                'array': arr.copy(),
                'comparing': [k-1, k]
            })
            
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            steps.append({
                'array': arr.copy(),
                'comparing': [k-1]
            })
            
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            steps.append({
                'array': arr.copy(),
                'comparing': [k-1]
            })
    
    def merge_sort_recursive(arr, l, r):
        if l < r:
            m = (l + r) // 2
            merge_sort_recursive(arr, l, m)
            merge_sort_recursive(arr, m + 1, r)
            merge(arr, l, m, r)
    
    merge_sort_recursive(arr, 0, len(arr)-1)
    return steps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    size = int(data['size'])
    min_val = int(data['min'])
    max_val = int(data['max'])
    
    array = [random.randint(min_val, max_val) for _ in range(size)]
    return jsonify({'array': array})

@app.route('/sort', methods=['POST'])
def sort():
    data = request.get_json()
    array = data['array']
    algorithm = data['algorithm']
    
    algorithms = {
        'bubble': bubble_sort,
        'selection': selection_sort,
        'insertion': insertion_sort,
        'merge': merge_sort
    }
    
    steps = algorithms[algorithm](array)
    return jsonify({'steps': steps})

if __name__ == '__main__':
    app.run(debug=True)