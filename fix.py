import os
from unidecode import unidecode

def name_format(name):
    name = unidecode(name)
    formatted_name = name.strip().replace(" ", '-')
    formatted_name = formatted_name.replace('/', '-')
    while '--' in formatted_name:
        formatted_name = formatted_name.replace('--', '-')
    return formatted_name.upper()

def rename_csv_files_in_subfolders(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.csv'):
                new_filename = name_format(filename)
                old_file = os.path.join(dirpath, filename)
                new_file = os.path.join(dirpath, new_filename)
                os.rename(old_file, new_file)
                print(f'Renamed "{old_file}" to "{new_file}"')

# Example usage
rename_csv_files_in_subfolders('odds_data')
