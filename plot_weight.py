"""
Plot weight curves from logged weight data of a premature baby, in comparison to the standard Fenton growth curves at various percentiles.

This script loads weight data from a CSV file and plots it against the Fenton growth curves for comparison. The script expects a CSV file with two columns: date and weight. The Fenton growth data is loaded from predefined CSV files in the 'fenton_boys/' directory.

Usage:
python plot_weight.py <filename> --due-date <YYYY-MM-DD>
"""

import matplotlib.pyplot as plt
import csv
import argparse
from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_DIRECTORY = 'data'
FENTON_DIRECTORY = 'fenton_boys'
DEFAULT_FILE_NAME = 'weight.csv'

def load_data(file_name: str) -> Tuple[List[datetime], List[float]]:
    """
    Load date and weight data from a CSV file.

    Parameters:
    file_name (str): The name of the CSV file to load.

    Returns:
    Tuple[List[datetime], List[float]]: Lists of dates and corresponding weights.
    """
    dates: List[datetime] = []
    weights: List[float] = []

    file_path = f"{DATA_DIRECTORY}/{file_name}"

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
                        logging.warning(f"Skipping invalid row {row}: {e}")
    except FileNotFoundError:
        logging.error(f"Error: File '{file_path}' not found. Ensure the file exists in the 'data/' directory.")
        return [], []

    if not dates:
        logging.warning("No valid data found in the file. Please check the file format and contents.")
        return [], []

    return dates, weights

def load_fenton_data(due_date: datetime) -> Dict[str, Tuple[List[datetime], List[float]]]:
    """
    Load Fenton growth data from CSV files and convert gestational ages to actual dates.

    Parameters:
    due_date (datetime): The expected due date.

    Returns:
    Dict[str, Tuple[List[datetime], List[float]]]: Dictionary mapping percentile to list of (date, weight) tuples.
    """
    fenton_data: Dict[str, Tuple[List[datetime], List[float]]] = {}

    for percentile in ['3%', '10%', '50%', '90%', '97%']:
        file_path = f"{FENTON_DIRECTORY}/{percentile}.csv"
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
                            logging.warning(f"Skipping invalid row {row} in {file_path}: {e}")
        except FileNotFoundError:
            logging.error(f"Error: File '{file_path}' not found. Ensure the file exists in the 'fenton_boys/' directory.")

    return fenton_data

def plot_data(baby_dates: List[datetime], baby_weights: List[float], fenton_growth_data: Dict[str, Tuple[List[datetime], List[float]]]) -> None:
    """
    Plot the weight data against dates.

    Parameters:
    baby_dates (List[datetime]): List of dates for the baby's weight measurements.
    baby_weights (List[float]): Corresponding list of weights for the baby.
    fenton_growth_data (Dict[str, Tuple[List[datetime], List[float]]]): Fenton growth data for comparison.
    """
    def compute_limits(values, margin_percent=0.05):
        """
        Compute the limits for a plot axis with a specified margin percentage.
    
        Parameters:
        values (List[float]): List of values for the axis.
        margin_percent (float): Percentage of value range to add/subtract from the min/max values as margin (default: 0.05).
    
        Returns:
        Tuple[float, float]: Tuple of (min_limit, max_limit) according to the specified margin.
        """
        range_value = max(values) - min(values)
        margin = range_value * margin_percent
        return min(values) - margin, max(values) + margin
    
    plt.figure(figsize=(10, 5))
    plt.plot(baby_dates, baby_weights, marker='o', linestyle='', color='b', label='Baby Weight')
    
    line_styles = {
        '3%': ':',
        '10%': '--',
        '50%': '-',
        '90%': '--',
        '97%': ':'
    }
    
    for percentile, data in fenton_growth_data.items():
        plt.plot(data[0], data[1], linestyle=line_styles[percentile], label=f'{percentile} Percentile')
    
    plt.xlim(*compute_limits(baby_dates, margin_percent=0.05))
    plt.ylim(*compute_limits(baby_weights, margin_percent=0.10))
    
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
    parser.add_argument('file_name', nargs='?', default=DEFAULT_FILE_NAME, help=f'CSV filename (default: {DEFAULT_FILE_NAME})')
    parser.add_argument('-d', '--due-date', type=str, required=True, help='Expected due date in YYYY-MM-DD format')
    args = parser.parse_args()

    due_date = datetime.strptime(args.due_date, '%Y-%m-%d')
    baby_dates, baby_weights = load_data(args.file_name)
    fenton_growth_data = load_fenton_data(due_date)

    if baby_dates:
        plot_data(baby_dates, baby_weights, fenton_growth_data)

if __name__ == "__main__":
    main()
