import random
import time
import timeit
# Multiple thread
import threading

"""
Sort Algorithm
"""

#swap
def swap(a,b):
    a = a^b
    b = b^a
    a = a^b
    return a,b

#arr[::-1]
def reverse(arr):
    left = 0
    right = len(arr) - 1
    while left < right:
        # Swap the elements corresponding to left and right pointers
        arr[left], arr[right] = arr[right], arr[left]
        # Move the left and right pointers
        left += 1
        right -= 1
    return arr

#SelectionSort
def SelectionSort(arr):
    n=len(arr)
    left = 0
    right = n-1
    while left < right:
        min = left
        max = left
        # Find the minimum and maximum elements within the range [left, right]
        for j in range(left+1,right+1):
            if arr[j] < arr[min]:
                min = j
            if arr[j] > arr[max]:
                max = j
        # Swap the minimum element with the leftmost element if necessary
        if min != left:
            arr[left], arr[min] = arr[min], arr[left]
        # If the maximum element was initially at 'left', update 'max_index' accordingly
        if max == left:
            max = min
        # Swap the maximum element with the rightmost element if necessary
        if max != right:
            arr[right], arr[max] = arr[max], arr[right]
        # Move the left and right pointers
        left+=1
        right-=1
        #print(arr) # Test code
    return arr

#BubbleSort
def BubbleSort(arr):
    n = len(arr)
    left = 0
    right = n - 1
    while left < right:
        swapped = False
        last_swap_left = 0
        last_swap_right = 0
        # Scan from left to right
        for i in range(left, right):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
                last_swap_right = i
        #print(arr) # Test code
        # Update the right boundary
        right = last_swap_right
        # If no swap occurs, the array is already sorted
        if not swapped:
            break
        swapped = False
        # Scan from right to left
        for i in range(right, left, -1):
            if arr[i] < arr[i-1]:
                arr[i], arr[i-1] = arr[i-1], arr[i]
                swapped = True
                last_swap_left = i
        #print(arr) # Test code
        # Update the left boundary
        left = last_swap_left
        # If no swap occurs, the array is already sorted
        if not swapped:
            break
    return arr

#InsertionSort
def InsertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        left, right = 0, i - 1
        # Binary search for the insertion position
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] < key:
                left = mid + 1
            else:
                right = mid - 1
        # Move elements greater than key to the right
        for j in range(i - 1, left - 1, -1):
            arr[j + 1] = arr[j]
        arr[left] = key
        #print(arr) # Test code
    return arr

#InsertionSort is better used for sorting linked lists. Here is the feasible method.
"""
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def insertion_sort_linked_list(head):
    dummy = ListNode(float("-inf"))  # Dummy node to simplify insertion
    curr = head
    while curr:
        prev = dummy
        next_node = curr.next
        while prev.next and prev.next.val < curr.val:
            prev = prev.next
        curr.next = prev.next
        prev.next = curr
        curr = next_node
    return dummy.next

class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

def insertion_sort_doubly_linked_list(head):
    dummy = DoublyListNode(float("-inf"))  # Dummy node to simplify insertion
    curr = head
    while curr:
        prev = dummy
        next_node = curr.next
        while prev.next and prev.next.val < curr.val:
            prev = prev.next
        curr.next = prev.next
        if prev.next:
            prev.next.prev = curr
        prev.next = curr
        curr.prev = prev
        curr = next_node
    return dummy.next

class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

def insertion_sort_doubly_circular_linked_list(head):
    if not head:
        return None
    dummy = DoublyListNode(float("-inf"))  # Dummy node to simplify insertion
    dummy.next = dummy.prev = head
    tail = head
    curr = head.next
    while curr != head:
        prev = dummy
        next_node = curr.next
        while prev.next != tail and prev.next.val < curr.val:
            prev = prev.next
        curr.next = prev.next
        curr.prev = prev
        prev.next = curr
        curr.next.prev = curr
        if curr == tail:
            tail = curr.next
        curr = next_node
    return dummy.next
"""

#MergeSort
class MergeSort:
    def __init__(self):
        pass

    # Sort method
    def sort(self, arr):
        if len(arr) <= 5:
            return InsertionSort(arr)
        mid = len(arr) // 2
        left = self.sort(arr[:mid])
        #print(left) # Test code
        right = self.sort(arr[mid:])
        #print(right) # Test code
        if left[-1] <= right[0]:
            return left + right
        return self.merge(left, right)
    
    # Merge method
    def merge(self, left, right):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        #print(merged) # Test code
        return merged
    
    """
    # Test code
    arr = []
    merge_sort = MergeSort()
    sorted_arr = merge_sort.sort(arr)
    """
    
    """
    #InsertionSort
    def InsertionSort(arr):
        for i in range(1, len(arr)):
            key = arr[i]
            left, right = 0, i - 1
            # Binary search for the insertion position
            while left <= right:
                mid = (left + right) // 2
                if arr[mid] < key:
                    left = mid + 1
                else:
                    right = mid - 1
            # Move elements greater than key to the right
            for j in range(i - 1, left - 1, -1):
                arr[j + 1] = arr[j]
            arr[left] = key
        return arr
    """

"""
def merge_sorted_arrays(arr1, arr2):
    merged = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1
    merged.extend(arr1[i:])
    merged.extend(arr2[j:])
    return merged

def parallel_merge(arr1, arr2, result):
    merged = merge_sorted_arrays(arr1, arr2)
    result.extend(merged)

def parallel_merge_sort(arr, num_threads=2):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    if num_threads > 1:
        left_result = []
        right_result = []
        left_thread = threading.Thread(target=parallel_merge_sort, args=(left, num_threads // 2))
        right_thread = threading.Thread(target=parallel_merge_sort, args=(right, num_threads // 2))
        left_thread.start()
        right_thread.start()
        left_thread.join()
        right_thread.join()
        merge_thread = threading.Thread(target=parallel_merge, args=(left, right, left_result))
        merge_thread.start()
        merge_thread.join()
        return left_result
    else:
        merge_sort = MergeSort()
        sorted_left = merge_sort.sort(left)
        sorted_right = merge_sort.sort(right)
        return merge_sorted_arrays(sorted_left, sorted_right)
"""

#BucketSort
def BucketSort(arr):
    n = len(arr)
    if n <= 1:
        return arr
    # Find minimum and maximum values in the array
    min_val = min(arr)
    max_val = max(arr)
    # Calculate the range of each bucket
    bucket_range = (max_val - min_val) / n
    # Create buckets
    buckets = [[] for _ in range(n)]
    # Distribute elements into buckets
    for num in arr:
        index = int((num - min_val) / bucket_range)
        if index != n:
            buckets[index].append(num)
        else:
            buckets[n - 1].append(num)
    #print(buckets) # Test code
    # Sort each bucket
    for i in range(n):
        if len(buckets[i]) > 1:
            #Use insertion sort for small buckets, or use bubble sort and selection sort
            if len(buckets[i]) <= 10:
                buckets[i] = InsertionSort(buckets[i])
            else:
                buckets[i] = QuickSort(buckets[i])
    #print(buckets) # Test code
    # Concatenate sorted buckets
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)
    return sorted_arr

#CountingSort
def CountingSort(arr):
    if not arr:
        return arr
    min_val = min(arr)
    max_val = max(arr)
    # Create a nested list to store counts for each value
    counts = [0] * (max_val - min_val + 1)
    # Count occurrences of each value
    for num in arr:
        counts[num - min_val] += 1
    #print(counts) # Test code
    # Sort the array based on counts
    index = 0
    for i, count in enumerate(counts):
        for _ in range(count):
            arr[index] = i + min_val
            index += 1
    return arr

#RadixSort
class RadixSort:
    def __init__(self):
        pass

    def sort(self, arr):
        if not arr:
            return arr
        # Find the maximum number to determine the number of digits
        max_num = max(arr)
        max_digits = len(str(abs(max_num)))
        # Perform LSD (Least Significant Digit) radix sort
        for digit in range(max_digits):
            arr = self.Radix_Sort(arr, digit)
        return arr

    def Radix_Sort(self, arr, digit):
        # Create a nested list to store counts for each digit
        counts = [[] for _ in range(10)]
        # Count occurrences of each digit
        for num in arr:
            d = (num // (10 ** digit)) % 10
            counts[d].append(num)
        #print(counts) # Test code
        # Concatenate digits in the correct order
        sorted_arr = []
        for i in range(10):
            sorted_arr.extend(counts[i])
        return sorted_arr

#Quicksort
def QuickSortClassic(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    #print(left,middle,right) # Test code
    return QuickSortClassic(left) + middle + QuickSortClassic(right)

class QuickSort:
    def __init__(self):
        pass

    def sort(self, arr):
        self.quick_sort(arr, 0, len(arr) - 1)
        return arr

    def quick_sort(self, arr, left, right):
        if left >= right:
            return

        # Three median method for selecting pivot
        self.median_of_three(arr, left, right)

        pivot = arr[left]
        i = left + 1
        j = right

        while True:
            while i <= j and arr[i] <= pivot:
                i += 1
            while i <= j and arr[j] >= pivot:
                j -= 1
            if i > j:
                break
            arr[i], arr[j] = arr[j], arr[i]

        arr[left], arr[j] = arr[j], arr[left]

        # Dual pivot quicksort
        self.quick_sort(arr, left, j - 1)
        self.quick_sort(arr, j + 1, right)

    def median_of_three(self, arr, left, right):
        mid = (left + right) // 2
        if arr[mid] < arr[left]:
            arr[left], arr[mid] = arr[mid], arr[left]
        if arr[right] < arr[left]:
            arr[left], arr[right] = arr[right], arr[left]
        if arr[right] < arr[mid]:
            arr[mid], arr[right] = arr[right], arr[mid]
        arr[left], arr[mid] = arr[mid], arr[left]

#ShellSort
def ShellSort(arr):
    n = len(arr)
    gap = n // 2  # Initial gap is half of the array length
    # Choose the increment sequence
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # Insertion sort
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        #print(gap,arr) #Test code
        gap //= 2  # Reduce the gap
    return arr

#HeapSort
class HeapSort():
    def __init__(self):
        pass

    def Heapify(self,heap, start, end):
        son = start * 2
        while son <= end:
            # Compare with the larger child if it exists
            if son + 1 <= end and heap[son + 1] > heap[son]:
                son += 1
            # Swap with the larger child if necessary
            if heap[son] > heap[start]:
                heap[start], heap[son] = heap[son], heap[start]
                # Move down to the next level
                start, son = son, son * 2
            else:
                break

    def sort(self,arr):
        # Create a heap from the array
        heap = [ None ] + arr
        root = 1
        length = len(heap)
        # Build max heap
        for i in range(length // 2, root - 1, -1):
            self.Heapify(heap, i, length-1)
        # Extract elements from the heap
        for i in range(length-1, root, -1):
            # Swap root with the last element
            heap[i], heap[root] = heap[root], heap[i]
            # Adjust heap after removing the root
            self.Heapify(heap, root, i-1)
        return heap[root:]

#Test code
def Test():
    arr = list(range(1,2049))
    #print(arr)
    random.shuffle(arr)
    print(arr)
    heap_sort = HeapSort()
    starttime = time.time()
    sortarr = heap_sort.sort(arr)
    endtime = time.time()
    print(sortarr)
    print(f"Time taken for sorting: {endtime-starttime} seconds.")
    
#main
if __name__ == '__main__':
    Test()
