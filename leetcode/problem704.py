from typing import List


def search(nums: List[int], target: int) -> int:

    left = 0
    right = len(nums) - 1

    # While there is only one element left
    while left <= right:

        mid = (left + right) // 2
        guess = nums[mid]

        # Guess matches the target
        if guess == target:
            return mid

        # Guess is too high, lowering right side
        if guess > target:
            right = mid - 1

        # Guess is too low, incrementing left side
        else:
            left = mid + 1

    # No Matches found
    return -1
