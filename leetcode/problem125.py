def is_palindrome(s: str):

    left = 0
    right = len(s) - 1

    # Start pointers from start and end
    while left < right:

        # Check if the charater is alpha numeric, move pointers
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        # It is a palindrome only when both pointers are equal all the time
        elif s[left].lower() == s[right].lower():
            left += 1
            right -= 1
        else:
            return False

    return True
