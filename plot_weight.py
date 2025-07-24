import matplotlib.pyplot as plt
import csv
import argparse
from datetime import datetime, timedelta
from typing import List, Tuple, Dict

DATA_DIR = 'data'
FENTON_DIR = 'fenton_boys'
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

def load_fenton_data(due_date: datetime) -> Dict[str, Tuple[List[datetime], List[float]]]:
    """
    Load Fenton growth data from CSV files and convert gestational ages to actual dates.

    Parameters:
    due_date (datetime): The expected due date.

    Returns:
    Dict[str, List[Tuple[datetime, float]]]: Dictionary mapping percentile to list of (date, weight) tuples.
    """
    fenton_data: Dict[str, Tuple[List[datetime], List[float]]] = {}

    for percentile in ['3%', '10%', '50%', '90%', '97%']:
        file_path = f"{FENTON_DIR}/{percentile}.csv"
        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                fenton_data[percentile] = ([], [])
                for row in reader:
                    if len(row) == 2:
                        try:
                            gestational_age_weeks = float(row[0])
                            weight = 1000.*float(row[1]) # convert to grams
                            date = due_date - timedelta(weeks=(40 - gestational_age_weeks))
                            fenton_data[percentile][0].append(date)
                            fenton_data[percentile][1].append(weight)
                        except ValueError as e:
                            print(f"Skipping invalid row {row} in {file_path}: {e}")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found. Ensure the file exists in the 'fenton_boys/' directory.")

    return fenton_data

def plot_data(dates: List[datetime], weights: List[float], fenton_data: Dict[str, Tuple[List[datetime], List[float]]]) -> None:
    """
    Plot the weight data against dates.

    Parameters:
    dates (List[datetime]): List of dates.
    weights (List[float]): Corresponding list of weights.
    fenton_data (Dict[str, List[Tuple[datetime, float]]]): Fenton growth data.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker='s', linestyle='', color='b', label='Baby Weight')

    for percentile, data in fenton_data.items():
        plt.plot(data[0], data[1], linestyle='--', label=f'{percentile} Percentile')

    plt.xlabel('Date')
    plt.ylabel('Weight [g]')
    plt.title('Weight Development')
    plt.grid(True, linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main() -> None:
    """
    Main function to parse arguments, load data, and plot the weight curve.
    """
    parser = argparse.ArgumentParser(description='Plot weight curve from CSV.')
    parser.add_argument('filename', nargs='?', default=DEFAULT_FILENAME, help=f'CSV filename (default: {DEFAULT_FILENAME})')
    parser.add_argument('--due-date', type=str, required=True, help='Expected due date in YYYY-MM-DD format')
    args = parser.parse_args()

    due_date = datetime.strptime(args.due_date, '%Y-%m-%d')
    dates, weights = load_data(args.filename)
    fenton_data = load_fenton_data(due_date)

    if dates:
        plot_data(dates, weights, fenton_data)

if __name__ == "__main__":
    main()
