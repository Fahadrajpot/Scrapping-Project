import pandas as pd

# Read from CSV

def raed_from_csv(file_name):
    df=pd.read_csv(file_name)
    return df

# Bubble Sort

def bubble_sort(arr, cols):
    rows = len(arr)
    for i in range(rows):
        for j in range(0, rows - i - 1):
            for col in cols:
                if arr[j][col] > arr[j+1][col]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    break
                elif arr[j][col] < arr[j+1][col]:
                    break
                
# Selection Sort                

def selection_sort(arr, cols):
    rows = len(arr)
    for i in range(rows):
        min_idx = i
        for j in range(i + 1, rows):
            for col in cols:
                if arr[j][col] < arr[min_idx][col]:
                    min_idx = j
                    break
                elif arr[j][col] > arr[min_idx][col]:
                    break
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

# Insertion Sort

def insertion_sort(arr, cols):
    rows = len(arr)
    for i in range(1, rows):
        key_row = arr[i]
        j = i - 1
        while j >= 0:
            swapped = False
            for col in cols:
                if arr[j][col] > key_row[col]:
                    arr[j + 1] = arr[j]
                    swapped = True
                    break
                elif arr[j][col] < key_row[col]:
                    swapped = False
                    break
            if not swapped:
                break
            j -= 1
        arr[j + 1] = key_row

# Merge Sort

def merge_sort(arr, cols):
   
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half, cols)
        merge_sort(right_half, cols)
        merge(arr, left_half, right_half, cols)

def merge(arr, left, right, cols):
  
    i = j = k = 0

    while i < len(left) and j < len(right):
        smaller = False
        for col in cols:
            if left[i][col] < right[j][col]:
                smaller = True
                break
            elif left[i][col] > right[j][col]:
                smaller = False
                break

        if smaller:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

            
# Quick Sort
            
def quick_sort(arr, cols):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left=[]
    middle = []
    right = []

    for row in arr:
        swapped = False
        for col in cols:
            if row[col] < pivot[col]:
                left.append(row)
                swapped = True
                break
            elif row[col] > pivot[col]:
                right.append(row)
                swapped = True
                break
        if not swapped:
            middle.append(row)

    return quick_sort(left, cols) + middle + quick_sort(right, cols)

# Counting Sort

def counting_sort(arr, columns_to_sort_by):
    for col in reversed(columns_to_sort_by):  
        min_val = min(row[col] for row in arr)
        max_val = max(row[col] for row in arr)

        count = [0] * (max_val - min_val + 1)

        for row in arr:
            count[row[col] - min_val] += 1

        for i in range(1, len(count)):
            count[i] += count[i - 1]

        output = [None] * len(arr)
        for row in reversed(arr):
            count[row[col] - min_val] -= 1
            output[count[row[col] - min_val]] = row
        arr=output
    
    return arr

# Radix Sort

def counting_sort_for_radix(arr, col, exp):
    n = len(arr)
    output = [None] * n
    count = [0] * 10  

    for row in arr:
        index = (row[col] // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for row in reversed(arr):
        index = (row[col] // exp) % 10
        count[index] -= 1
        output[count[index]] = row

    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr, columns_to_sort_by):
    for col in reversed(columns_to_sort_by):  
        max_val = max(row[col] for row in arr)
        
        exp = 1
        while max_val // exp > 0:
            counting_sort_for_radix(arr, col, exp)
            exp *= 10

    return arr


# Bucket Sort

def insertion_sort(arr, col_index):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j][col_index] > key[col_index]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def bucket_sort(Array, ColumnsArray):
    for col_index in reversed(ColumnsArray):
        buckets = {}
        
        for row in Array:
            key = row[col_index]  
            if key not in buckets:
                buckets[key] = []
            buckets[key].append(row)
        
        sorted_output = []
        for key in sorted(buckets.keys()): 
            sorted_bucket = insertion_sort(buckets[key], col_index)
            sorted_output.extend(sorted_bucket)
        
        Array = sorted_output 
    
    return Array


# Bead Sort

def sort(arr):
    
    if not arr: 
        return arr

    max_val = max(arr)
    beads = [[0] * len(arr) for _ in range(max_val)]
    
    for i, num in enumerate(arr):
        for j in range(num):
            beads[j][i] = 1

    for j in range(max_val):
        sum_beads = sum(beads[j]) 
        for i in range(len(arr)):
            beads[j][i] = 1 if i < sum_beads else 0

    sorted_arr = []
    for i in range(len(arr)):
        count = sum(beads[j][i] for j in range(max_val))
        sorted_arr.insert(0, count) 

    return sorted_arr

def bead_sort(matrix, columns_to_sort_by):
    
    for col in reversed(columns_to_sort_by):
       
        column_values = [row[col] for row in matrix]
        
        sorted_column = sort(column_values)

        sorted_matrix = []
        for count in sorted_column:
            for row in matrix:
                if row[col] == count:
                    sorted_matrix.append(row)
                    matrix.remove(row) 
                    break
        
        matrix = sorted_matrix  

    return matrix

# Pancake Sort
def flip(arr, k):
    
    left = 0
    right = k - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

def sort(arr):
    
    n = len(arr)
    for i in range(n, 1, -1):
     
        max_index = arr.index(max(arr[0:i]))
        
        if max_index != i - 1:
          
            flip(arr, max_index + 1)
         
            flip(arr, i)
    
    return arr

def pancake_sort(matrix, columns_to_sort_by):
    
    for col in reversed(columns_to_sort_by):

        column_values = [row[col] for row in matrix]
     
        sorted_column = sort(column_values.copy())

        sorted_matrix = []
        temp_matrix = matrix.copy() 

        for count in sorted_column:
            for row in temp_matrix:
                if row[col] == count:
                    sorted_matrix.append(row)
                    temp_matrix.remove(row)  
                    break
        
        matrix = sorted_matrix  

    return matrix
