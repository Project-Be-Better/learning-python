### Problem 
Given the `head` of a linked list, remove the `nth` node from the end of the list and return its head

### Usage 
```python 
#Example 1:
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
#Example 2:
Input: head = [1], n = 1
Output: []
#Example 3:
Input: head = [1,2], n = 1
Output: [1]
```
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
**Input**: 
Takes the head of a linked list and an integer n 
**Output**:
Return the head of the linked list after removing the nth node from the end of the list 
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.
```python 
#Example 1:
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
#Example 2:
Input: head = [1], n = 1
Output: []
#Example 3:
Input: head = [1,2], n = 1
Output: [1]
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
![[(leetcode)19. Remove Nth Node From End of List-1.png]]
1. Use Two pointer technique 
2. Initialize the two pointers, left and right. Left will he the head of the linked list and right will be immediate next node 
3. Move the right pointer to the right by n nodes 
4. Now move the pointers simultaneously until the right pointer reaches the end. 
5. Now, the node next to the left pointer is the one to be removed 
6. Move the pointer from left to the skip its next node 
7. Return the head of the linked list
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.
```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy_node = ListNode(0,head)

        left = dummy_node
        right = head 

        # Push the right pointer until to n nodes from the head 
        while n > 0 and right: 
            right = right.next 
            n -= 1 
            print(f"right {right.val}")
        

        # Traverse the list until the right pointer reaches null
        while right: 
            left = left.next 
            right = right.next

            l1 = left.val if left else None 
            r1 = right.val if right else None 
            print(f"left : {l1} right : {r1}")


        # delete the next node to the left pointer  
        left.next = left.next.next 

        # Return the next of the dummy node 
        return dummy_node.next
```

###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
Time complexity is [[Big O Notation#O(n) - Linear Time |O(n)]] 

###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.


<img src="img/problem 19.png"/>

#### Related 
1. [[DSA Strategy]]
2. [[Big O Notation]]



#### References
1. [Remove Nth Node from End of List - Oracle Interview Question - Leetcode 19 (youtube.com)](https://www.youtube.com/watch?v=XVuQxVej6y8)