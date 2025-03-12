# a farmer wants to farm their land where the maximum area of good land is available.
# the land is represented as a matrix with 1s and 0s, where 1 represents good land and 0 represents bad land.
# the farmer wants to only farm in a square of good land with the maximum area.
# help the farmer to find the maximum area of the land they can farm in good land.

# this is the land matrix
# 01101
# 11010
# 01110
# 11110
# 01111
# 00000



def max_square_area(matrix):
    """
    Finds the maximum area of a square of good land (represented by 1s) in a matrix.

    Args:
        matrix: A list of lists representing the land.

    Returns:
        The maximum area of a square of good land, or 0 if no good land is found.
    """

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    max_side = 0

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == '1':
                # Start with a 1x1 square
                current_side = 1

                # Expand the square as long as possible
                while i + current_side < rows and j + current_side < cols:
                    is_square = True
                    for x in range(i, i + current_side + 1):
                        for y in range(j, j + current_side + 1):
                            if matrix[x][y] == '0':
                                is_square = False
                                break
                        if not is_square:
                            break
                    if is_square:
                        current_side += 1
                    else:
                        break

                max_side = max(max_side, current_side)

    return max_side * max_side


def max_rectangle_area(matrix):
    """
    Finds the maximum area of a rectangle of good land (represented by 1s) in a matrix.

    Args:
        matrix: A list of lists representing the land.

    Returns:
        The maximum area of a rectangle of good land, or 0 if no good land is found.
    """

    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    max_area = 0

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == '1':
                # Initialize the width and height of the rectangle
                width = 0
                height = 0

                # Expand the rectangle to the right
                while j + width < cols and matrix[i][j + width] == '1':
                    width += 1

                # Expand the rectangle downwards
                for k in range(width):
                    current_height = 0
                    while i + current_height < rows and matrix[i + current_height][j + k] == '1':
                        current_height += 1
                    height = max(height, current_height)

                # Calculate the area of the rectangle
                max_area = max(max_area, width * height)

    return max_area


land = [
    "01101",
    "11010",
    "01110",
    "11110",
    "01111",
    "00000",
]

# Convert the land matrix to a list of lists of characters
land_matrix = [list(row) for row in land]

max_area_square = max_square_area(land_matrix)
max_area_rectangle = max_rectangle_area(land_matrix)
print(f"The maximum area of farmable land (square) is: {max_area_square}")
print(
    f"The maximum area of farmable land (rectangle) is: {max_area_rectangle}")
