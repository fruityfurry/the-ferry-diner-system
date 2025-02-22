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