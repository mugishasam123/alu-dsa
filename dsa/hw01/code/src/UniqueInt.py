import os
import time
import psutil
import sys

class UniqueInt:
    """
    A class to process files and extract unique integers from a specified range (-1023 to 1023).
    """

    def __init__(self):
        # Boolean array of size 2047 to represent the integers from -1023 to 1023
        self.seen = [False] * 2047

    def process_file(self, input_file_name, output_file_name):
        """
        Reads integers from the input file, identifies unique integers, sorts them, 
        and writes them to the output file.
        :param input_file_name: Name of the input file containing integers.
        :param output_file_name: Name of the output file where unique integers will be written.
        """
        try:
            input_file_path = self.get_file_path(input_file_name)
            output_file_path = self.get_file_path(output_file_name)

            # Collect unique numbers
            for line in self.read_input_file(input_file_path):
                line = line.strip()

                try:
                    number = int(line)
                    if -1023 <= number <= 1023 and not self.is_seen(number):
                        self.mark_as_seen(number)
                except ValueError:
                    # Skipping invalid lines that cannot be converted to int
                    continue
            
            # Write unique numbers directly to the output file as they are found
            self.write_unique_numbers_directly(output_file_path)

        except FileNotFoundError:
            print(f"Error: File '{input_file_name}' not found.")
        except OSError as e:
            print(f"File error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def is_seen(self, number):
        """
        Checks if a number has been seen before using the boolean array.
        :param number: The integer to check.
        :return: True if the number has been seen before, False otherwise.
        """
        index = number + 1023  # Adjust number range (-1023 to 1023) to index range (0 to 2046)
        return self.seen[index]

    def mark_as_seen(self, number):
        """
        Marks a number as seen in the boolean array.
        :param number: The integer to mark as seen.
        """
        index = number + 1023
        self.seen[index] = True

    def write_unique_numbers_directly(self, file_path):
        """
        Writes unique integers directly to the output file.
        :param file_path: The path to the output file.
        """
        try:
            with open(file_path, "w") as output_file:
                for i, seen in enumerate(self.seen):
                    if seen:
                        output_file.write(f"{i - 1023}\n") 
        except OSError as e:
            print(f"Error writing to file '{file_path}': {str(e)}")

    def read_input_file(self, file_path):
        """
        Reads lines from the input file.
        :param file_path: The path to the input file.
        :return: Generator of lines from the file.
        """
        try:
            with open(file_path, "r") as input_file:
                for line in input_file:
                    yield line
        except OSError as e:
            print(f"Error reading file '{file_path}': {str(e)}")
    
    def get_file_path(self, file_name):
        """
        Constructs the full file path using os.path.join for platform independence.
        :param file_name: The file name to append to the base path.
        :return: Full file path.
        """
        base_path = os.path.join("dsa", "hw01")
        file_path = os.path.join(base_path, file_name)
        return file_path

if __name__ == "__main__":
    # If command line arguments are provided, use them; otherwise use defaults
    if len(sys.argv) >= 3:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]
    else:
        input_file_name = "sample_inputs/sample_01.txt"
        output_file_name = "sample_results/sample_01.txt_results.txt"

    unique_int = UniqueInt()

    # Start time measurement
    start_time = time.time()

    # Process file
    unique_int.process_file(input_file_name, output_file_name)

    # End time measurement
    end_time = time.time()

    # Calculate memory usage (RSS: non-swapped physical memory the process is using)
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024  # Memory usage in KB

    # Display the runtime and memory usage
    print(f"Execution time: {end_time - start_time} seconds")
    print(f"Memory used: {memory_usage} KB")
