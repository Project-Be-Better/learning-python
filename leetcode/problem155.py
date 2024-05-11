class MinStack(object):

    def __init__(self):
        """
        Initialises the stack object
        """
        self.stack = []
        self.min_stack = []

    def push(self, val):
        """
        Pushes the element val onto the stack.
        :type val: int
        :rtype: None
        """
        # Append to stack as well as minstack

        self.stack.append(val)
        val = min(
            val,
            (self.min_stack[-1] if self.min_stack else val),
        )
        self.min_stack.append(val)

    def pop(self):
        """
        Removes the element on the top of the stack.
        :rtype: None
        """
        # Removes the top element from both lists at the same time
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        """
        Gets the top element of the stack
        :rtype: int
        """
        return self.stack[-1]

    def get_min(self):
        """
        Retrieves the minimum element in the stack.
        :rtype: int
        """
        return self.min_stack[-1]
