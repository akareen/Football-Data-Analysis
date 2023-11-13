import os

def rename_files(root_directory):
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.csv') and '---' in file:
                original_file_path = os.path.join(root, file)
                new_file_name = file.replace('---', '-')
                new_file_path = os.path.join(root, new_file_name)

                os.rename(original_file_path, new_file_path)
                print(f"Renamed {original_file_path} to {new_file_path}")

root_directory = 'odds_data'
rename_files(root_directory)
