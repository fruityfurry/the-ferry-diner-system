from typing import List, Any, Callable
from random import randint

def _partition(array: List[Any], key: Callable[[Any], Any], low: int, high: int) -> int:
    # Picking a random element as the pivot "shakes things up" to prevent worst-case performance.
    pivotIndex = randint(low, high)
    pivot = array[pivotIndex]
    
    # Move pivot to the end.
    array[pivotIndex], array[high] = array[high], array[pivotIndex]
    
    i = low - 1
    
    # Partition array.
    for j in range(low, high):
        if key(array[j]) < key(pivot):
            i += 1
            array[i], array[j] = array[j], array[i]
            
    # Move pivot to correct position.
    array[i + 1], array[high] = array[high], array[i + 1]
    
    return i + 1

def quicksort(array: List[Any], key: Callable[[Any], Any] = lambda x: x, low: int = 0, high: int = -999) -> None:
    if high == -999: high = len(array) - 1  # Correct default argument to last element of array
    
    if low < high:
        partitionIndex = _partition(array, key, low, high)
        
        quicksort(array, key, low, partitionIndex - 1)
        quicksort(array, key, partitionIndex + 1, high)