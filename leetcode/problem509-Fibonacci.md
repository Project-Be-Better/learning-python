### Problem 
The **Fibonacci numbers**, commonly denoted `F(n)` form a sequence, called the **Fibonacci sequence**, such that each number is the sum of the two preceding ones, starting from `0` and `1`. That is,

F(0) = 0, F(1) = 1
F(n) = F(n - 1) + F(n - 2), for n > 1.

Given `n`, calculate `F(n)`.
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
- Find the nth Fibonacci number 
- Input is a single digit n 
- Output is a single integer representing the nth Fibonacci number 
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.

> [!tip] Input
```
Example 1:

Input: n = 2
Output: 1
Explanation: F(2) = F(1) + F(0) = 1 + 0 = 1.
Example 2:

Input: n = 3
Output: 2
Explanation: F(3) = F(2) + F(1) = 1 + 1 = 2.
Example 3:

Input: n = 4
Output: 3
Explanation: F(4) = F(3) + F(2) = 2 + 1 = 3.
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
- If n is 0, return 0  
- If n is 1, return 1 
-  For n ≥ 2, F(n) = F(n-1) + F(n-2)
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.

> [!done] Solution
```python
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_recursion(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    return fibonacci_recursion(n - 1) + fibonacci_recursion(n - 2)

```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
- [[Space Complexity]] : we have a constant amount of space regardless of the input size 
- [[Time Complexity]] : O(n) as we compute the sequence in a single loop 

<img src="img/problem 509.png"/>

###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.
Current solution is optimised 
#### Related 
1. [[DSA Strategy]]
2. [[Space Complexity]]
3. [[Time Complexity]]
4. [[Big O Notation]]
#### References
1. [Roadmap (neetcode.io)](https://neetcode.io/roadmap)
