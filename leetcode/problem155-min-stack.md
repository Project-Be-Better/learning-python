### Problem 
Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the `MinStack` class:

- `MinStack()` initializes the stack object.
- `void push(int val)` pushes the element `val` onto the stack.
- `void pop()` removes the element on the top of the stack.
- `int top()` gets the top element of the stack.
- `int getMin()` retrieves the minimum element in the stack.

You must implement a solution with `O(1)` time complexity for each function.
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.

> [!abstract]  Problem
```
1. Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
2. This has to be O(1), so has to be linear operation 
```

###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```
Example 1:

Input
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

Output
[null,null,null,null,-3,null,0,-2]

Explanation
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // return -3
minStack.pop();
minStack.top();    // return 0
minStack.getMin(); // return -2
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
1. We can use two stacks, one named `stack` for storing the elements and another one for tracking the minimum value named `min_stack`
2. When pushing element on the `stack`, add a corresponding element in the `min_stack` as well.
3. When popping the element from stack, pop the top element from `min_stack` 
4. for `get_min`, get the top element of the `min_stack`
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.
```python 
class MinStack(object):

    def __init__(self):
        """
        Initialises the stack object
        """
        self.stack = []
        self.min_stack = []

    def push(self, val):
        """
        Pushes the element val onto the stack.
        :type val: int
        :rtype: None
        """
        # Append to stack as well as minstack

        self.stack.append(val)
        val = min(
            val,
            (self.min_stack[-1] if self.min_stack else val),
        )
        self.min_stack.append(val)

    def pop(self):
        """
        Removes the element on the top of the stack.
        :rtype: None
        """
        # Removes the top element from both lists at the same time
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        """
        Gets the top element of the stack
        :rtype: int
        """
        return self.stack[-1]

    def get_min(self):
        """
        Retrieves the minimum element in the stack.
        :rtype: int
        """
        return self.min_stack[-1]

```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.
- The time complexity for all operations (`push`, `pop`, `top`, and `getMin`) is O(1) because each operation involves only stack operations, which have constant time complexity.

<img src="img/problem 155.png"/>



#### Related 
1. [[DSA Strategy]] 
#### References
1. [Roadmap (neetcode.io)](https://neetcode.io/roadmap)
2. [Design Min Stack - Amazon Interview Question - Leetcode 155 - Python (youtube.com)](https://www.youtube.com/watch?v=qkLl7nAwDPo)