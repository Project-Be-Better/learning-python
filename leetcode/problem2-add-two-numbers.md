### Problem 
You are given two **non-empty** [[linked list]]s representing two non-negative integers. The digits are stored in **reverse order**, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.





**Constraints:**
- The number of nodes in each linked list is in the range `[1, 100]`.
- `0 <= Node.val <= 9`
- It is guaranteed that the list represents a number that does not have leading zeros.

### Usage 
```python 
# Example 1:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.

# Example 2:
Input: l1 = [0], l2 = [0]
Output: [0]

# Example 3:
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
```
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
- Given two non empty linked lists representing non negative integers 
- Digits are reversed 
- Each node contains one digit 
- Sum is a linked list 
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```python
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
Example 2:

Input: l1 = [0], l2 = [0]
Output: [0]
Example 3:

Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
1. Start with dummy node to server as the head of resulting linked list 
2. Initialize a carry variable as 0 
3. Parse the two linked lists at the same time 
4. Carry is sum of nodes // 10 and value to be copied over is sum of nodes % 10 
5. Move over the nodes of linked lists, l1 and l2 to next node 
6. Create a next List node with value to be copied , set it as the current node 
7. Return the next node of the dummy node

###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.
```python
class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:

        carry = 0
        dummy_node = ListNode()
        current_node = dummy_node

        # Parse the linked list
        while l1 or l2 or carry:

            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            sum_total = v1 + v2 + carry 
            carry = sum_total // 10
            val_to_be_copied = sum_total % 10 

            current_node.next = ListNode(val_to_be_copied)
            current_node = current_node.next
            
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy_node.next
```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.


<img src="img/problem 2.png"/>
