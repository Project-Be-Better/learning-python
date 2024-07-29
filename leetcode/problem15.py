def three_sum(nums):
    res = []
    nums.sort()

    # enumerate
    for index, num in enumerate(nums):

        # skip the duplicate number
        if index > 0 and nums[index] == nums[index - 1]:
            continue

        # two pointers left and right
        left, right = index + 1, len(nums) - 1

        while left < right:
            result = num + nums[left] + nums[right]

            # check if sum is less than 0, increment left
            if result < 0:
                left += 1

            # check if sum is greater than 0, decrement right
            elif result > 0:
                right -= 1

            # If zero, add to the res and increment the left
            else:
                res.append([num, nums[left], nums[right]])
                left += 1

                # Skip the duplicates again
                if left < right and nums[left] == nums[left - 1]:
                    left += 1

    # return res
    return res
