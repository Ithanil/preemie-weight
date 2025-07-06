import csv
from datetime import datetime

DATA_DIR = "data"
DATA_FILENAME = "weight.csv"

def get_valid_date():
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Invalid date format. Please try again.")

def get_valid_weight():
    while True:
        weight_str = input("Enter weight in grams: ")
        if weight_str.isdigit():
            weight = int(weight_str)
            if weight > 0:
                return weight_str
            else:
                print("Weight must be a positive integer.")
        else:
            print("Invalid weight. Please enter a valid number.")

def main():
    date = get_valid_date()
    weight = get_valid_weight()
    file_path = f"{DATA_DIR}/{DATA_FILENAME}"

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, weight])

    print(f"Added {date}, {weight} grams to {file_path}")

if __name__ == "__main__":
    main()
