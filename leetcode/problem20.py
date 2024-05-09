def valid_parentheses(s: str):
    # 1. Parse the string and add the opening parenthesis to a list
    stack = []
    mapping = {
        "}": "{",
        "]": "[",
        ")": "(",
    }
    # 2. Create a dictionary with mapping for closing parentheses

    # 3. Use the stacks (LIFO) and for the closing parenthesis, check the last item of the list, if they match, remove it from the list
    for char in s:
        # We will be looking for the closing char
        # If the closing char is present, check the last item of the list. If it is not the same, it means that the brackets are not closed properly
        if char in mapping:
            if stack and stack[-1] == mapping[char]:
                stack.pop()
            else:
                return False
        else:
            # We will be adding the opening characters here
            stack.append(char)

    return True if not stack else False
