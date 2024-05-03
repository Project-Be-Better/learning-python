### Problem 
You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.

 
```python
# Example 1:

#Input: 
nums1 = [1,2,3,0,0,0]
m = 3

nums2 = [2,5,6] 
n = 3

Output: [1,2,2,3,5,6]

#Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
#The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.


# Example 2:

Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
#Explanation: The arrays we are merging are [1] and [].
#The result of the merge is [1].

# Example 3:

Input: 
nums1 = [0]
m = 0
nums2 = [1]
n = 1
Output: [1]
Explanation: The arrays we are merging are [] and [1].
#The result of the merge is [1].
#Note that because m = 0, there are no elements in nums1. The 0 is only there to ensure the merge result can fit in nums1.
```
 
```
Constraints:

nums1.length == m + n
nums2.length == n
0 <= m, n <= 200
1 <= m + n <= 200
-109 <= nums1[i], nums2[j] <= 109
 
Follow up: Can you come up with an algorithm that runs in O(m + n) time?
```
### Usage 

```python 
```
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.

**Problem Statement**
- There are two arrays, nums1 and nums2. We need to merge them to a single sorted array in  non decreasing order 
- nums1 has the length of `m+n` 

**Input**
- `nums1` : First sorted array  
- `m` : Number of elements to be merged from nums1
- `nums2` : Second sorted array  
- `n` : Number of elements to be merged from nums2

**Output**
- Merged array, sorted, stored in `nums1`
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```python
# Example 1:

#Input: 
nums1 = [1,2,3,0,0,0]
m = 3

nums2 = [2,5,6] 
n = 3

Output: [1,2,2,3,5,6]

#Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
#The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.


# Example 2:

Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
#Explanation: The arrays we are merging are [1] and [].
#The result of the merge is [1].

# Example 3:

Input: 
nums1 = [0]
m = 0
nums2 = [1]
n = 1
Output: [1]
Explanation: The arrays we are merging are [] and [1].
#The result of the merge is [1].
#Note that because m = 0, there are no elements in nums1. The 0 is only there to ensure the merge result can fit in nums1.
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
- Use the [[(algo) Two Pointer Technique|Two Pointer Technique]] with p1 and p2 
	- p1 for nums1 
	- p2 for nums2 
- Another pointer p which is initialized to m+n-1 
- It will be iterated from the end to start 
	- If p1 is greater than p2, p1 will be selected at p and p1 will be decremented 
		`nums1[p] = nums1[p1]`
	- If p2 is greater than p1, p2 will be selected for p and p2 will be decremented 
		`nums1[p] = nums1[p2]` 
	- decrement the p by 1 
- There could be uncopied elements in the nums2 array. If that is the case, copy them over to nums1 array
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any
```python
def merge(nums1: list, nums2: list, m: int, n: int):
    p1 = m - 1
    p2 = n - 1
    p = m + n - 1

    while p1 >= 0 and p2 >= 0:

        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1

        p -= 1

    #
    nums1[: p2 + 1] = nums2[: p2 + 1]
```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
- Time complexity: The algorithm iterates through both arrays once, so it has a time complexity of O(m + n).
- Space complexity: The algorithm uses only a constant amount of extra space, so the space complexity is O(1).
###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.

<img src="img/problem 88.png"/>
