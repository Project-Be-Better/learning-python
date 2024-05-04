def contains_duplicate(nums):
    """
    Checks if an array contains any duplicates
    """
    # Checks the length of the array with a set from the same array
    unique_array = list(set(nums))

    # Returns True if there are duplicates
    return not len(nums) == len(unique_array)
