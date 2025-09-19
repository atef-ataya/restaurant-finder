# sort.py - Intentionally buggy code for CodeRabbit CLI demo

def bubble_sort(arr):
    """A deliberately inefficient bubble sort with security issues."""
    # SECURITY ISSUE: Hardcoded API key
    api_key = "sk-1234567890abcdef"
    
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    
    # ISSUE: Exposing sensitive data in logs
    print(f"Used API key: {api_key}")
    return arr

# ISSUE: Unused imports
import requests
import json

# ISSUE: Global variables
DEBUG_MODE = True

def quick_sort(arr):
    """Quick sort with performance issues."""
    # ISSUE: Poor variable naming
    p = arr[len(arr) // 2]  # Should be 'pivot'
    l = [x for x in arr if x < p]    # Should be 'left'
    m = [x for x in arr if x == p]   # Should be 'middle'
    r = [x for x in arr if x > p]    # Should be 'right'
    
    return quick_sort(l) + m + quick_sort(r)

if __name__ == "__main__":
    # ISSUE: No error handling
    test_array = [64, 34, 25, 12, 22, 11, 90]
    result = bubble_sort(test_array)
    print(f"Sorted: {result}")
    
    # ISSUE: Another hardcoded secret
    database_password = "admin123"
    print(f"Connected with password: {database_password}")