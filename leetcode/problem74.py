from typing import List


def search_matrix(matrix: List[List[int]], target: int):

    rows = len(matrix)
    cols = len(matrix[0])

    top_row = 0
    bottom_row = rows - 1

    # Binary search through the arrays in the matrix
    while top_row <= bottom_row:

        # Find the middle row
        mid_row = (top_row + bottom_row) // 2

        # Target is greater than the end of the array
        if target > matrix[mid_row][-1]:
            top_row = mid_row + 1

        # Target is smaller than the start of the array
        elif target < matrix[mid_row][0]:
            bottom_row = mid_row - 1

        # Target is in this array
        else:
            break

    # If the row is not found, return false
    if not (top_row <= bottom_row):
        return False

    # Binary search the selected array in the matrix
    left = 0
    right = cols - 1

    while left <= right:
        mid = (left + right) // 2
        guess_value = matrix[mid_row][mid]

        # Return is guess is correct
        if guess_value == target:
            return True

        # Check if guess is too high
        if guess_value > target:
            right = mid - 1

        # Check if guess is too low
        else:
            left = mid + 1

    return False


if __name__ == "__main__":
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    target = 3
    rlt = search_matrix(matrix, target)
