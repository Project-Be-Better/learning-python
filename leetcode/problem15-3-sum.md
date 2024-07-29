### Problem 
Given an integer array nums, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
- Given an integer array nums, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`. 
- Input array is nums 
- Output : List of lists where inner list contains an array of numbers summing up to zero 
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.

> [!tip] Input
```
Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.
Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.
Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
- Sort the array 
- Iterate through the array 
- Two pointer technique 
	1. Initialise two pointers : left and right 
	2. Check the sum of current number, numbers at left and right pointer 
	3. If sum is zero, add the triplet to the result and move the pointers
	4. If the sum is less than zero, increment left pointer by one to increase the sum 
	5. IF sum is more than zero, decrease right pointer to decrease the sum 
	6. Once the number is added, make sure that the duplicates are skipped by checking the number at the left pointer is same as the previous one or when left is lesser than right
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.

> [!done] Solution
```python
def three_sum(nums):
    res = []
    nums.sort()

    # enumerate
    for index, num in enumerate(nums):

        # skip the duplicate number
        if index > 0 and nums[index] == nums[index - 1]:
            continue

        # two pointers left and right
        left, right = index + 1, len(nums) - 1

        while left < right:
            result = num + nums[left] + nums[right]

            # check if sum is less than 0, increment left
            if result < 0:
                left += 1

            # check if sum is greater than 0, decrement right
            elif result > 0:
                right -= 1

            # If zero, add to the res and increment the left
            else:
                res.append([num, nums[left], nums[right]])
                left += 1

                # Skip the duplicates again
                if left < right and nums[left] == nums[left - 1]:
                    left += 1

    # return res
    return res

```

###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.

- [[Space Complexity]] : O(1)
- [[Time Complexity]] : O(n^2)

<img src="img/problem 15.png"/>


###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.

#### Related 
1. [[DSA Strategy]]
2. [[Space Complexity]]
3. [[Time Complexity]]
4. [[Big O Notation]]
#### References
1. [Roadmap (neetcode.io)](https://neetcode.io/roadmap)
