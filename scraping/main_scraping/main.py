import os
import csv
import glob

def read_and_append_csv_files(root_folder):
    # This list will hold all the rows from all the CSV files
    all_rows = []

    # Walk through the directories, and sort them in descending order
    for root, dirs, files in sorted(os.walk(root_folder), reverse=True):
        # Find all CSV files in the current directory
        for file in glob.glob(os.path.join(root, '*.csv')):
            with open(file, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Skip the header row
                for row in reader:
                    all_rows.append(row)
    
    return all_rows

def write_to_csv(file_path, data):
    score_data_headers = [
                "Week", "Day", "Date", "Time", "Home Team", 
                "Home Expected Goals", "Home Goals", "Away Goals", 
                "Away Expected Goals", "Away Team", 
                "Attendance", "Venue", "Referee", "Match Report", "Notes"
            ]
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(score_data_headers)
        writer.writerows(data)

# Use the function
root_folder = 'match_and_player_data/competition_data' # Change this to your folder path
all_csv_rows = read_and_append_csv_files(root_folder)

# Write to a new CSV file
output_csv_path = 'match_and_player_data/competition_data/ALL_MATCH_RESULTS.csv'  # Change this to your desired output path
write_to_csv(output_csv_path, all_csv_rows)
