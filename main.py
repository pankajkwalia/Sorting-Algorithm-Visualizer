import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# Sorting Algorithms
def bubblesort(A):
    n = len(A)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if A[j] > A[j+1]:
                A[j], A[j+1] = A[j+1], A[j]
                swapped = True
            yield A
        if not swapped:
            break

def insertionsort(A):
    for i in range(1, len(A)):
        key = A[i]
        j = i - 1
        while j >= 0 and key < A[j]:
            A[j + 1] = A[j]
            j -= 1
            yield A
        A[j + 1] = key
        yield A

def selectionsort(A):
    n = len(A)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if A[j] < A[min_idx]:
                min_idx = j
            yield A
        A[i], A[min_idx] = A[min_idx], A[i]
        yield A

def mergesort(A, start=0, end=None):
    if end is None:
        end = len(A) - 1
    if start >= end:
        return
    mid = (start + end) // 2
    yield from mergesort(A, start, mid)
    yield from mergesort(A, mid + 1, end)
    yield from merge(A, start, mid, end)
    yield A

def merge(A, start, mid, end):
    left = A[start:mid + 1]
    right = A[mid + 1:end + 1]
    k = start
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            A[k] = left[i]
            i += 1
        else:
            A[k] = right[j]
            j += 1
        k += 1
        yield A
    while i < len(left):
        A[k] = left[i]
        i += 1
        k += 1
        yield A
    while j < len(right):
        A[k] = right[j]
        j += 1
        k += 1
        yield A

def quicksort(A, start=0, end=None):
    if end is None:
        end = len(A) - 1
    if start >= end:
        return
    pivot = A[end]
    p_index = start
    for i in range(start, end):
        if A[i] <= pivot:
            A[i], A[p_index] = A[p_index], A[i]
            p_index += 1
        yield A
    A[p_index], A[end] = A[end], A[p_index]
    yield A
    yield from quicksort(A, start, p_index - 1)
    yield from quicksort(A, p_index + 1, end)

# Visualization function
def visualize_multiple(sort_funcs, N=100, speed=15):
    A = list(range(1, N + 1))
    random.shuffle(A)
    arrays = [A[:] for _ in sort_funcs]  # Duplicate the array for each sort function
    
    generators = [sort_func(array) for sort_func, array in zip(sort_funcs, arrays)]
    titles = [sort_func.__name__.capitalize() for sort_func in sort_funcs]
    
    fig, axs = plt.subplots(len(sort_funcs), 1, figsize=(10, 5 * len(sort_funcs)))  # Create subplots
    
    if len(sort_funcs) == 1:
        axs = [axs]
    
    plots = []
    texts = []
    start_times = [time.time() for _ in sort_funcs]
    iterations = [[0] for _ in sort_funcs]
    
    # Setup each subplot
    for ax, title, array in zip(axs, titles, arrays):
        if title == "Mergesort":
            ax.set_title(f"{title} O(n log n)")
        elif title == "Quicksort":
            ax.set_title(f"{title} O(n log n)")
        else:
            ax.set_title(f"{title} O(n²)")
        bar_sub = ax.bar(range(len(array)), array, align="edge")
        ax.set_xlim(0, N)
        text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
        plots.append(bar_sub)
        texts.append(text)

    def update(A, rects, iteration, text, start_time):
        for rect, val in zip(rects, A):
            rect.set_height(val)
        iteration[0] += 1
        elapsed_time = time.time() - start_time
        text.set_text(f"# of operations: {iteration[0]}, Time: {elapsed_time:.2f}s")
    
    # Animation function to update each frame
    def animate(i):
        for gen, plot, iter_data, text, start_time in zip(generators, plots, iterations, texts, start_times):
            try:
                update(next(gen), plot, iter_data, text, start_time)
            except StopIteration:
                pass

    anim = animation.FuncAnimation(
        fig,
        animate,
        repeat=False,
        blit=False,
        interval=speed,
        cache_frame_data=False  # Explicitly set cache_frame_data to False
    )
    
    plt.show()
    plt.close()

# Function to start visualization based on user input
def start_visualization_multiple():
    selected_sort_funcs = []
    if bubble_sort_var.get():
        selected_sort_funcs.append(bubblesort)
    if insertion_sort_var.get():
        selected_sort_funcs.append(insertionsort)
    if selection_sort_var.get():
        selected_sort_funcs.append(selectionsort)
    if merge_sort_var.get():
        selected_sort_funcs.append(mergesort)
    if quick_sort_var.get():
        selected_sort_funcs.append(quicksort)
    
    speed = int(speed_choice.get())
    visualize_multiple(selected_sort_funcs, speed=speed)

# GUI Setup
root = tk.Tk()
root.title("Sorting Algorithm Visualizer")

bubble_sort_var = tk.BooleanVar()
insertion_sort_var = tk.BooleanVar()
selection_sort_var = tk.BooleanVar()
merge_sort_var = tk.BooleanVar()
quick_sort_var = tk.BooleanVar()

speed_choice = tk.StringVar(value="15")

# GUI Labels and Input Fields
ttk.Label(root, text="Choose sorting algorithms:").grid(column=0, row=0, padx=10, pady=10)

ttk.Checkbutton(root, text="Bubble Sort", variable=bubble_sort_var).grid(column=1, row=0, padx=10, pady=10)
ttk.Checkbutton(root, text="Insertion Sort", variable=insertion_sort_var).grid(column=1, row=1, padx=10, pady=10)
ttk.Checkbutton(root, text="Selection Sort", variable=selection_sort_var).grid(column=1, row=2, padx=10, pady=10)
ttk.Checkbutton(root, text="Merge Sort", variable=merge_sort_var).grid(column=1, row=3, padx=10, pady=10)
ttk.Checkbutton(root, text="Quick Sort", variable=quick_sort_var).grid(column=1, row=4, padx=10, pady=10)

ttk.Label(root, text="Choose animation speed (ms):").grid(column=0, row=5, padx=10, pady=10)
speed_menu = ttk.Combobox(root, textvariable=speed_choice)
speed_menu['values'] = ("10", "15", "20", "30", "50", "100")
speed_menu.grid(column=1, row=5, padx=10, pady=10)

# Start Visualization Button
ttk.Button(root, text="Start Visualization", command=start_visualization_multiple).grid(column=0, row=6, columnspan=2, padx=10, pady=20)

root.mainloop()
