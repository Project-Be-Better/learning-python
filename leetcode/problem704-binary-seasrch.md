### Problem 
Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.
You must write an algorithm with O(log n) runtime complexity.
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
**Problem**
- Given a sorted array of integers and target. We need to write a function to search the array. 
**Input**
- Sorted list of integers num
- integer target 
**Output**
- Return an integer representing the index of the target. If nothing is found, return -1 
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```
Example 1:

Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4
Example 2:

Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
1. Initialize two pointers, left and right 
	1. left is initialized to 0 and right is initialized to the end of the array 
2. Until the number of elements left is 1 : 
	1. calculate mid by floor dividing left and right by 2 
	2. Check if `nums[mid] == target`, if so return mid
	3. if the guess is greater than target, move the right pointer back 
	4. If the guess is less than target, move the left pointer 
	5. Return -1 if no matches are found 
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.
```python
from typing import List


def search(nums: List[int], target: int) -> int:

    left = 0
    right = len(nums) - 1

    # While there is only one element left
    while left <= right:

        mid = (left + right) // 2
        guess = nums[mid]

        # Guess matches the target
        if guess == target:
            return mid

        # Guess is too high, lowering right side
        if guess > target:
            right = mid - 1

        # Guess is too low, incrementing left side
        else:
            left = mid + 1

    # No Matches found
    return -1


```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
- Time Complexity: O(log n) - Binary search divides the search space in half at each step.
###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.

<img src="img/problem 704.png"/>
