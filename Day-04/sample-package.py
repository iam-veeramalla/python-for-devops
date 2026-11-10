import os
import math
import random
from typing import List

def generate_random_numbers(count: int, start: int, end: int) -> List[int]:
    """Generate a list of random integers within a given range."""
    return [random.randint(start, end) for _ in range(count)]

def calculate_square_roots(numbers: List[int]) -> List[float]:
    """Calculate the square root of each number in the list."""
    return [math.sqrt(num) for num in numbers]

def create_directory(directory_name: str) -> None:
    """Create a directory if it does not exist."""
    os.makedirs(directory_name, exist_ok=True)

def write_numbers_to_file(filename: str, numbers: List[int]) -> None:
    """Write a list of numbers to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(map(str, numbers)))

def read_numbers_from_file(filename: str) -> List[int]:
    """Read numbers from a file and return them as a list."""
    with open(filename, "r", encoding="utf-8") as file:
        return [int(line.strip()) for line in file]

def main() -> None:
    """Main function to execute the script."""
    numbers = generate_random_numbers(10, 1, 100)
    square_roots = calculate_square_roots(numbers)

    output_dir = "output"
    create_directory(output_dir)

    file_path = os.path.join(output_dir, "numbers.txt")
    write_numbers_to_file(file_path, numbers)

    read_numbers = read_numbers_from_file(file_path)

    print("Original Numbers:", read_numbers)
    print("Square Roots:", square_roots)

if __name__ == "__main__":
    main()
