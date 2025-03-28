### app/utils.py

from typing import List

def bubble_sort(numbers: List[int]) -> List[int]:
    nums = numbers[:]
    n = len(nums)
    for i in range(n):
        for j in range(0, n - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums

def filter_even(numbers: List[int]) -> List[int]:
    return [x for x in numbers if x % 2 == 0]

def sum_elements(numbers: List[int]) -> int:
    return sum(numbers)

def find_max(numbers: List[int]) -> int:
    if not numbers:
        raise ValueError("Lista vacía")
    return max(numbers)

def binary_search(numbers: List[int], target: int) -> int:
    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == target:
            return mid
        elif numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
