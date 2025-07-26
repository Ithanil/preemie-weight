"""
Script to add weight data for preemies to a CSV file.

Usage:
python add_weight.py --file <filename> <date> <weight>
"""

import csv
from datetime import datetime
import argparse

DATA_DIR = "data"
DATA_FILENAME = "weight.csv"

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        print("Invalid date format. Please try again.")
        return False

def get_valid_date(prompt="Enter date (YYYY-MM-DD): "):
    while True:
        date_str = input(prompt)
        if validate_date(date_str):
            return date_str

def validate_weight(weight_str):
    if weight_str.isdigit():
        weight = int(weight_str)
        if weight > 0:
            return True
    print("Weight must be a positive integer.")
    return False

def get_valid_weight(prompt="Enter weight in grams: "):
    while True:
        weight_str = input(prompt)
        if validate_weight(weight_str):
            return weight_str

def main() -> None:
    """
    Main function to parse arguments, validate inputs, and add weight data to a CSV file.
    """
    parser = argparse.ArgumentParser(description="Add weight data for preemies.")
    parser.add_argument('--file', type=str, default=DATA_FILENAME, help='Filename to store weight data (default: weight.csv)')
    parser.add_argument('date', nargs='?', help='Date of the weight measurement (YYYY-MM-DD)')
    parser.add_argument('weight', nargs='?', type=float, help='Weight in kilograms')

    args = parser.parse_args()

    if args.date:
        if validate_date(args.date):
            date = args.date
        else:
            print(f"Invalid date format: {args.date}. Falling back to interactive mode.")
            date = get_valid_date()
    else:
        date = get_valid_date()

    if args.weight:
        weight_str = str(args.weight)
        if validate_weight(weight_str):
            weight = weight_str
        else:
            print(f"Invalid weight: {args.weight}. Weight must be a positive number. Falling back to interactive mode.")
            weight = get_valid_weight()
    else:
        weight = get_valid_weight()

    file_path = f"{DATA_DIR}/{args.file}"

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, weight])

    print(f"Added {date}, {weight} kg to {file_path}")

if __name__ == "__main__":
    main()
