### Problem 
Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
**Problem**
- Open brackets must be closed by the same type of character in the correct order 
- Every closing bracket has a corresponding open bracket 
**Input**
String of characters containing `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`
**Output**
True if conditions are met, False if not met 
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```
Input: s = "()"
Output: true

Input: s = "()[]{}"
Output: true

Input: s = "(]"
Output: false
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
1. Parse the string and add the opening parenthesis to a list 
2. Create a dictionary with mapping for closing parentheses 
3. Use the stacks (LIFO) and for the closing parenthesis, check the last item of the list, if they match, remove it from the list 
	1. We will be looking for the closing char
	2. If the closing char is present, check the last item of the list. If it is not the same, it means that the brackets are not closed properly
4. Check if the list is empty at the end of the operation. If all the closing parentheses are accounted for, the list will be empty 
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.
```python
def valid_parentheses(s: str):
    # 1. Parse the string and add the opening parenthesis to a list
    stack = []
    mapping = {
        "}": "{",
        "]": "[",
        ")": "(",
    }
    # 2. Create a dictionary with mapping for closing parentheses

    # 3. Use the stacks (LIFO) and for the closing parenthesis, check the last item of the list, if they match, remove it from the list
    for char in s:
        # We will be looking for the closing char
        # If the closing char is present, check the last item of the list. If it is not the same, it means that the brackets are not closed properly
        if char in mapping:
            if stack and stack[-1] == mapping[char]:
                stack.pop()
            else:
                return False
        else:
            # We will be adding the opening characters here
            stack.append(char)

    return True if not stack else False

```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
- Time complexity: O(n), where n is the length of the input string `s`.
###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.

<img src="img/problem 20.png"/>
