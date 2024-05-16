class Solution(object):
    def evalRPN(self, tokens):
        """
        :type tokens: List[str]
        :rtype: int
        """
        # Parse through the array
        # We will be using a stack for this. we will read from the list and add to the stack
        stack = []

        for token in tokens:
            flag = self.is_operator(token)

            if flag:
                # As soon as we encounter an operator, we will pop the last two entries and perform the operation and add it back to the stack

                # perform the operation and add to the array

                b = stack.pop()
                a = stack.pop()

                if token == "*":
                    stack.append(a * b)
                elif token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "/":
                    stack.append(int(a / b))

            else:
                # Add to the stack
                stack.append(int(token))

        # Finally return the value
        return stack.pop()

    def is_operator(self, item):
        return item in ["+", "-", "*", "/"]
