
### Problem 
You are given an m x n integer matrix matrix with the following two properties:
Each row is sorted in non-decreasing order.
The first integer of each row is greater than the last integer of the previous row.
Given an integer target, return true if target is in matrix or false otherwise.
You must write a solution in O(log(m * n)) time complexity.
### Usage 

```python 
```
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
**Problem**
`m x n` matrix with the following properties
- Each row is sorted and non decreasing order 
- First integer of each row is larger than the last integer of the previous row 
**Input** 
Matrix of `m x n` and integer `target`
**Output**
True if target is found in the matrix else return false

###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true

Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
There will be two binary searches for this problem 
1. To find the row 
2. To find the value 

For the row : 
1. Calculate the column length and row length 
2. Find the middle row
3. If the target is more than the last element of the selected row, we need to move to the right 
4. If the target is less than the first element of the selected row, move to the left 
5. Break the loop if we find the row

Binary search within the selected row : 
1. Initialize two pointers, left and right 
	1. left is initialized to 0 and right is initialized to the end of the array 
2. Until the number of elements left is 1 : 
	1. calculate mid by floor dividing left and right by 2 
	2. Check if `guess_value == target`, if so return True
	3. if the guess is greater than target, move the right pointer back 
	4. If the guess is less than target, move the left pointer 
	5. Return False if no matches are found 
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.
```python
from typing import List


def search_matrix(matrix: List[List[int]], target: int):

    rows = len(matrix)
    cols = len(matrix[0])

    top_row = 0
    bottom_row = rows - 1

    # Binary search through the arrays in the matrix
    while top_row <= bottom_row:

        # Find the middle row
        mid_row = (top_row + bottom_row) // 2

        # Target is greater than the end of the array
        if target > matrix[mid_row][-1]:
            top_row = mid_row + 1

        # Target is smaller than the start of the array
        elif target < matrix[mid_row][0]:
            bottom_row = mid_row - 1

        # Target is in this array
        else:
            break

    # If the row is not found, return false
    if not (top_row <= bottom_row):
        return False

    # Binary search the selected array in the matrix
    left = 0
    right = cols - 1

    while left <= right:
        mid = (left + right) // 2
        guess_value = matrix[mid_row][mid]

        # Return is guess is correct
        if guess_value == target:
            return True

        # Check if guess is too high
        if guess_value > target:
            right = mid - 1

        # Check if guess is too low
        else:
            left = mid + 1

    return False


if __name__ == "__main__":
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    target = 3
    rlt = search_matrix(matrix, target)

```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
We do two binary searches. One for the row and another for finding the element. So the resultant complexity is O(log m + log n )
###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.

#### Related 
1. [[DSA Strategy]]
2. [[Binary Search]]
#### References
1. [Roadmap (neetcode.io)](https://neetcode.io/roadmap)
2. [Search a 2D Matrix - Leetcode 74 - Python (youtube.com)](https://www.youtube.com/watch?v=Ber2pi2C0j0&t=106s)

<img src="img/problem 74.png"/>
