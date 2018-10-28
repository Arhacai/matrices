
def determinant(matrix):
    if matrix.rows != matrix.columns:
        raise IndexError(
            "Matrix determinant can only be calculated on square matrices."
        )
    result = 0
    if matrix.rows == 1:
        return matrix.element(0, 0)
    for row in range(matrix.rows):
        result += matrix.element(row, 0) * adjoint(matrix, row, 0)
    return result


def identity(size):
    result = []
    for row in range(size):
        result.append([])
        for column in range(size):
            if row == column:
                result[row].append(1)
            else:
                result[row].append(0)
    return Matrix(result)


def minor(matrix, i, j):
    from copy import deepcopy
    matrix = deepcopy(matrix.matrix)
    for row in matrix:
        del row[j]
    del matrix[i]
    return determinant(Matrix(matrix))


def adjoint(matrix, row, column):
    return pow(-1, row+column) * minor(matrix, row, column)


def adjoint_matrix(matrix):
    result = []
    for row in range(matrix.rows):
        result.append([])
        for column in range(matrix.columns):
            result[row].append(adjoint(matrix, row, column))
    return Matrix(result)


def inverse(matrix):
    if matrix.rows != matrix.columns:
        raise ValueError(
            "Inverse matrix can only be calculated on square matrices."
        )
    det = determinant(matrix)
    if det == 0:
        raise ValueError("This matrix has no inverse.")
    return int(1/det) * transpose(adjoint_matrix(matrix))


def transpose(matrix):
    result = []
    for row in range(matrix.columns):
        result.append([])
        for column in range(matrix.rows):
            result[row].append(matrix.element(column, row))
    return Matrix(result)


class Matrix:

    def __init__(self, matrix=None):
        if matrix is None:
            matrix = self.get_values()
        self.matrix, self.rows, self.columns = self.get_matrix(matrix)

    @staticmethod
    def get_values():
        values = input("Values? (Use '; ' to separate each row) ").split("; ")
        return [[int(column) for column in row.split(" ")] for row in values]

    def get_matrix(self, matrix):
        if type(matrix) != str and type(matrix) != list:
            raise ValueError("You must introduce a matrix as a string or list")
        if type(matrix) == str:
            values = matrix.split("; ")
            matrix = [[int(column) for column in row.split(" ")] for row in values]
        rows = len(matrix)
        columns = len(matrix[0])
        for row in matrix:
            if len(row) != columns:
                raise ValueError(
                    "All rows must have the same number of columns"
                )
        return matrix, rows, columns

    def element(self, row, column):
        return self.matrix[row][column]

    def __add__(self, other):
        result = []
        for row in range(self.rows):
            result.append([])
            for column in range(self.columns):
                if type(other) == int:
                    result[row].append(self.element(row, column) + other)
                else:
                    result[row].append(
                        self.element(row, column) + other.element(row, column)
                    )
        return Matrix(result)

    def __sub__(self, other):
        result = []
        for row in range(self.rows):
            result.append([])
            for column in range(self.columns):
                if type(other) == int:
                    result[row].append(self.element(row, column) - other)
                else:
                    result[row].append(
                        self.element(row, column) - other.element(row, column)
                    )
        return Matrix(result)

    def __mul__(self, other):
        result = []
        for row in range(self.rows):
            result.append([])
            if type(other) == int:
                for column in range(self.columns):
                    result[row].append(self.element(row, column) * other)
            else:
                if self.columns != other.rows:
                    raise ValueError("This matrices can't be multiplied.")
                for column in range(other.columns):
                    result[row].append(0)
                    for index in range(self.columns):
                        aij = self.element(row, index)
                        bji = other.element(index, column)
                        result[row][column] += aij * bji
        return Matrix(result)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        str_matrix = []
        for row in range(self.rows):
            str_matrix.append([])
            for column in range(self.columns):
                if self.element(row, column) >= 0:
                    str_matrix[row].append(
                        ' ' + str(self.element(row, column))
                    )
                else:
                    str_matrix[row].append(str(self.element(row, column)))

        result = []
        for row in str_matrix:
            result.append(
                "( {}  )".format(' '.join([element for element in row]))
            )
        return '\n'.join(result)

    def __eq__(self, other):
        return self.matrix == other.matrix


def first_exercise():
    # A = Matrix([[-1, 2, 4, 0], [3, 2, -1, -3], [6, 0, 1, 1]])
    A = Matrix("-1 2 4 0; 3 2 -1 -3; 6 0 1 1")
    B = Matrix([[2, 1], [1, 0], [-3, -2], [0, 3]])
    print("First Exercise:")
    print("a) A x B")
    print(A*B)
    print("\n(A x B)t = Br x At")
    print(transpose(A*B) == transpose(B)*transpose(A))


def third_exercise():
    A = Matrix([[1, 4], [1, 3]])
    B = Matrix([[4, 0], [1, 2]])

    print("Third Exercise:")
    print("a) AXA = AB")
    print("Sol:")
    print("A'AXAA' = AA'BA'")
    print("IXI = IBA'")
    print("X = BA'")
    print(B * inverse(A))

if __name__ == '__main__':

    first_exercise()
    third_exercise()