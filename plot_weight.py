import matplotlib.pyplot as plt
import csv
import argparse
from datetime import datetime
from typing import List, Tuple

DATA_DIR = 'data'
DEFAULT_FILENAME = 'weight.csv'

def load_data(filename: str) -> Tuple[List[datetime], List[float]]:
    """
    Load date and weight data from a CSV file.

    Parameters:
    filename (str): The name of the CSV file to load.

    Returns:
    Tuple[List[datetime], List[float]]: Lists of dates and corresponding weights.
    """
    dates: List[datetime] = []
    weights: List[float] = []

    file_path = f"{DATA_DIR}/{filename}"

    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    date_str, weight_str = row
                    try:
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        weight = float(weight_str)
                        dates.append(date)
                        weights.append(weight)
                    except ValueError as e:
                        print(f"Skipping invalid row {row}: {e}")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Ensure the file exists in the 'data/' directory.")
        return [], []

    if not dates:
        print("No valid data found in the file. Please check the file format and contents.")
    
    return dates, weights

def plot_data(dates: List[datetime], weights: List[float]) -> None:
    """
    Plot the weight data against dates.

    Parameters:
    dates (List[datetime]): List of dates.
    weights (List[float]): Corresponding list of weights.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker='o', linestyle='-', color='b')
    plt.xlabel('Date')
    plt.ylabel('Weight [g]')
    plt.title('Weight Development')
    plt.grid(True, linestyle='--')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main() -> None:
    """
    Main function to parse arguments, load data, and plot the weight curve.
    """
    parser = argparse.ArgumentParser(description='Plot weight curve from CSV.')
    parser.add_argument('filename', nargs='?', default=DEFAULT_FILENAME, help=f'CSV filename (default: {DEFAULT_FILENAME})')
    args = parser.parse_args()

    dates, weights = load_data(args.filename)

    if dates:
        plot_data(dates, weights)

if __name__ == "__main__":
    main()
