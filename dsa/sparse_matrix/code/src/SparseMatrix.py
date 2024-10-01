class SparseMatrix:
    """A class representing a sparse matrix."""

    def __init__(self, file_path=None, rows=0, cols=0):
        """
        Initialize a SparseMatrix.
        Args:
            file_path (str): Path to the file containing matrix data (optional).
            rows (int): Number of rows in the matrix.
            cols (int): Number of columns in the matrix.
        """
        self.num_rows = rows
        self.num_cols = cols
        self.elements = {} 
        
        if file_path:
            self.read_matrix(file_path)

    def read_matrix(self, file_path):
        """
        Read a sparse matrix from a file and populate the matrix.
        Args:
            file_path (str): Path to the input file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.num_rows = int(file.readline().split('=')[1])
                self.num_cols = int(file.readline().split('=')[1])

                for line in file:
                    line = line.strip()
                    if line and line.startswith('('):
                        line = line.strip('()').split(',')
                        row, col, value = int(line[0]), int(line[1]), int(line[2])
                        self.set_element(row, col, value)
        except Exception as e:
            print(e)
            raise ValueError("Input file has wrong format") from e

    def set_element(self, row, col, value):
        """
        Set an element in the matrix. Adds it if non-zero, removes if zero.
        Args:
            row (int): The row index.
            col (int): The column index.
            value (int): The value to set.
        """
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)] 

    def get_element(self, row, col):
        """
        Get an element from the matrix.
        Args:
            row (int): The row index.
            col (int): The column index.
        Returns:
            int: The value at the specified position, or 0 if not found.
        """
        return self.elements.get((row, col), 0)

    def __add__(self, other):
        """
        Perform element-wise addition of two matrices.
        Args:
            other (SparseMatrix): The matrix to add.
        Returns:
            SparseMatrix: The resulting matrix from the addition.
        """
        return self._elementwise_operation(other, operation="add")

    def __sub__(self, other):
        """
        Perform element-wise subtraction of two matrices.
        Args:
            other (SparseMatrix): The matrix to subtract.
        Returns:
            SparseMatrix: The resulting matrix from the subtraction.
        """
        return self._elementwise_operation(other, operation="sub")

    def __mul__(self, other):
        """
        Perform matrix multiplication.
        Args:
            other (SparseMatrix): The matrix to multiply with.
        Returns:
            SparseMatrix: The resulting matrix from the multiplication.
        """
        if self.num_cols != other.num_rows:
            raise ValueError("Matrix multiplication not possible, column of first must match rows of second")
        
        result = SparseMatrix(rows=self.num_rows, cols=other.num_cols)
        for (i, k), v in self.elements.items():
            for j in range(other.num_cols):
                if (k, j) in other.elements:
                    result.set_element(i, j, result.get_element(i, j) + v * other.elements[(k, j)])
        return result

    def _elementwise_operation(self, other, operation):
        """
        Perform element-wise addition or subtraction of two matrices.
        Args:
            other (SparseMatrix): The other matrix to operate on.
            operation (str): The operation type ("add" or "sub").
        Returns:
            SparseMatrix: The resulting matrix from the operation.
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices must have the same dimensions for addition/subtraction")
        
        result = SparseMatrix(rows=self.num_rows, cols=self.num_cols)
        
        all_keys = set(self.elements.keys()).union(set(other.elements.keys()))
        
        for key in all_keys:
            self_value = self.get_element(key[0], key[1])
            other_value = other.get_element(key[0], key[1])
            
            if operation == "add":
                result_value = self_value + other_value
            elif operation == "sub":
                result_value = self_value - other_value
            else:
                raise ValueError("Unsupported operation")

            result.set_element(key[0], key[1], result_value)
        
        return result

    def save_to_file(self, output_file):
        """
        Save the sparse matrix to a file.
        Args:
            output_file (str): Path to the output file.
        """
        with open(output_file, 'w') as file:
            file.write(f"rows={self.num_rows}\n")
            file.write(f"cols={self.num_cols}\n")
            
            for (row, col), value in sorted(self.elements.items()):
                file.write(f"({row}, {col}, {value})\n")
