import os
import json
import sys
import subprocess

# Function to install a package
def install_package(package):
    print(f"{package} is not installed. Installing now...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Check and import necessary libraries
try:
    import pandas as pd
except ImportError:
    install_package('pandas')
    import pandas as pd  # Try importing again after installation

try:
    from tqdm import tqdm
except ImportError:
    install_package('tqdm')
    from tqdm import tqdm  # Try importing again after installation

# Prompt for the parent folder
parent_folder = input("Enter the path of the parent folder: ")
# Prompt for the output CSV file name
output_csv = input("Enter the output CSV file name (including .csv extension): ")

# Check if the folder exists
if not os.path.exists(parent_folder):
    print("The specified folder does not exist.", flush=True)
    exit()

# Initialize a list to hold the results
result = []

# Get all JSON files in the parent folder and its subfolders
json_files = []
for root, _, files in os.walk(parent_folder):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

# Create a progress bar for processing JSON files
for json_file_path in tqdm(json_files, desc="Processing JSON files", unit="file"):
    try:
        with open(json_file_path, 'r') as json_file:
            json_content = json.load(json_file)

            # If the JSON is a list, extend the result
            if isinstance(json_content, list):
                result.extend(json_content)
            else:
                result.append(json_content)
    except Exception as e:
        print(f"Failed to process {json_file_path}: {e}", flush=True)

# Export the results to a CSV file
if result:
    df = pd.DataFrame(result)
    df.to_csv(output_csv, index=False)
    print(f"Successfully exported to {output_csv}", flush=True)
else:
    print("No valid JSON data found to export.", flush=True)
