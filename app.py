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

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class LinkedList:
    def __init__(self, max_size=10):
        self.head = None
        self.size = 0
        self.max_size = max_size
    
    def insert_at_beginning(self, data):
        if self.size >= self.max_size:
            return False, "Linked List is full"
        
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        return True, "Insert successful"
    
    def insert_at_end(self, data):
        if self.size >= self.max_size:
            return False, "Linked List is full"
            
        new_node = Node(data)
        
        if not self.head:
            self.head = new_node
            self.size += 1
            return True, "Insert successful"
            
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        self.size += 1
        return True, "Insert successful"
    
    def delete_at_beginning(self):
        if not self.head:
            return False, "Linked List is empty"
            
        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return True, data
    
    def delete_at_end(self):
        if not self.head:
            return False, "Linked List is empty"
            
        if not self.head.next:
            data = self.head.data
            self.head = None
            self.size -= 1
            return True, data
            
        current = self.head
        while current.next.next:
            current = current.next
        data = current.next.data
        current.next = None
        self.size -= 1
        return True, data
    
    def get_all_nodes(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(current.data)
            current = current.next
        return nodes

# Initialize linked list
linked_list = LinkedList()

# Add new routes
@app.route('/linkedlist/insert_beginning', methods=['POST'])
def linkedlist_insert_beginning():
    data = request.get_json()
    value = int(data['value'])
    success, message = linked_list.insert_at_beginning(value)
    return jsonify({
        'success': success,
        'message': message,
        'nodes': linked_list.get_all_nodes()
    })

@app.route('/linkedlist/insert_end', methods=['POST'])
def linkedlist_insert_end():
    data = request.get_json()
    value = int(data['value'])
    success, message = linked_list.insert_at_end(value)
    return jsonify({
        'success': success,
        'message': message,
        'nodes': linked_list.get_all_nodes()
    })

@app.route('/linkedlist/delete_beginning', methods=['POST'])
def linkedlist_delete_beginning():
    success, result = linked_list.delete_at_beginning()
    return jsonify({
        'success': success,
        'message': result if not success else "Delete successful",
        'value': result if success else None,
        'nodes': linked_list.get_all_nodes()
    })

@app.route('/linkedlist/delete_end', methods=['POST'])
def linkedlist_delete_end():
    success, result = linked_list.delete_at_end()
    return jsonify({
        'success': success,
        'message': result if not success else "Delete successful",
        'value': result if success else None,
        'nodes': linked_list.get_all_nodes()
    })

# Stack and Queue data structures
class Stack:
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size
    
    def push(self, item):
        if len(self.items) >= self.max_size:
            return False, "Stack is full"
        self.items.append(item)
        return True, "Push successful"
    
    def pop(self):
        if not self.items:
            return False, "Stack is empty"
        return True, self.items.pop()
    
    def peek(self):
        if not self.items:
            return None
        return self.items[-1]
    
    def get_items(self):
        return self.items

class Queue:
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size
    
    def enqueue(self, item):
        if len(self.items) >= self.max_size:
            return False, "Queue is full"
        self.items.append(item)
        return True, "Enqueue successful"
    
    def dequeue(self):
        if not self.items:
            return False, "Queue is empty"
        return True, self.items.pop(0)
    
    def peek(self):
        if not self.items:
            return None
        return self.items[0]
    
    def get_items(self):
        return self.items

# Initialize data structures
stack = Stack()
queue = Queue()

@app.route('/')
def index():
    return render_template('DSV.html')

@app.route('/generateDS', methods=['POST'])
def generateDS():
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

@app.route('/stack/push', methods=['POST'])
def stack_push():
    data = request.get_json()
    value = int(data['value'])
    success, message = stack.push(value)
    return jsonify({
        'success': success,
        'message': message,
        'items': stack.get_items()
    })

@app.route('/stack/pop', methods=['POST'])
def stack_pop():
    success, result = stack.pop()
    return jsonify({
        'success': success,
        'message': result if not success else "Pop successful",
        'value': result if success else None,
        'items': stack.get_items()
    })

@app.route('/queue/enqueue', methods=['POST'])
def queue_enqueue():
    data = request.get_json()
    value = int(data['value'])
    success, message = queue.enqueue(value)
    return jsonify({
        'success': success,
        'message': message,
        'items': queue.get_items()
    })

@app.route('/queue/dequeue', methods=['POST'])
def queue_dequeue():
    success, result = queue.dequeue()
    return jsonify({
        'success': success,
        'message': result if not success else "Dequeue successful",
        'value': result if success else None,
        'items': queue.get_items()
    })

if __name__ == '__main__':
    app.run(debug=True)