"""Various helper functions used throughout the program."""

from typing import List, Any, Callable

# A recursive formulation of a general binary search function. Returns -1 if no match is found.
# Takes in an array, a search item, and a function key to get to the data being compared. (e.g., lambda x: x.customerID)
# Typing is left inccredibly loose to allow for complete generality in this program.
def binarySearch(array: List[Any], searchItem: Any, key: Callable[[Any], Any] = lambda x: x) -> int:
    # If len(array) == 0, there must be no match.
    if len(array) == 0:
        return -1
    
    # Find middle of array and the value at that index.
    mid = len(array) // 2
    midVal = key(array[mid])

    if midVal < searchItem:  # Recursively call function with latter half of array. Python happens to be very forgiving
                             # with slice indices, so there will never be an index out of range error here.
        index = binarySearch(array[(mid+1):], searchItem, key)
        return mid + 1 + index if index != -1 else -1  # Account for indices shifting with array slicing as well as no match.
    if midVal > searchItem:  # Recursively call function with first half of array.
        return binarySearch(array[:mid], searchItem, key)
    
    # If neither of those if statements branched, midVal must be equal to searchItem.
    return mid



from hashlib import sha256

def hash(text: str) -> int:
    textBytes = text.encode()
    hashNumHex = sha256(textBytes).hexdigest()
    hashNum = int(hashNumHex, 16)
    return hashNum



def roundPrice(x: float) -> str:
    # String form of price.
    xString = str(round(float(x), 2))
    # Part after decimal point.
    decimal = xString.split(".")[1]
    
    # Length of decimal part is guaranteed to be 2 or 1 after rounding.
    if len(decimal) == 1:
        xString += "0"  # Add on trailing zero.
        
    return xString



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