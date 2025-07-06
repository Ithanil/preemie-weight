import matplotlib.pyplot as plt
import csv
import argparse
from datetime import datetime

DATA_DIR = 'data'
DEFAULT_FILENAME = 'weight.csv'

def main():
    parser = argparse.ArgumentParser(description='Plot weight curve from CSV.')
    parser.add_argument('filename', nargs='?', default=DEFAULT_FILENAME, help=f'CSV filename (default: {DEFAULT_FILENAME})')
    args = parser.parse_args()

    dates = []
    weights = []

    file_path = f"{DATA_DIR}/{args.filename}"

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
        print(f"Error: File '{file_path}' not found.")
        return

    if not dates:
        print("No valid data found in the file.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker='o', linestyle='-', color='b')
    plt.xlabel('Date')
    plt.ylabel('Weight [g]')
    plt.title('Weight Development')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
