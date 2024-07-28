def twoSum(nums, target):
    compliment_dict = {}

    for i, num in enumerate(nums):
        compliment = target - num

        if compliment in compliment_dict:
            return [compliment_dict[compliment], i]

        compliment_dict[num] = i
