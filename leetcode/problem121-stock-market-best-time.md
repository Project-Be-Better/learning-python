### Problem 
- You are given an array `prices` where `prices[i]` is the price of a given stock on the `ith` day.
- You want to maximise your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.
- Return _the maximum profit you can achieve from this transaction_. If you cannot achieve any profit, return `0`.
### Notes 
###### 1. State the problem clearly. Identify the input & output formats.
- Array of stock prices where stock price for ith day is `prices[i]`
- Maximise the profit possible in the given time period 
- If we cannot achieve any profit, return 0 
###### 2. Come up with some example inputs & outputs. Try to cover all edge cases.

> [!tip] Input
```
Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
Example 2:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.
```

###### 3. Come up with a correct solution for the problem. State it in plain English.
- Initialise two pointers, buy and sell. Buy will be for the first day and sell for the second day 
- Initialise max_p for recording maximum profit.
- Iterate through the list using sell pointer. 
	- Check if the transaction yield any net profit. 
	- If there is net profit (>0), compare it with the current max profit and store
	- If the profit is not positive, move the buy to sell 
	- move the sell to the next day 
- Return the maximum profit 
###### 4. Implement the solution and test it using example inputs. Fix bugs, if any.

> [!done] Solution
```python
def max_profit(prices: List[int]) -> int:
    buy, sell = 0, 1
    max_p = 0

    while sell < len(prices): 

        profit = prices[sell] - prices[buy]

        if profit > 0 : 
            max_p = max(max_p,profit)
        else: 
            buy = sell 

        # Move the pointer right for the sell
        sell += 1  

        print("buy :", buy, "sell :", sell, "profit :", max_p)

    return max_p
```

###### 5. Analyze the algorithm's complexity and identify inefficiencies, if any.
- [[Time Complexity]] : O(n)
- [[Space Complexity]] : O(1)

**Input Data:**
- The input is a list of integers `prices`, representing stock prices. The memory occupied by this input does not count towards the algorithm's space complexity because it's given as part of the problem statement.
**Additional Variables:**
- **`buy` and `sell`:** These are integer variables used to track indices in the `prices` list.
- **`max_p`:** An integer variable to store the maximum profit found so far.
- **`profit`:** A temporary variable used to calculate the profit for the current pair of days.

<img src="img/problem 121.png"/>


###### 6. Apply the right technique to overcome the inefficiency. Repeat steps 3 to 6.

#### Related 
1. [[DSA Strategy]]
#### References
1. [Roadmap (neetcode.io)](https://neetcode.io/roadmap)