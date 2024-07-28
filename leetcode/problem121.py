from typing import List


def max_profit(prices: List[int]) -> int:
    buy, sell = 0, 1
    max_p = 0

    while sell < len(prices):

        profit = prices[sell] - prices[buy]

        if profit > 0:
            max_p = max(max_p, profit)
        else:
            buy = sell

        # Move the pointer right for the sell
        sell += 1

    return max_p
