import os
import pandas as pd

def combine_csv_files(root_directory, output_file):
    all_csv_paths = []


    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.csv'):
                full_path = os.path.join(root, file)
                all_csv_paths.append(full_path)

    all_csv_paths.sort()

    all_dataframes = [pd.read_csv(path, header=0) for path in all_csv_paths]
    combined_df = pd.concat(all_dataframes, ignore_index=True)

    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV file created: {output_file}")

root_directory = 'odds_data'
output_file = 'odds_data/COMPLETE_DATA.csv'
combine_csv_files(root_directory, output_file)