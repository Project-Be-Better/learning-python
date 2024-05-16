### Problem 
You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.
Evaluate the expression. Return an integer that represents the value of the expression.

Note that:
The valid operators are '`+`', '`-`', '`*`', and '`/'`.
Each operand may be an integer or another expression.
The division between two integers always truncates toward zero.
There will not be any division by zero.
The input represents a valid arithmetic expression in a reverse polish notation.
The answer and all the intermediate calculations can be represented in a 32-bit integer.
 
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.

> [!info]  Problem 
```
- An array of strings that are given in reverse polish notatation 
- Evaluate the expression and return an integer that represents the value of the expression 
```


> [!tip] Input
```
An array of strings which are a mix of operators and int 
```


> [!check] Output 
```
Integer representing the result 
```
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```python
Example 1:

Input: tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9
Example 2:

Input: tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6
Example 3:

Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
Output: 22
Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
1. Parse through the array
2. We will be using a stack for this. we will read from the list and add to the stack
3. As soon as we encounter an operator, we will pop the last two entries and perform the operation and add it back to the stack
4. perform the operation and add to the array
5. Finally return the value
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.

> [!done] Solution
```python
class Solution(object):
    def evalRPN(self, tokens):
        """
        :type tokens: List[str]
        :rtype: int
        """
        # Parse through the array
        # We will be using a stack for this. we will read from the list and add to the stack
        stack = []

        for token in tokens:
            flag = self.is_operator(token)

            if flag:
                # As soon as we encounter an operator, we will pop the last two entries and perform the operation and add it back to the stack

                # perform the operation and add to the array

                b = stack.pop()
                a = stack.pop()

                if token == "*":
                    stack.append(a * b)
                elif token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "/":
                    stack.append(int(a / b))

            else:
                # Add to the stack
                stack.append(int(token))

        # Finally return the value
        return stack.pop()

    def is_operator(self, item):
        return item in ["+", "-", "*", "/"]

```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
- Time Complexity: O(n), where n is the number of tokens in the input array. This is because each token is processed once.
- Space Complexity: O(n), where n is the number of tokens. This is due to the stack used to store operands.
###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.


<img src="img/problem 150.png"/>

#### Related 
1. [[DSA Strategy]]
2. [[Stacks]]
#### References
1. [Roadmap (neetcode.io)](https://neetcode.io/roadmap)
2. [Reverse Polish notation - Wikipedia](https://en.wikipedia.org/wiki/Reverse_Polish_notation)
3. [Evaluate Reverse Polish Notation - Leetcode 150 - Python (youtube.com)](https://www.youtube.com/watch?v=iu0082c4HDE)