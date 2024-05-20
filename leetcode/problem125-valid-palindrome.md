### Problem 
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.
 
```


Example 1:

Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
Example 2:

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
Example 3:

Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.
```
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.

> [!info]  Problem 
```
Check if the given string is a palindrome 
```


> [!tip] Input
```
A string s 
```


> [!check] Output 
```
- True if string palindrome after converting all the characters to lowercase and removing the non alpha numeric characters 
- False if not a palindrome 
```
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```python
import unittest
from problem125 import is_palindrome


class TestProblem125(unittest.TestCase):

    def test_is_palindrome(self):

        input = "A man, a plan, a canal: Panama"
        output = is_palindrome(input)
        self.assertTrue(output)

        input = "race a car"
        output = is_palindrome(input)
        self.assertFalse(output)

        input = " "
        output = is_palindrome(input)
        self.assertTrue(output)

```
###### 3. Come up with a correct solution for the problem. State it in plain English.
We will be solving it with [[(algo) Two Pointer Technique|Two Pointer Technique]]
1. Start two pointers, left and right. 
2. Check if each character is alphanumeric, if not, move pointers to left and right respectively 
3. If both characters are equal, then update both pointers
4. It is not a palindrome if the characters are not equal, so return False 
5. Return True otherwise, because the given string is a palindrome 
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.

> [!done] Solution
```python
def is_palindrome(s: str):

    left = 0
    right = len(s) - 1

    # Start pointers from start and end
    while left < right:

        # Check if the charater is alpha numeric, move pointers
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        # It is a palindrome only when both pointers are equal all the time
        elif s[left].lower() == s[right].lower():
            left += 1
            right -= 1
        else:
            return False

    return True

```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
- Time Complexity: The time complexity of the algorithm is O(n), where n is the length of the string `s`. This is because we iterate through the string only once.
- Space Complexity: The space complexity is O(1), as we are using only a constant amount of extra space.
###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.
- We can use a string reversal after removing the spaces, but it is not efficient 

#### Related 
1. [[DSA Strategy]]
2. [[(algo) Two Pointer Technique|Two Pointer Technique]]
#### References
1. [Roadmap (neetcode.io)](https://neetcode.io/roadmap)
2. [Valid Palindrome - Leetcode 125 - Python (youtube.com)](https://www.youtube.com/watch?v=jJXJ16kPFWg)

<img src="img/problem 125.png"/>
