def remove_empty_rows_columns(matrix_restored):
    # Find empty rows and columns
    empty_rows = [i for i, row in enumerate(matrix_restored[1:]) if all(cell == [] for cell in row[1:])]
    empty_columns = [j for j in range(len(matrix_restored[0])) if all(matrix_restored[i][j] == [] for i in range(1, len(matrix_restored)))]

    # Remove empty rows
    for i in reversed(empty_rows):
        del matrix_restored[i + 1]

    # Remove empty columns
    for j in reversed(empty_columns):
        for row in matrix_restored:
            del row[j]

    return matrix_restored

# Example usage:
matrix = [
    ['', 'A', 'B', 'C', 'D'],
    ['A', [1], [], [2], []],
    ['B', [], [], [], []],
    ['C', [2], [], [], []],
    ['D', [3], [], [9], []]
]

result = remove_empty_rows_columns(matrix)
for i in result:
    print(i)
