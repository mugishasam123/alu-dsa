from SparseMatrix import SparseMatrix
import os

def menu():
    """
    Display the menu to select the matrix operation.
    """
    print("Matrix Operations:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    return int(input("Select an operation (1/2/3): "))


def main():
    """
    Main function to handle input, perform operations, and save output.
    """
    try:
        matrix1_file = input("Enter path for first matrix file (default: 'easy_sample_01_1.txt'): ") or 'easy_sample_01_1.txt'
        matrix2_file = input("Enter path for second matrix file (default: 'easy_sample_01_2.txt'): ") or 'easy_sample_01_2.txt'
        output_file = input("Enter path for the output file (default: 'result.txt'): ") or 'result.txt'

        input_base_path = 'dsa/sparse_matrix/sample_inputs'
        matrix1_file_path = os.path.join(input_base_path, matrix1_file)
        matrix2_file_path = os.path.join(input_base_path, matrix2_file)
        output_file_path = os.path.join('dsa/sparse_matrix/sample_results', output_file)

        print(f"{matrix1_file_path} {matrix2_file_path} {output_file_path}")
        matrix1 = SparseMatrix(matrix1_file_path)
        matrix2 = SparseMatrix(matrix2_file_path)

        operation = menu()

        if operation == 1:
            result = matrix1 + matrix2
        elif operation == 2:
            result = matrix1 - matrix2
        elif operation == 3:
            result = matrix1 * matrix2
        else:
            raise ValueError("Invalid operation selected")

        result.save_to_file(output_file_path)
        print(f"Result saved to {output_file_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
