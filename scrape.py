import pandas as pd
import requests
import os

# Base URL for the cycling data
base_url = "https://cycling.data.tfl.gov.uk/usage-stats/"

# Read Excel file to extract file names from the first column
excel_file = "names.xlsx"  # Path to your Excel file
df = pd.read_excel(excel_file)

# Extract file names from the first column
file_names = df.iloc[:, 0].dropna()  # Ensure no empty values

# Directory to save downloaded files
output_dir = "tfl_csv_files"
os.makedirs(output_dir, exist_ok=True)

# Download each file by joining the base URL with the file name
for file_name in file_names:
    url = base_url + file_name  # Construct full URL
    file_path = os.path.join(output_dir, file_name)
    try:
        print(f"Downloading {file_name}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"Saved: {file_path}")
        else:
            print(f"Failed to download {file_name}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")

print("Download complete!")