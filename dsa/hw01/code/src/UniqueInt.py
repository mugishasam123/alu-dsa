#!/usr/bin/python3

from os import path
import time
import psutil


class UniqueInt:
    """
    A class to process files and extract unique integers from a specified range (-1023 to 1023).
    """

    def __init__(self):
        # We will use a boolean array of size 2047 to represent the integers from -1023 to 1023
        # Index 0 corresponds to -1023, and index 2046 corresponds to 1023
        self.seen = [False] * 2047

    def process_file(self, input_file_name, output_file_name):
        """
        Reads integers from the input file, identifies unique integers, sorts them, and writes them to the output file.
        :param input_file_path: Path to the input file containing integers.
        :param output_file_path: Path to the output file where unique integers will be written.
        """
        try:
            input_file_path = self.getFilePath(input_file_name)
            output_file_path = self.getFilePath(output_file_name)

            with open(input_file_path, "r") as input_file:
                # Collect unique numbers
                unique_numbers = []

                for line in input_file:
                    line = line.strip()
                    
                    try:
                        number = int(line)
                    except ValueError:
                        continue
                    
                    if -1023 <= number <= 1023:
                        if not self.is_seen(number):
                            self.mark_as_seen(number)
                            unique_numbers.append(number)
                
                # Sort unique numbers using quicksort
                self.sort(unique_numbers, 0, len(unique_numbers) - 1)
                
                # Write sorted unique numbers to the output file
                with open(output_file_path, "w") as output_file:
                    for number in unique_numbers:
                        output_file.write(f"{number}\n")

        except FileNotFoundError:
            print(f"Error: File '{input_file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

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

    def sort(self, arr, low, high):
        """
        Sorts an array in ascending order using quicksort.
        :param arr: The array to sort.
        :param low: The starting index of the segment to sort.
        :param high: The ending index of the segment to sort.
        """
        if low < high:
            # pi is the partitioning index
            pi = self.partition(arr, low, high)

            # Recursively sort elements before partition and after partition
            self.sort(arr, low, pi - 1)
            self.sort(arr, pi + 1, high)

    def partition(self, arr, low, high):
        """
        Partition function for quicksort. Places the pivot element at the correct position
        in the sorted array and places all smaller elements to the left and larger elements to the right.
        :param arr: The array to partition.
        :param low: The starting index of the segment.
        :param high: The ending index of the segment.
        :return: The partition index.
        """
        pivot = arr[high]  # Pivot element
        i = low - 1        # Index of smaller element

        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                # Swap arr[i] and arr[j]
                arr[i], arr[j] = arr[j], arr[i]

        # Swap arr[i+1] and arr[high] (or pivot)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]

        return i + 1
    
    def getFilePath(self,file_name):
        file_path = path.relpath("dsa/hw01" + file_name)
        return file_path 



if __name__ == "__main__":
    
    input_file_path ="/sample_inputs/sample_01.txt"
    output_file_path = "/sample_results/sample_01.txt_results.txt"

    unique_int = UniqueInt()

    # Start time measurement
    start_time = time.time()

    # Process file
    unique_int.process_file(input_file_path, output_file_path)

    # End time measurement
    end_time = time.time()

    # Calculate memory usage
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024  # Memory usage in KB

    # Display the runtime and memory usage
    print(f"Execution time: {end_time - start_time} seconds")
    print(f"Memory used: {memory_usage} KB")
