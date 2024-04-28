Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

```py
#Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

#Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

#Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]
 
```
Constraints:

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
Only one valid answer exists.
 

Follow-up: Can you come up with an algorithm that is less than O(n2) time complexity?

###### 1. State the problem clearly. Identify the input & output formats.

""" 
Given an array of numbers, find two numbers that can be added to return the target 
"""

###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.

```py
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1]

Input: nums = [3,2,4], target = 6
Output: [1,2]

Input: nums = [3,3], target = 6
Output: [0,1]
```

###### 3. Come up with a correct solution for the problem. State it in plain English.
""" 
1. Create a Hashmap called complement dict 
2. Enumerate over the array and calculate complement 
3. Check if the complement is in the complement dict 
    3.1 If does not exist, add the number to the complement dict with the index and value 
4. If no values are found, [] is returned 
"""

###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.

###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.

###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.

```py
def two_sum(nums: list, target: int):
    """
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    """

    complement_dict = {}

    for i, num in enumerate(nums):

        # Find the complement of the query wrt to numer
        complement = target - num

        if complement in complement_dict:
            return [i, complement_dict[complement]]

        complement_dict[num] = i

        print(
            f"index : {i} num : {num} complement : {complement} map : {complement_dict}"
        )

    return []
```
