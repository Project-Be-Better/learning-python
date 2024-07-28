### Problem 
Given two strings `s` and `t`, return `true` _if_ `t` _is an anagram of_ `s`_, and_ `false` _otherwise_.

An **Anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
- Anagram are words are formed using the exact letters of the same word, just changing the order 
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.

> [!tip] Input
```
Example 1:

Input: s = "anagram", t = "nagaram"
Output: true
Example 2:

Input: s = "rat", t = "car"
Output: false
```
###### 3. Come up with a correct solution for the problem. State it in plain English.
- Check the length of the strings, if they are not of the same length, exit 
- Create a dictionary with the letters of the word. As soon as a word is found add it to the dictionary and increment the value by 1 
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.

> [!done] Solution 1 
```python
def is_anagram_longer(s: str, t: str) -> bool:
    """
    Returns True if both strings are anagrams
    """

    # convert string to dict
    def convert_to_dict(str_to_convert):
        dict_holder = {}
        for i in str_to_convert:
            dict_holder[i] = dict_holder.get(i, 0) + 1

        return dict_holder

    dict_s = convert_to_dict(s)
    dict_t = convert_to_dict(t)

    return dict_s == dict_t
```

> [!danger] Solution 2 
```python
# Involved sorting and sorting has time complexity of O(m log m)
def is_anagram(s: str, t: str) -> bool:
    """
    Returns True if both strings are anagrams
    """
    return sorted(s) == sorted(t)
```
###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
<img src="img/problem 242-1.png"/>
Solution for sorted : Less Efficient
<img src="img/problem 242-2.png"/>

###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.

#### Related 
1. [[DSA Strategy]]
2. [[Space Complexity]]
3. [[Time Complexity]]
4. [[Big O Notation]]
#### References
1. [Roadmap (neetcode.io)](https://neetcode.io/roadmap)
