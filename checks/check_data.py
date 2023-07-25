import pandas as pd
import argparse
import sys

def check_data(input_file):
    # Load data
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"File {input_file} not found. Make sure you've ingested and processed the data correctly.")
        sys.exit(1)

    # Check columns
    expected_columns = ["country", "time", "electricity_consumption", "green_energy_generation"]
    if not all(column in data.columns for column in expected_columns):
        print(f"Expected columns {expected_columns}, but got {list(data.columns)}.")
        sys.exit(1)

    # Check for NANs
    if data.isna().any().any():
        print("Data contains NANs. Please make sure to deal with NANs in your data processing stage.")
        sys.exit(1)
    
    # Check that all expected countries are present
    expected_countries = ["Spain", "UK", "Germany", "Denmark", "Sweden", "Hungary", "Italy", "Poland", "Netherlands"]
    if not all(country in data["country"].unique() for country in expected_countries):
        print(f"Data does not contain all expected countries. Expected {expected_countries}, but got {list(data['country'].unique())}.")
        sys.exit(1)
    
    # Check that time data is in correct format and range
    try:
        data['time'] = pd.to_datetime(data['time'])
    except ValueError:
        print("Time data is not in the correct format. Please ensure it is in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).")
        sys.exit(1)
    
    # Check that the electricity consumption and green energy generation data are within a reasonable range
    if data["electricity_consumption"].min() < 0 or data["green_energy_generation"].min() < 0:
        print("Electricity consumption and/or green energy generation contain negative values. Please check your data.")
        sys.exit(1)
    
    # Check for duplicates
    if data.duplicated().any():
        print("Data contains duplicated rows. Please check your data.")
        sys.exit(1)
    
    print("All checks passed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input file.")
    args = parser.parse_args()
    check_data(args.input_file)
