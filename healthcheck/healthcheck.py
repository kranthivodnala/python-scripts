import os
import datetime
import csv
import json
import requests

# Open the CSV file and read the URLs and do health checks and log results in the same csv file in another column
def health_check_and_log(csv_file_path):
    temp_file_path = csv_file_path + '.tmp'

    with open(csv_file_path, mode='r', newline='') as csvfile, open(temp_file_path, mode='w', newline='') as temp_csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['Status', 'Response Time (ms)', 'Checked At']
        writer = csv.DictWriter(temp_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            url = row['website']
            try:
                start_time = datetime.datetime.now()
                response = requests.get(url, timeout=5)
                response_time = (datetime.datetime.now() - start_time).total_seconds() * 1000  # in milliseconds
                status = 'Healthy' if response.status_code == 200 else f'Unhealthy (Status Code: {response.status_code})'
            except requests.RequestException as e:
                status = f'Unhealthy (Error: {str(e)})'
                response_time = 'N/A'

            row['Status'] = status
            row['Response Time (ms)'] = response_time
            row['Checked At'] = datetime.datetime.now().isoformat()
            writer.writerow(row)
    os.replace(temp_file_path, csv_file_path)
# Example usage
# ...existing code...
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run website health checks and log to CSV.")
    parser.add_argument(
        "csv_file",
        nargs="?",
        default=r"C:\Users\User\websites_url.csv", # Replace with File location
    )
    args = parser.parse_args()
    health_check_and_log(args.csv_file)
# ...existing code...
