### Problem 
Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.

```
Example 1:

Input: nums = [1,2,3,1]
Output: true
Example 2:

Input: nums = [1,2,3,4]
Output: false
Example 3:

Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
 

Constraints:

1 <= nums.length <= 105
-109 <= nums[i] <= 109
```
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
- Given is an array and we need to return true if any value appears twice in the array 
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```python
Input: nums = [1,2,3,1]
Output: true

Input: nums = [1,2,3,4]
Output: false

Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
1. Make a set of the array
2. Check if the length of the set to that of the original array 
3. If the lengths are different, then there are duplicates 
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.
```python
def contains_duplicate(nums):
    """
    Checks if an array contains any duplicates
    """
    # Checks the length of the array with a set from the same array
    unique_array = list(set(nums))

    # Returns True if there are duplicates
    return not len(nums) == len(unique_array)

```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
Time complexity: O(n) where n is the number of elements in the array.
###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.

<img src="img/problem 217.png"/>
